# Usage: python3 schema_merge_validation_simple.py

import json
import sys
import os
from datetime import datetime

def merge_dicts_original(dict1, dict2):
    """Original merge logic from the script"""
    for k in dict2.keys():
        if k not in dict1.keys():
            dict1[k] = dict2[k]
        if k in dict1.keys() and type(dict1[k]) is dict:
            merge_dicts_original(dict1[k], dict2[k])
    return dict1

def merge_dicts_strict(dict1, dict2, path="", collect_conflicts=False, conflicts_list=None):
    """Strict validation merge logic - now collects all conflicts instead of failing on first"""
    if conflicts_list is None:
        conflicts_list = []
    
    for k in dict2.keys():
        current_path = f"{path}.{k}" if path else k
        
        if k not in dict1:
            # Key doesn't exist in global schema - this is fine, we add it
            dict1[k] = dict2[k]
        elif isinstance(dict1[k], dict) and isinstance(dict2[k], dict):
            # Both are dictionaries, recurse deeper
            merge_dicts_strict(dict1[k], dict2[k], current_path, collect_conflicts, conflicts_list)
        elif dict1[k] != dict2[k]:
            # Conflict detected - collect it instead of failing
            conflict_msg = f"Schema conflict at '{current_path}': Global={dict1[k]} vs Event={dict2[k]}"
            conflicts_list.append(conflict_msg)
            
            if not collect_conflicts:
                # Old behavior - fail immediately
                raise ValueError(conflict_msg)
    
    return dict1, conflicts_list

def compare_schema_original(global_schema, event_schema):
    """Original compare_schema logic"""
    global_schema_json = json.loads(global_schema)
    event_schema_json = json.loads(event_schema)
    global_schema_json["properties"] = merge_dicts_original(global_schema_json["properties"], event_schema_json["properties"])
    return global_schema_json

def compare_schema_strict(global_schema, event_schema, collect_conflicts=False):
    """Strict validation compare_schema logic - now can collect all conflicts"""
    global_schema_json = json.loads(global_schema)
    event_schema_json = json.loads(event_schema)
    
    if collect_conflicts:
        conflicts_list = []
        global_schema_json["properties"], conflicts_list = merge_dicts_strict(
            global_schema_json["properties"], 
            event_schema_json["properties"], 
            collect_conflicts=collect_conflicts,
            conflicts_list=conflicts_list
        )
        return global_schema_json, conflicts_list
    else:
        global_schema_json["properties"], _ = merge_dicts_strict(global_schema_json["properties"], event_schema_json["properties"])
        return global_schema_json

def load_schema_from_file(file_path):
    """Load schema from JSON file"""
    try:
        with open(file_path, 'r') as f:
            schema_dict = json.load(f)
            return json.dumps(schema_dict)
    except FileNotFoundError:
        print(f"❌ Error: Schema file not found: {file_path}")
        return None
    except json.JSONDecodeError as e:
        print(f"❌ Error: Invalid JSON in file {file_path}: {e}")
        return None

def run_test(global_file, event_file, expected_to_fail=False, fail_on_conflict=False, test_name="Schema Merge Test"):
    """Run test with two schema files"""
    print(f"{'='*60}")
    print(f"TEST: {test_name}")
    print(f"Global Schema: {global_file}")
    print(f"Event Schema: {event_file}")
    print(f"Expected to Fail: {expected_to_fail}")
    print(f"Fail on Conflict: {fail_on_conflict}")
    print(f"{'='*60}")
    
    # Load schemas from files
    global_schema = load_schema_from_file(global_file)
    event_schema = load_schema_from_file(event_file)
    
    if not global_schema or not event_schema:
        print("❌ Failed to load schema files. Test aborted.")
        return
    
    print("\n📄 GLOBAL SCHEMA:")
    print(json.dumps(json.loads(global_schema), indent=2))
    print("\n📄 EVENT SCHEMA:")
    print(json.dumps(json.loads(event_schema), indent=2))
    
    # Test original approach
    print(f"\n{'🔄 ORIGINAL APPROACH':^60}")
    print("-" * 60)
    try:
        global_copy = json.loads(global_schema)  # Create copy to avoid mutation
        event_copy = json.loads(event_schema)
        global_copy["properties"] = merge_dicts_original(global_copy["properties"], event_copy["properties"])
        print("✅ SUCCESS - Merged Result:")
        print(json.dumps(global_copy, indent=2))
    except Exception as e:
        print(f"❌ ERROR: {e}")
    
    # Test strict approach
    print(f"\n{'⚡ STRICT APPROACH':^60}")
    print("-" * 60)
    try:
        result_strict = compare_schema_strict(global_schema, event_schema)
        print("✅ SUCCESS - Merged Result:")
        print(json.dumps(result_strict, indent=2))
        if expected_to_fail:
            print("\n⚠️  WARNING: Expected this to fail but it succeeded!")
            print("    Check if your test setup is correct.")
    except Exception as e:
        print(f"🚫 CONFLICT DETECTED: {e}")
        if not expected_to_fail:
            print("\n⚠️  WARNING: Unexpected conflict detected!")
            print("    You may want to set expected_to_fail=True for this test.")
        
        # Exit the script immediately if fail_on_conflict is True
        if fail_on_conflict:
            print(f"\n💥 SCRIPT TERMINATING due to conflict (fail_on_conflict=True)")
            sys.exit(1)
    
    print(f"\n{'='*60}")

def read_event_list(list_file_path):
    """Read comma-separated list of event names from file"""
    try:
        with open(list_file_path, 'r') as f:
            content = f.read().strip()
            # Split by comma and clean up whitespace
            event_names = [name.strip() for name in content.split(',') if name.strip()]
            return event_names
    except FileNotFoundError:
        print(f"❌ Error: Event list file not found: {list_file_path}")
        return None
    except Exception as e:
        print(f"❌ Error reading event list file: {e}")
        return None

def validate_single_event(global_schema, event_file_path, events_folder, ignore_required=False):
    """Validate a single event schema against global schema - now collects all conflicts"""
    full_event_path = os.path.join(events_folder, event_file_path)
    
    # Load event schema
    event_schema = load_schema_from_file(full_event_path)
    if not event_schema:
        return {
            'file': event_file_path,
            'status': 'ERROR',
            'error': f'Failed to load event schema from {full_event_path}',
            'conflicts': []
        }
    
    # Remove required fields if requested
    if ignore_required:
        try:
            global_schema_dict = json.loads(global_schema)
            event_schema_dict = json.loads(event_schema)
            
            global_schema_dict = remove_required_fields(global_schema_dict, ignore_required)
            event_schema_dict = remove_required_fields(event_schema_dict, ignore_required)
            
            global_schema = json.dumps(global_schema_dict)
            event_schema = json.dumps(event_schema_dict)
        except Exception as e:
            return {
                'file': event_file_path,
                'status': 'ERROR',
                'error': f'Error processing required fields: {str(e)}',
                'conflicts': []
            }
    
    # Test for conflicts - now collect all conflicts instead of failing on first
    try:
        merged_schema, conflicts_list = compare_schema_strict(global_schema, event_schema, collect_conflicts=True)
        
        if conflicts_list:
            return {
                'file': event_file_path,
                'status': 'CONFLICT',
                'error': f'Found {len(conflicts_list)} conflict(s)',
                'conflicts': conflicts_list
            }
        else:
            return {
                'file': event_file_path,
                'status': 'SUCCESS',
                'error': None,
                'conflicts': []
            }
            
    except Exception as e:
        return {
            'file': event_file_path,
            'status': 'ERROR',
            'error': f'Unexpected error during validation: {str(e)}',
            'conflicts': []
        }

def batch_validate_events(global_file, events_folder, event_list_file, output_file, ignore_required=False):
    """Validate multiple event schemas and generate conflict report"""
    print("=" * 80)
    print("BATCH SCHEMA VALIDATION")
    print("=" * 80)
    print(f"Global Schema: {global_file}")
    print(f"Events Folder: {events_folder}")
    print(f"Event List File: {event_list_file}")
    print(f"Output Report: {output_file}")
    print(f"Ignore Required Fields: {ignore_required}")
    print("=" * 80)
    
    # Load global schema
    global_schema = load_schema_from_file(global_file)
    if not global_schema:
        print("❌ Failed to load global schema. Aborting.")
        return
    
    # Read event list
    event_names = read_event_list(event_list_file)
    if not event_names:
        print("❌ Failed to read event list. Aborting.")
        return
    
    print(f"\n📋 Found {len(event_names)} events to validate:")
    for name in event_names:
        print(f"   - {name}")
    
    # Validate each event
    results = []
    total_conflicts = 0
    
    print(f"\n🔄 Validating events...")
    for event_name in event_names:
        # Assume event files have .json extension if not provided
        if not event_name.endswith('.json'):
            event_file = f"{event_name}.json"
        else:
            event_file = event_name
            
        print(f"   Validating {event_name}...", end=" ")
        
        result = validate_single_event(global_schema, event_file, events_folder, ignore_required)
        results.append(result)
        
        if result['status'] == 'CONFLICT':
            conflict_count = len(result['conflicts'])
            total_conflicts += conflict_count
            print(f"🚫 {conflict_count} conflict(s)")
        elif result['status'] == 'SUCCESS':
            print("✅ OK")
        else:
            print(f"❌ {result['error']}")
    
    # Generate report
    generate_conflict_report(results, output_file, global_file, events_folder, total_conflicts, ignore_required)
    
    # Summary
    success_count = len([r for r in results if r['status'] == 'SUCCESS'])
    error_count = len([r for r in results if r['status'] == 'ERROR'])
    conflict_files = len([r for r in results if r['status'] == 'CONFLICT'])
    
    print(f"\n📊 VALIDATION SUMMARY:")
    print(f"   Total Events: {len(results)}")
    print(f"   ✅ Success: {success_count}")
    print(f"   🚫 Files with Conflicts: {conflict_files}")
    print(f"   🔍 Total Conflicts Found: {total_conflicts}")
    print(f"   ❌ Errors: {error_count}")
    print(f"   📄 Report saved to: {output_file}")

def generate_conflict_report(results, output_file, global_file, events_folder, total_conflicts, ignore_required=False):
    """Generate detailed conflict report"""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    with open(output_file, 'w') as f:
        f.write("=" * 80 + "\n")
        f.write("SCHEMA VALIDATION CONFLICT REPORT\n")
        f.write("=" * 80 + "\n")
        f.write(f"Generated: {timestamp}\n")
        f.write(f"Global Schema: {global_file}\n")
        f.write(f"Events Folder: {events_folder}\n")
        f.write(f"Total Events Processed: {len(results)}\n")
        f.write(f"Total Conflicts Found: {total_conflicts}\n")
        f.write(f"Ignore Required Fields: {ignore_required}\n")
        f.write("=" * 80 + "\n\n")
        
        # Group results by status
        conflicts = [r for r in results if r['status'] == 'CONFLICT']
        successes = [r for r in results if r['status'] == 'SUCCESS']
        errors = [r for r in results if r['status'] == 'ERROR']
        
        # Write conflicts section
        if conflicts:
            f.write("🚫 CONFLICTS DETECTED:\n")
            f.write("-" * 40 + "\n\n")
            
            for result in conflicts:
                f.write(f"File: {result['file']}\n")
                f.write(f"Status: {result['status']}\n")
                f.write(f"Total Conflicts: {len(result['conflicts'])}\n")
                f.write("Conflicts:\n")
                for i, conflict in enumerate(result['conflicts'], 1):
                    f.write(f"  {i}. {conflict}\n")
                f.write("-" * 40 + "\n\n")
        
        # Write errors section
        if errors:
            f.write("❌ ERRORS ENCOUNTERED:\n")
            f.write("-" * 40 + "\n\n")
            
            for result in errors:
                f.write(f"File: {result['file']}\n")
                f.write(f"Status: {result['status']}\n")
                f.write(f"Error: {result['error']}\n")
                f.write("-" * 40 + "\n\n")
        
        # Write successes section
        if successes:
            f.write("✅ SUCCESSFUL VALIDATIONS:\n")
            f.write("-" * 40 + "\n")
            for result in successes:
                f.write(f"File: {result['file']} - No conflicts detected\n")
        
        f.write(f"\n" + "=" * 80 + "\n")
        f.write("END OF REPORT\n")
        f.write("=" * 80 + "\n")

def remove_required_fields(schema_dict, ignore_required=False):
    """Remove 'required' fields from schema if ignore_required is True"""
    if not ignore_required:
        return schema_dict
    
    # Create a deep copy to avoid mutating the original
    import copy
    schema_copy = copy.deepcopy(schema_dict)
    
    def remove_required_recursive(obj):
        if isinstance(obj, dict):
            # Remove 'required' key if it exists
            if 'required' in obj:
                del obj['required']
            # Recursively process nested objects
            for key, value in obj.items():
                remove_required_recursive(value)
        elif isinstance(obj, list):
            # Process list items
            for item in obj:
                remove_required_recursive(item)
    
    remove_required_recursive(schema_copy)
    return schema_copy

def construct_global_schema_from_events(events_folder, event_names, ignore_required=False):
    """Construct a global schema by merging all event schemas"""
    print(f"\n🏗️  Constructing global schema from {len(event_names)} events...")
    
    global_schema = {
        "type": "object",
        "properties": {}
    }
    
    construction_log = []
    
    for i, event_name in enumerate(event_names, 1):
        # Ensure .json extension
        if not event_name.endswith('.json'):
            event_file = f"{event_name}.json"
        else:
            event_file = event_name
            
        full_event_path = os.path.join(events_folder, event_file)
        print(f"   [{i}/{len(event_names)}] Processing {event_name}...", end=" ")
        
        # Load event schema
        event_schema = load_schema_from_file(full_event_path)
        if not event_schema:
            print(f"❌ Failed to load")
            construction_log.append(f"ERROR: Failed to load {event_file}")
            continue
            
        try:
            event_schema_dict = json.loads(event_schema)
            
            # Remove required fields if requested
            if ignore_required:
                event_schema_dict = remove_required_fields(event_schema_dict, ignore_required)
            
            # Extract properties if they exist
            if "properties" in event_schema_dict:
                # Merge properties into global schema
                global_schema["properties"] = merge_dicts_original(
                    global_schema["properties"], 
                    event_schema_dict["properties"]
                )
                print(f"✅ Added {len(event_schema_dict['properties'])} properties")
                construction_log.append(f"SUCCESS: Merged {len(event_schema_dict['properties'])} properties from {event_file}")
            else:
                print("⚠️  No properties found")
                construction_log.append(f"WARNING: No properties found in {event_file}")
                
        except Exception as e:
            print(f"❌ Error: {str(e)}")
            construction_log.append(f"ERROR: Failed to process {event_file}: {str(e)}")
    
    print(f"\n🎯 Global schema constructed with {len(global_schema['properties'])} total properties")
    return json.dumps(global_schema), construction_log

def validate_event_against_constructed_schema(constructed_global_schema, event_file_path, events_folder, ignore_required=False):
    """Validate a single event schema against the constructed global schema"""
    full_event_path = os.path.join(events_folder, event_file_path)
    
    # Load event schema
    event_schema = load_schema_from_file(full_event_path)
    if not event_schema:
        return {
            'file': event_file_path,
            'status': 'ERROR',
            'error': f'Failed to load event schema from {full_event_path}',
            'conflicts': []
        }
    
    # Remove required fields if requested
    if ignore_required:
        try:
            global_schema_dict = json.loads(constructed_global_schema)
            event_schema_dict = json.loads(event_schema)
            
            global_schema_dict = remove_required_fields(global_schema_dict, ignore_required)
            event_schema_dict = remove_required_fields(event_schema_dict, ignore_required)
            
            constructed_global_schema = json.dumps(global_schema_dict)
            event_schema = json.dumps(event_schema_dict)
        except Exception as e:
            return {
                'file': event_file_path,
                'status': 'ERROR',
                'error': f'Error processing required fields: {str(e)}',
                'conflicts': []
            }
    
    # Test for conflicts - collect all conflicts instead of failing on first
    try:
        merged_schema, conflicts_list = compare_schema_strict(constructed_global_schema, event_schema, collect_conflicts=True)
        
        if conflicts_list:
            return {
                'file': event_file_path,
                'status': 'CONFLICT',
                'error': f'Found {len(conflicts_list)} conflict(s)',
                'conflicts': conflicts_list
            }
        else:
            return {
                'file': event_file_path,
                'status': 'SUCCESS',
                'error': None,
                'conflicts': []
            }
            
    except Exception as e:
        return {
            'file': event_file_path,
            'status': 'ERROR',
            'error': f'Unexpected error during validation: {str(e)}',
            'conflicts': []
        }

if __name__ == "__main__":
    print("Schema Merge Validation Test - Batch Processing Version")
    print("=" * 80)
    
    # ===================================
    # CONFIGURE YOUR PATHS HERE
    # ===================================
    
    # Set your file paths here
    global_file = "/Path/to/global_schema.json"
    events_folder = "/Path/to/folder/default-schema"  # 👈 Folder containing event JSON files
    event_list_file = "/Path/to/events_list.txt"  # 👈 File with comma-separated event names
    output_report_file = "/Path/to/schema_validation_report.txt"  # 👈 Output report file
    
    # ===================================
    # CONFIGURE VALIDATION OPTIONS HERE
    # ===================================
    
    # Set to True to ignore 'required' fields during schema validation

    ignore_required_fields = True  # 👈 Set to True to skip validation of 'required' sections
    
    # ===================================
    # BATCH VALIDATION
    # ===================================
    
    # Run batch validation
    batch_validate_events(
        global_file=global_file,
        events_folder=events_folder,
        event_list_file=event_list_file,
        output_file=output_report_file,
        ignore_required=ignore_required_fields
    )    
    print(f"\n{'📋 CONFIGURATION GUIDE':^80}")
    print("=" * 80)
    print("To set up batch validation, configure the paths above:")
    print("")
    print("📁 REQUIRED PATHS:")
    print("   global_file = 'path/to/your/global_schema.json'")
    print("   events_folder = 'path/to/folder/containing/event/json/files'")
    print("   event_list_file = 'path/to/file/with/comma-separated/event/names'")
    print("   output_report_file = 'path/to/output/report.txt'")
    print("")
    print("⚙️  VALIDATION OPTIONS:")
    print("   ignore_required_fields = False  # Set to True to skip 'required' field validation")
    print("")
    print("📝 EVENT LIST FILE FORMAT:")
    print("   event1, event2, event3")
    print("   or")
    print("   event1.json, event2.json, event3.json")
    print("")
    print("📊 OUTPUT REPORT:")
    print("   - Lists all conflicts file by file")
    print("   - Shows successful validations")
    print("   - Reports any file loading errors")
    print("   - Includes summary statistics")
    print("")
    print("💡 TIP: The script will automatically add '.json' extension")
    print("   if not present in the event list file")