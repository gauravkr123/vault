/**
 * Compute income tax with slabs, surcharge and cess (FY 2025-26, New Regime).
 * @param {number} taxableIncome - Annual taxable income after standard deduction
 * @returns {number} Total tax including surcharge and cess
 */
function computeTax(taxableIncome) {
    // Tax slabs for FY 2025-26 (New Regime)
    const slabs = [
        [400000, 0.00],  // 0 to 4L: 0%
        [800000, 0.05],  // 4L to 8L: 5%
        [1200000, 0.10], // 8L to 12L: 10%
        [1600000, 0.15], // 12L to 16L: 15%
        [2000000, 0.20], // 16L to 20L: 20%
        [2400000, 0.25], // 20L to 24L: 25%
        [Infinity, 0.30] // Above 24L: 30%
    ];

    let tax = 0;
    let prev = 0;
    
    for (const [cap, rate] of slabs) {
        if (taxableIncome > prev) {
            const taxableChunk = Math.min(taxableIncome, cap) - prev;
            tax += taxableChunk * rate;
            prev = cap;
        } else {
            break;
        }
    }

    if (taxableIncome <= 1200000) {
        return 0;
    }

    let surchargeRate;
    if (taxableIncome > 50000000) {
        surchargeRate = 0.25;
    } else if (taxableIncome > 20000000) {
        surchargeRate = 0.25;
    } else if (taxableIncome > 10000000) {
        surchargeRate = 0.15;
    } else if (taxableIncome > 5000000) {
        surchargeRate = 0.10;
    } else {
        surchargeRate = 0.0;
    }

    return tax * (1 + surchargeRate) * 1.04;
}

/**
 * Calculate monthly take-home salary from annual gross income
 * @param {number} income - Annual gross income
 * @param {number} basicDaPct - Basic + DA percentage of gross
 * @returns {Object} Detailed breakdown of salary components
 */
function calculateTakeHome(income, basicDaPct) {
    const standardDeduction = 75000;
    const taxableIncome = Math.max(0, income - standardDeduction);
    const tax = computeTax(taxableIncome);

    const postTaxAnnual = income - tax;

    const basicDaAnnual = income * (basicDaPct / 100);
    const empfMonthly = (basicDaAnnual / 12) * 0.12;

    const takeHomeAnnual = postTaxAnnual - empfMonthly * 12;
    
    return {
        annualGross: income,
        monthlyGross: income / 12,
        annualTax: tax,
        monthlyTax: tax / 12,
        monthlyEpf: empfMonthly,
        monthlyTakeHome: takeHomeAnnual / 12
    };
}

/**
 * Estimate annual gross income needed for desired monthly take-home
 * @param {number} targetMonthly - Desired monthly take-home salary
 * @param {number} basicDaPct - Basic + DA percentage of gross
 * @returns {number} Estimated annual gross income
 */
function estimateGrossIncome(targetMonthly, basicDaPct) {
    let low = 100000;  // 1L
    let high = 100000000;  // 10Cr

    for (let i = 0; i < 100; i++) {
        const mid = (low + high) / 2;
        const result = calculateTakeHome(mid, basicDaPct);

        if (result.monthlyTakeHome < targetMonthly) {
            low = mid;
        } else {
            high = mid;
        }
    }

    return Math.round(low * 100) / 100;
}

/**
 * Format currency in Indian format with ₹ symbol
 * @param {number} amount - Amount to format
 * @returns {string} Formatted currency string
 */
function formatCurrency(amount) {
    return new Intl.NumberFormat('en-IN', {
        style: 'currency',
        currency: 'INR',
        maximumFractionDigits: 0
    }).format(amount);
}

/**
 * Update the result table with calculation results
 * @param {Object} result - Calculation results
 */
function updateResultTable(result) {
    document.getElementById('grossIncome').textContent = formatCurrency(result.annualGross);
    document.getElementById('monthlyGross').textContent = formatCurrency(result.monthlyGross);
    document.getElementById('annualTax').textContent = formatCurrency(result.annualTax);
    document.getElementById('monthlyTax').textContent = formatCurrency(result.monthlyTax);
    document.getElementById('monthlyEpf').textContent = formatCurrency(result.monthlyEpf);
    document.getElementById('monthlyTakeHome').textContent = formatCurrency(result.monthlyTakeHome);
    
    document.getElementById('result').style.display = 'block';
}

// Event handler for Gross → Take-home calculator
document.getElementById('grossForm').addEventListener('submit', function(e) {
    e.preventDefault();
    
    const annualGross = parseFloat(document.getElementById('annualGross').value);
    const basicDaPct = parseFloat(document.getElementById('basicDaPctGross').value);

    const result = calculateTakeHome(annualGross, basicDaPct);
    updateResultTable(result);
});

// Event handler for Take-home → Gross calculator
document.getElementById('takeHomeForm').addEventListener('submit', function(e) {
    e.preventDefault();
    
    const targetMonthly = parseFloat(document.getElementById('targetMonthly').value);
    const basicDaPct = parseFloat(document.getElementById('basicDaPct').value);

    const estimatedAnnualIncome = estimateGrossIncome(targetMonthly, basicDaPct);
    const result = calculateTakeHome(estimatedAnnualIncome, basicDaPct);
    updateResultTable(result);
});
