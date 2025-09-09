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

    // Calculate base tax
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

    // Section 87A rebate
    if (taxableIncome <= 1200000) {
        return 0;
    }

    // Calculate surcharge
    let surchargeRate;
    if (taxableIncome > 50000000) {       // > 5 Cr
        surchargeRate = 0.25;
    } else if (taxableIncome > 20000000) { // > 2 Cr
        surchargeRate = 0.25;
    } else if (taxableIncome > 10000000) { // > 1 Cr
        surchargeRate = 0.15;
    } else if (taxableIncome > 5000000) {  // > 50 L
        surchargeRate = 0.10;
    } else {
        surchargeRate = 0.0;
    }

    const taxWithSurcharge = tax * (1 + surchargeRate);

    // Add 4% cess
    return taxWithSurcharge * 1.04;
}

/**
 * Calculate take-home salary and all components
 * @param {number} income - Annual gross income
 * @param {number} basicDaPct - Basic + DA percentage of gross
 * @returns {Object} Detailed breakdown of salary components
 */
function calculateTakeHome(income, basicDaPct) {
    const standardDeduction = 75000;
    const taxableIncome = Math.max(0, income - standardDeduction);
    const tax = computeTax(taxableIncome);
    const postTaxAnnual = income - tax;

    // Calculate EPF deduction
    const basicDaAnnual = income * (basicDaPct / 100);
    const empfMonthly = (basicDaAnnual / 12) * 0.12;

    const takeHomeAnnual = postTaxAnnual - empfMonthly * 12;

    return {
        annualIncome: income,
        standardDeduction: standardDeduction,
        taxableIncome: taxableIncome,
        tax: tax,
        postTaxAnnual: postTaxAnnual,
        epfMonthly: empfMonthly,
        takeHomeMonthly: takeHomeAnnual / 12
    };
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

// Handle form submission
document.getElementById('salaryForm').addEventListener('submit', function(e) {
    e.preventDefault();
    
    const annualGross = parseFloat(document.getElementById('annualGross').value);
    const basicDaPct = parseFloat(document.getElementById('basicDaPct').value);

    const result = calculateTakeHome(annualGross, basicDaPct);

    // Update result table
    document.getElementById('grossIncome').textContent = formatCurrency(result.annualIncome);
    document.getElementById('standardDeduction').textContent = formatCurrency(result.standardDeduction);
    document.getElementById('taxableIncome').textContent = formatCurrency(result.taxableIncome);
    document.getElementById('totalTax').textContent = formatCurrency(result.tax);
    document.getElementById('postTaxAnnual').textContent = formatCurrency(result.postTaxAnnual);
    document.getElementById('monthlyEpf').textContent = formatCurrency(result.epfMonthly);
    document.getElementById('monthlyTakeHome').textContent = formatCurrency(result.takeHomeMonthly);
    
    document.getElementById('result').style.display = 'block';
});
