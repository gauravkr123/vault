#!/usr/bin/env python3
"""
ISM Policy Analyzer
Analyzes Elasticsearch Index State Management (ISM) policies and generates detailed reports
about failed transitions, rollover operations, and provides recommendations.

Features:
- Analyzes failed and pending ISM operations
- Ignores system indices (starting with '.')
- Provides detailed failure analysis including circuit breaker errors
- Generates actionable recommendations
- Supports both console output and detailed markdown reports

Usage:
    python ism_policy_analyzer.py <path_to_json_file>
    python ism_policy_analyzer.py /path/to/index_ism_policy.json
    python3 ism_policy_analyzer.py dev_index_ism_policy.json --index-size-csv dev_index_size.csv --report dev_detailed_analysis_with_age.md
"""

import json
import sys
import os
from datetime import datetime, timezone
from typing import Dict, List, Tuple, Optional
import argparse


class ISMPolicyAnalyzer:
    def get_index_age_days(self, index_data: Dict) -> str:
        """Calculate index age in days from creation_date to today."""
        creation_ts = index_data.get('creation_date')
        if not creation_ts:
            return "Unknown"
        try:
            # creation_ts is in ms, convert to seconds
            creation_dt = datetime.fromtimestamp(creation_ts / 1000, tz=timezone.utc)
            now_dt = datetime.now(timezone.utc)
            age_days = (now_dt - creation_dt).days
            return str(age_days)
        except Exception:
            return "Unknown"
    def __init__(self, file_path: str, index_size_csv: str = None):
        self.file_path = file_path
        self.data = None
        self.failed_indices = []
        self.pending_indices = []
        self.successful_indices = []
        self.circuit_breaker_limit = 31111669350  # 28.9GB
        self.index_sizes = {}
        if index_size_csv:
            self.index_sizes = self._load_index_sizes(index_size_csv)

    def _load_index_sizes(self, csv_path: str):
        sizes = {}
        try:
            with open(csv_path, 'r') as f:
                # Read header and split by whitespace
                header_line = f.readline()
                header = [h.strip() for h in header_line.split()]
                index_col = None
                size_col = None
                for i, h in enumerate(header):
                    if h.lower() == 'index':
                        index_col = i
                    elif h.lower().replace(' ', '') == 'store.size':
                        size_col = i
                if index_col is None or size_col is None:
                    raise Exception('CSV header missing required columns')
                # Read the rest of the lines
                for line in f:
                    parts = line.split()
                    if len(parts) > max(index_col, size_col):
                        idx = parts[index_col].strip()
                        size = parts[size_col].strip()
                        sizes[idx] = size
        except Exception as e:
            print(f"Warning: Could not load index sizes from {csv_path}: {e}")
        return sizes
        
    def load_data(self) -> bool:
        """Load JSON data from file"""
        try:
            with open(self.file_path, 'r') as file:
                self.data = json.load(file)
            return True
        except FileNotFoundError:
            print(f"❌ Error: File '{self.file_path}' not found.")
            return False
        except json.JSONDecodeError as e:
            print(f"❌ Error: Invalid JSON format in '{self.file_path}': {e}")
            return False
        except Exception as e:
            print(f"❌ Error loading file: {e}")
            return False
    
    def convert_timestamp(self, timestamp: int) -> str:
        """Convert epoch timestamp to readable format"""
        try:
            dt = datetime.fromtimestamp(timestamp / 1000, tz=timezone.utc)
            return dt.strftime('%Y-%m-%d %H:%M:%S UTC')
        except:
            return f"Invalid timestamp: {timestamp}"
    
    def convert_bytes_to_gb(self, bytes_value: str) -> float:
        """Convert byte string to GB"""
        try:
            # Remove brackets and convert to int
            bytes_int = int(bytes_value.strip('[]'))
            return bytes_int / (1024**3)
        except:
            return 0.0
    
    def parse_size_condition(self, size_str: str) -> float:
        """Parse size condition (e.g., '480gb' -> 480.0)"""
        try:
            if size_str.lower().endswith('gb'):
                return float(size_str[:-2])
            elif size_str.lower().endswith('mb'):
                return float(size_str[:-2]) / 1024
            else:
                return float(size_str)
        except:
            return 0.0
    
    def extract_index_size(self, index_data: Dict) -> str:
        """Get index size from loaded CSV sizes, fallback to ISM info if not found."""
        index_name = index_data.get('index', None)
        if index_name and index_name in self.index_sizes:
            return self.index_sizes[index_name]
        # Fallback to ISM info
        try:
            info = index_data.get('info', {})
            if 'conditions' in info and 'min_size' in info['conditions']:
                current_size = info['conditions']['min_size'].get('current', 'Unknown')
                return current_size
            return "Unknown"
        except:
            return "Unknown"
    
    def parse_age_condition(self, age_str: str) -> float:
        """Parse age condition (e.g., '7d' -> 7.0, '1.8d' -> 1.8)"""
        try:
            if age_str.lower().endswith('d'):
                return float(age_str[:-1])
            elif age_str.lower().endswith('h'):
                return float(age_str[:-1]) / 24
            else:
                return float(age_str)
        except:
            return 0.0
    
    def analyze_index(self, index_name: str, index_data: Dict) -> Dict:
        """Analyze a single index and return its status"""
        analysis = {
            'index': index_name,
            'policy': index_data.get('policy_id', 'Unknown'),
            'state': index_data.get('state', {}).get('name', 'Unknown'),
            'enabled': index_data.get('enabled', True),
            'rolled_over': index_data.get('rolled_over', False),
            'action': index_data.get('action', {}),
            'step': index_data.get('step', {}),
            'info': index_data.get('info', {}),
            'creation_date': index_data.get('index_creation_date'),
            'size': self.extract_index_size(index_data),
            'status': 'Unknown',
            'issues': [],
            'recommendations': []
        }
        
        action = analysis['action']
        step = analysis['step']
        info = analysis['info']
        
        # Determine status based on action and step
        if action.get('failed', False):
            analysis['status'] = 'FAILED'
            analysis['failure_reason'] = self._extract_failure_reason(info, action)
            analysis['consumed_retries'] = action.get('consumed_retries', 0)
            analysis['last_retry'] = action.get('last_retry_time', 0)
            self.failed_indices.append(analysis)
            
        elif step.get('step_status') == 'failed':
            analysis['status'] = 'FAILED'
            analysis['failure_reason'] = self._extract_failure_reason(info, step)
            self.failed_indices.append(analysis)
            
        elif step.get('step_status') == 'timed_out':
            analysis['status'] = 'FAILED'
            analysis['failure_reason'] = 'Operation timed out'
            self.failed_indices.append(analysis)
            
        elif step.get('step_status') == 'condition_not_met':
            analysis['status'] = 'PENDING'
            analysis['pending_reason'] = info.get('message', 'Waiting for conditions')
            if 'conditions' in info:
                analysis['conditions'] = info['conditions']
            self.pending_indices.append(analysis)
            
        else:
            analysis['status'] = 'SUCCESS'
            self.successful_indices.append(analysis)
        
        return analysis
    
    def _extract_failure_reason(self, info: Dict, action_or_step: Dict) -> str:
        """Extract detailed failure reason from info and action/step data"""
        # Check for circuit breaking exceptions
        if 'shard_failures' in info:
            failures = info['shard_failures']
            if failures and 'CircuitBreakingException' in str(failures[0]):
                return self._parse_circuit_breaker_error(failures[0])
        
        # Check for timeout
        if action_or_step.get('step_status') == 'timed_out':
            return 'Operation timed out'
        
        # Check for generic message
        if 'message' in info:
            return info['message']
        
        return 'Unknown failure reason'
    
    def _parse_circuit_breaker_error(self, error_msg: str) -> str:
        """Parse circuit breaker error message"""
        try:
            if 'Data too large' in error_msg:
                # Extract memory usage information
                parts = error_msg.split(',')
                usage_info = []
                for part in parts:
                    if 'would be' in part:
                        usage = part.split('[')[1].split(']')[0]
                        usage_info.append(f"Would use: {usage}")
                    elif 'larger than the limit' in part:
                        limit = part.split('[')[1].split(']')[0]
                        usage_info.append(f"Limit: {limit}")
                    elif 'real usage' in part:
                        real = part.split('[')[1].split(']')[0]
                        usage_info.append(f"Current: {real}")
                
                return f"Circuit Breaker - Memory limit exceeded. {', '.join(usage_info)}"
        except:
            pass
        
        return "Circuit Breaker - Data too large"
    
    def generate_recommendations(self, output_file: Optional[str] = None) -> str:
        """Generate detailed recommendations file"""
        if not self.data:
            return "❌ No data loaded. Please load data first."
        
        # Ensure we have analyzed data
        if not hasattr(self, 'failed_indices') or not self.failed_indices:
            self.analyze_all_indices()
        
        recommendations = []
        recommendations.append("# ISM Policy Recommendations")
        recommendations.append(f"**Generated:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        recommendations.append(f"**Source File:** {os.path.basename(self.file_path)}")
        recommendations.append("")
        
        # Executive summary of issues
        recommendations.append("## Issue Summary")
        recommendations.append("")
        
        if self.failed_indices:
            circuit_breaker_failures = [idx for idx in self.failed_indices if 'Circuit Breaker' in idx.get('failure_reason', '')]
            timeout_failures = [idx for idx in self.failed_indices if 'timeout' in idx.get('failure_reason', '').lower()]
            
            recommendations.append(f"**Total Failed Indices:** {len(self.failed_indices)}")
            recommendations.append(f"**Circuit Breaker Failures:** {len(circuit_breaker_failures)}")
            recommendations.append(f"**Timeout Failures:** {len(timeout_failures)}")
            recommendations.append("")
            
            # Immediate Actions
            recommendations.append("## 🚨 Immediate Actions Required")
            recommendations.append("")
            
            if circuit_breaker_failures:
                recommendations.append("### Circuit Breaker Failures")
                recommendations.append("**Priority: HIGH** - These indices cannot perform operations due to memory limits.")
                recommendations.append("")
                recommendations.append("#### 1. Increase Circuit Breaker Limits")
                recommendations.append("```json")
                recommendations.append("PUT /_cluster/settings")
                recommendations.append("{")
                recommendations.append("  \"persistent\": {")
                recommendations.append("    \"indices.breaker.total.limit\": \"35gb\",")
                recommendations.append("    \"indices.breaker.fielddata.limit\": \"20gb\",")
                recommendations.append("    \"indices.breaker.request.limit\": \"15gb\"")
                recommendations.append("  }")
                recommendations.append("}")
                recommendations.append("```")
                recommendations.append("")
                
                recommendations.append("#### 2. Clear Field Data Cache")
                recommendations.append("```bash")
                recommendations.append("# Clear fielddata cache to free memory immediately")
                recommendations.append("POST /_cache/clear?fielddata=true")
                recommendations.append("")
                recommendations.append("# Clear all caches if needed")
                recommendations.append("POST /_cache/clear")
                recommendations.append("```")
                recommendations.append("")
                
                recommendations.append("#### 3. Force Garbage Collection")
                recommendations.append("```bash")
                recommendations.append("POST /_nodes/gc")
                recommendations.append("```")
                recommendations.append("")
            
            if timeout_failures:
                recommendations.append("### Timeout Failures")
                recommendations.append("**Priority: HIGH** - Operations are timing out.")
                recommendations.append("")
                recommendations.append("#### 1. Check Cluster Health")
                recommendations.append("```bash")
                recommendations.append("GET /_cluster/health")
                recommendations.append("GET /_nodes/stats")
                recommendations.append("GET /_cat/pending_tasks?v")
                recommendations.append("```")
                recommendations.append("")
                
                recommendations.append("#### 2. Increase Operation Timeouts")
                recommendations.append("Update your ISM policy to include longer timeouts:")
                recommendations.append("```json")
                recommendations.append("{")
                recommendations.append("  \"policy\": {")
                recommendations.append("    \"default_state\": \"hot\",")
                recommendations.append("    \"states\": [{")
                recommendations.append("      \"name\": \"warm\",")
                recommendations.append("      \"actions\": [{")
                recommendations.append("        \"warm_migration\": {")
                recommendations.append("          \"timeout\": \"12h\"")
                recommendations.append("        }")
                recommendations.append("      }]")
                recommendations.append("    }]")
                recommendations.append("  }")
                recommendations.append("}")
                recommendations.append("```")
                recommendations.append("")
            
            # Re-enable disabled indices
            disabled_indices = [idx for idx in self.failed_indices if not idx['enabled']]
            if disabled_indices:
                recommendations.append("### Re-enable Failed Indices")
                recommendations.append("**Priority: HIGH** - After fixing root causes, re-enable these indices:")
                recommendations.append("")
                for idx in disabled_indices:
                    recommendations.append(f"#### {idx['index']}")
                    recommendations.append("```bash")
                    recommendations.append(f"# Re-enable ISM policy for {idx['index']}")
                    recommendations.append(f"POST /_plugins/_ism/change_policy/{idx['index']}")
                    recommendations.append("{")
                    recommendations.append(f"  \"policy_id\": \"{idx['policy']}\",")
                    recommendations.append("  \"state\": \"hot\"")
                    recommendations.append("}")
                    recommendations.append("```")
                    recommendations.append("")
        
        # Medium-term optimizations
        recommendations.append("## 🔧 Medium-term Optimizations")
        recommendations.append("")
        
        recommendations.append("### 1. Resource Scaling")
        recommendations.append("**Timeline: 1-2 weeks**")
        recommendations.append("")
        recommendations.append("#### Increase Heap Size")
        recommendations.append("- Current limit appears to be ~29GB")
        recommendations.append("- Recommended: Increase to 50% of available RAM")
        recommendations.append("- Update `jvm.options`: `-Xms32g -Xmx32g`")
        recommendations.append("")
        
        recommendations.append("#### Add Data Nodes")
        recommendations.append("- Distribute load across more nodes")
        recommendations.append("- Reduce memory pressure per node")
        recommendations.append("- Improve parallel processing capabilities")
        recommendations.append("")
        
        recommendations.append("### 2. Index Optimization")
        recommendations.append("**Timeline: 2-4 weeks**")
        recommendations.append("")
        recommendations.append("#### Optimize Rollover Thresholds")
        recommendations.append("```json")
        recommendations.append("PUT /_index_template/optimized_rollover")
        recommendations.append("{")
        recommendations.append("  \"index_patterns\": [\"otel-*\", \"*-logs-*\"],")
        recommendations.append("  \"template\": {")
        recommendations.append("    \"settings\": {")
        recommendations.append("      \"index.plugins.index_state_management.rollover_alias\": \"active\",")
        recommendations.append("      \"index.plugins.index_state_management.policy_id\": \"optimized_policy\"")
        recommendations.append("    }")
        recommendations.append("  }")
        recommendations.append("}")
        recommendations.append("```")
        recommendations.append("")
        
        recommendations.append("#### Implement Force Merge Before Warm Transition")
        recommendations.append("```json")
        recommendations.append("{")
        recommendations.append("  \"warm\": {")
        recommendations.append("    \"actions\": [")
        recommendations.append("      {")
        recommendations.append("        \"force_merge\": {")
        recommendations.append("          \"max_num_segments\": 1")
        recommendations.append("        }")
        recommendations.append("      },")
        recommendations.append("      {")
        recommendations.append("        \"warm_migration\": {}")
        recommendations.append("      }")
        recommendations.append("    ]")
        recommendations.append("  }")
        recommendations.append("}")
        recommendations.append("```")
        recommendations.append("")
        
        # Long-term strategy
        recommendations.append("## 📈 Long-term Strategy")
        recommendations.append("")
        
        recommendations.append("### 1. Architecture Improvements")
        recommendations.append("**Timeline: 1-3 months**")
        recommendations.append("")
        recommendations.append("- **Hot-Warm-Cold Architecture**: Implement dedicated node types")
        recommendations.append("- **Index Lifecycle Management**: Automate data tier transitions")
        recommendations.append("- **Data Retention Policies**: Implement automated deletion of old data")
        recommendations.append("- **Compression**: Enable index compression for warm/cold data")
        recommendations.append("")
        
        recommendations.append("### 2. Monitoring and Alerting")
        recommendations.append("**Timeline: 2-4 weeks**")
        recommendations.append("")
        recommendations.append("#### Set Up ISM Policy Monitoring")
        recommendations.append("```json")
        recommendations.append("PUT /_watcher/watch/ism_failures")
        recommendations.append("{")
        recommendations.append("  \"trigger\": {")
        recommendations.append("    \"schedule\": {")
        recommendations.append("      \"interval\": \"5m\"")
        recommendations.append("    }")
        recommendations.append("  },")
        recommendations.append("  \"input\": {")
        recommendations.append("    \"http\": {")
        recommendations.append("      \"request\": {")
        recommendations.append("        \"host\": \"localhost\",")
        recommendations.append("        \"port\": 9200,")
        recommendations.append("        \"path\": \"/_plugins/_ism/explain\"")
        recommendations.append("      }")
        recommendations.append("    }")
        recommendations.append("  },")
        recommendations.append("  \"condition\": {")
        recommendations.append("    \"script\": {")
        recommendations.append("      \"source\": \"return ctx.payload.total_managed_indices > 0\"")
        recommendations.append("    }")
        recommendations.append("  }")
        recommendations.append("}")
        recommendations.append("```")
        recommendations.append("")
        
        recommendations.append("#### Circuit Breaker Monitoring")
        recommendations.append("```bash")
        recommendations.append("# Monitor circuit breaker usage")
        recommendations.append("GET /_nodes/stats/breaker")
        recommendations.append("")
        recommendations.append("# Set up alerts for >80% usage")
        recommendations.append("GET /_nodes/stats/breaker?filter_path=nodes.*.breakers.parent")
        recommendations.append("```")
        recommendations.append("")
        
        recommendations.append("### 3. Performance Optimization")
        recommendations.append("**Timeline: Ongoing**")
        recommendations.append("")
        recommendations.append("- **Reduce Replica Count During Rollover**: Temporarily reduce replicas")
        recommendations.append("- **Optimize Mapping**: Use appropriate field types and disable unnecessary features")
        recommendations.append("- **Bulk Operations**: Optimize indexing performance")
        recommendations.append("- **Refresh Intervals**: Increase refresh intervals for write-heavy indices")
        recommendations.append("")
        
        # Implementation timeline
        recommendations.append("## 📅 Implementation Timeline")
        recommendations.append("")
        recommendations.append("| Priority | Action | Timeline | Impact |")
        recommendations.append("|----------|--------|----------|--------|")
        recommendations.append("| 🚨 Critical | Increase circuit breaker limits | Immediate | High |")
        recommendations.append("| 🚨 Critical | Clear fielddata cache | Immediate | High |")
        recommendations.append("| 🚨 Critical | Re-enable failed indices | After fixes | High |")
        recommendations.append("| 🔧 High | Add monitoring alerts | 1 week | Medium |")
        recommendations.append("| 🔧 High | Optimize ISM policies | 2 weeks | Medium |")
        recommendations.append("| 📈 Medium | Scale cluster resources | 2-4 weeks | High |")
        recommendations.append("| 📈 Medium | Implement hot-warm-cold | 1-3 months | High |")
        recommendations.append("")
        
        recommendations.append("## 🔍 Monitoring Commands")
        recommendations.append("")
        recommendations.append("Use these commands to monitor the situation after implementing fixes:")
        recommendations.append("")
        recommendations.append("```bash")
        recommendations.append("# Check ISM policy status")
        recommendations.append("GET /_plugins/_ism/explain")
        recommendations.append("")
        recommendations.append("# Monitor circuit breaker usage")
        recommendations.append("GET /_nodes/stats/breaker")
        recommendations.append("")
        recommendations.append("# Check cluster health")
        recommendations.append("GET /_cluster/health")
        recommendations.append("")
        recommendations.append("# Monitor index sizes")
        recommendations.append("GET /_cat/indices?v&s=store.size:desc")
        recommendations.append("")
        recommendations.append("# Check fielddata usage")
        recommendations.append("GET /_cat/fielddata?v")
        recommendations.append("```")
        
        recommendations_text = "\n".join(recommendations)
        
        # Save to file if specified
        if output_file:
            try:
                with open(output_file, 'w') as f:
                    f.write(recommendations_text)
                print(f"✅ Recommendations saved to: {output_file}")
            except Exception as e:
                print(f"❌ Error saving recommendations: {e}")
        
        return recommendations_text
    
    def analyze_all_indices(self) -> Dict:
        """Analyze all indices in the data"""
        if not self.data:
            return {}
        
        total_indices = self.data.get('total_managed_indices', 0)
        analyses = {}
        skipped_indices = []
        
        for key, value in self.data.items():
            if key != 'total_managed_indices' and isinstance(value, dict):
                # Skip indices that start with a dot (system indices)
                if key.startswith('.'):
                    skipped_indices.append(key)
                    continue
                analyses[key] = self.analyze_index(key, value)
        
        return {
            'total_indices': total_indices,
            'analyzed_indices': len(analyses),
            'skipped_indices': len(skipped_indices),
            'skipped_index_names': skipped_indices,
            'analyses': analyses,
            'summary': {
                'failed': len(self.failed_indices),
                'pending': len(self.pending_indices),
                'successful': len(self.successful_indices)
            }
        }
    
    def generate_report(self, output_file: Optional[str] = None) -> str:
        """Generate comprehensive analysis report"""
        if not self.data:
            return "❌ No data loaded. Please load data first."
        
        results = self.analyze_all_indices()
        
        report = []
        report.append("# ISM Policy Analysis Report")
        report.append(f"**Generated:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        report.append(f"**Source File:** {os.path.basename(self.file_path)}")
        report.append("")
        
        # Summary
        report.append("## Executive Summary")
        report.append(f"**Total Managed Indices:** {results['total_indices']}")
        report.append(f"**Analyzed Indices:** {results['analyzed_indices']}")
        if results['skipped_indices'] > 0:
            report.append(f"**Skipped System Indices:** {results['skipped_indices']} (indices starting with '.')")
        report.append(f"**Failed Operations:** {results['summary']['failed']} indices")
        report.append(f"**Pending Operations:** {results['summary']['pending']} indices")
        report.append(f"**Successful Operations:** {results['summary']['successful']} indices")
        report.append("")
        
        # Show skipped indices if any
        if results['skipped_indices'] > 0:
            report.append("### Skipped System Indices")
            report.append("The following system indices (starting with '.') were excluded from analysis:")
            for idx_name in results['skipped_index_names']:
                report.append(f"- `{idx_name}`")
            report.append("")
        
        # Failed indices section
        if self.failed_indices:
            report.append("## ❌ Failed Operations")
            report.append("")
            
            for i, idx in enumerate(self.failed_indices, 1):
                report.append(f"### {i}. **{idx['index']}** - {idx['action'].get('name', 'Unknown').upper()} FAILED")
                report.append(f"- **Policy:** {idx['policy']}")
                report.append(f"- **State:** {idx['state']}")
                report.append(f"- **Size:** {idx['size']}")
                report.append(f"- **Enabled:** {idx['enabled']}")
                report.append(f"- **Operation:** {idx['action'].get('name', 'Unknown')}")
                report.append(f"- **Failure Reason:** {idx.get('failure_reason', 'Unknown')}")
                
                if 'consumed_retries' in idx:
                    report.append(f"- **Retries Consumed:** {idx['consumed_retries']}")
                
                if idx.get('last_retry', 0) > 0:
                    report.append(f"- **Last Retry:** {self.convert_timestamp(idx['last_retry'])}")
                
                if idx.get('creation_date'):
                    report.append(f"- **Created:** {self.convert_timestamp(idx['creation_date'])}")
                
                report.append("")
        
        # Pending indices section
        if self.pending_indices:
            report.append("## ⏳ Pending Operations")
            report.append("")
            
            # Group by operation type
            rollover_pending = [idx for idx in self.pending_indices if idx['action'].get('name') == 'rollover']
            transition_pending = [idx for idx in self.pending_indices if idx['action'].get('name') == 'transition']
            
            if rollover_pending:
                report.append("### Pending Rollover Operations")
                for idx in rollover_pending:
                    report.append(f"**{idx['index']}** (Policy: {idx['policy']}, Size: {idx['size']})")
                    if 'conditions' in idx:
                        conditions = idx['conditions']
                        for condition, details in conditions.items():
                            if condition == 'min_index_age':
                                report.append(f"  - Age: {details['current']} / {details['condition']} required")
                            elif condition == 'min_size':
                                report.append(f"  - Size: {details['current']} / {details['condition']} required")
                    report.append("")
            
            if transition_pending:
                report.append("### Pending Transition Operations")
                for idx in transition_pending:
                    report.append(f"**{idx['index']}** (Policy: {idx['policy']}, State: {idx['state']}, Size: {idx['size']})")
                    report.append(f"  - Status: {idx.get('pending_reason', 'Evaluating conditions')}")
                report.append("")
        
        # Next steps note
        report.append("## 📋 Next Steps")
        report.append("")
        report.append("1. **Generate Recommendations**: Run with `--recommendations` flag for detailed action items")
        report.append("2. **Monitor Progress**: Re-run analysis after implementing fixes")
        report.append("3. **Set Up Alerts**: Implement monitoring for ISM policy failures")
        report.append("")
        
        # Detailed index table
        report.append("## 📊 Detailed Index Status")
        report.append("")
        report.append("| Index | Policy | State | Size | Age (days) | Operation | Status | Enabled | Issue |")
        report.append("|-------|--------|-------|------|------------|-----------|--------|---------|-------|")
        
        # Sort indices by status (failed first, then pending, then successful)
        all_indices = self.failed_indices + self.pending_indices + self.successful_indices
        
        for idx in all_indices:
            status_icon = "❌" if idx['status'] == 'FAILED' else "⏳" if idx['status'] == 'PENDING' else "✅"
            operation = idx['action'].get('name', 'Unknown')
            issue = idx.get('failure_reason', idx.get('pending_reason', 'None'))[:40]
            if len(issue) > 37:
                issue = issue[:37] + "..."
            size_display = idx['size'][:15] if len(idx['size']) > 12 else idx['size']
            policy_display = idx['policy'][:10] if len(idx['policy']) > 10 else idx['policy']
            age_days = self.get_index_age_days(idx)
            report.append(f"| {idx['index']} | {policy_display} | {idx['state']} | {size_display} | {age_days} | {operation} | {status_icon} {idx['status']} | {idx['enabled']} | {issue} |")
        
        report.append("")
        report.append("**Legend:**")
        report.append("- ❌ FAILED: Operation failed and needs intervention")
        report.append("- ⏳ PENDING: Operation waiting for conditions to be met")
        report.append("- ✅ SUCCESS: Operation completed successfully")
        
        report_text = "\n".join(report)
        
        # Save to file if specified
        if output_file:
            try:
                with open(output_file, 'w') as f:
                    f.write(report_text)
                print(f"✅ Report saved to: {output_file}")
            except Exception as e:
                print(f"❌ Error saving report: {e}")
        
        return report_text
    
    def print_summary(self):
        """Print a quick summary to console"""
        if not self.data:
            print("❌ No data loaded.")
            return
        
        results = self.analyze_all_indices()
        
        print("="*60)
        print("🔍 ISM POLICY ANALYSIS SUMMARY")
        print("="*60)
        print(f"📁 File: {os.path.basename(self.file_path)}")
        print(f"📊 Total Indices: {results['total_indices']}")
        print(f"🔍 Analyzed Indices: {results['analyzed_indices']}")
        if results['skipped_indices'] > 0:
            print(f"⏭️  Skipped System Indices: {results['skipped_indices']} (starting with '.')")
        print(f"❌ Failed: {results['summary']['failed']}")
        print(f"⏳ Pending: {results['summary']['pending']}")
        print(f"✅ Successful: {results['summary']['successful']}")
        print("="*60)
        
        if results['skipped_indices'] > 0:
            print(f"\n⏭️  Skipped system indices: {', '.join(results['skipped_index_names'][:3])}")
            if results['skipped_indices'] > 3:
                print(f"    ... and {results['skipped_indices'] - 3} more")
        
        if self.failed_indices:
            print("\n🚨 CRITICAL - Failed Indices:")
            for idx in self.failed_indices:
                print(f"  • {idx['index']} - {idx.get('failure_reason', 'Unknown error')}")
        
        if self.pending_indices:
            print(f"\n⏳ Pending Operations: {len(self.pending_indices)} indices")
        
        print("\n📄 Run with --report option to generate detailed report.")


def main():
    parser = argparse.ArgumentParser(
        description="Analyze Elasticsearch ISM policy JSON files",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python ism_policy_analyzer.py policy.json
  python ism_policy_analyzer.py policy.json --report analysis_report.md
  python ism_policy_analyzer.py policy.json --report analysis_report.md --recommendations recommendations.md
  python ism_policy_analyzer.py policy.json --summary --recommendations rec.md
        """
    )
    
    parser.add_argument('file_path', help='Path to the ISM policy JSON file')
    parser.add_argument('--index-size-csv', help='Path to index_size.csv file for index sizes')
    parser.add_argument('--report', '-r', help='Generate detailed report and save to file')
    parser.add_argument('--recommendations', '--rec', help='Generate recommendations and save to file')
    parser.add_argument('--summary', '-s', action='store_true', help='Print summary to console')

    args = parser.parse_args()

    if not os.path.exists(args.file_path):
        print(f"❌ Error: File '{args.file_path}' does not exist.")
        sys.exit(1)

    # Initialize analyzer with index size CSV if provided
    analyzer = ISMPolicyAnalyzer(args.file_path, args.index_size_csv)

    # Load data
    if not analyzer.load_data():
        sys.exit(1)

    # Print summary if requested or no other output specified
    if args.summary or (not args.report and not args.recommendations):
        analyzer.print_summary()

    # Generate report if requested
    if args.report:
        print(f"\n📝 Generating detailed report...")
        report = analyzer.generate_report(args.report)
        if not args.summary:
            print("✅ Report generated!")

    # Generate recommendations if requested
    if args.recommendations:
        print(f"\n🔧 Generating recommendations...")
        recommendations = analyzer.generate_recommendations(args.recommendations)
        if not args.summary:
            print("✅ Recommendations generated!")

    if not args.summary and (args.report or args.recommendations):
        print("✅ Analysis complete!")


if __name__ == "__main__":
    main()
