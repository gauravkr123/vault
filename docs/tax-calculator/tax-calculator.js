function computeTax(taxableIncome) {
    const slabs = [
        [400000, 0.00],
        [800000, 0.05],
        [1200000, 0.10],
        [1600000, 0.15],
        [2000000, 0.20],
        [2400000, 0.25],
        [Infinity, 0.30]
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

function calculateTakeHomeMonthly(income, basicDaPct) {
    const standardDeduction = 75000;
    const taxableIncome = Math.max(0, income - standardDeduction);
    const tax = computeTax(taxableIncome);

    const postTaxAnnual = income - tax;

    const basicDaAnnual = income * (basicDaPct / 100);
    const empfMonthly = (basicDaAnnual / 12) * 0.12;

    const takeHomeAnnual = postTaxAnnual - empfMonthly * 12;
    return takeHomeAnnual / 12;
}

function estimateGrossIncome(targetMonthly, basicDaPct) {
    let low = 100000;  // 1L
    let high = 100000000;  // 10Cr

    for (let i = 0; i < 100; i++) {
        const mid = (low + high) / 2;
        const calcMonthly = calculateTakeHomeMonthly(mid, basicDaPct);

        if (calcMonthly < targetMonthly) {
            low = mid;
        } else {
            high = mid;
        }
    }

    return Math.round(low * 100) / 100;
}

function formatCurrency(amount) {
    return new Intl.NumberFormat('en-IN', {
        style: 'currency',
        currency: 'INR',
        maximumFractionDigits: 0
    }).format(amount);
}

document.getElementById('taxForm').addEventListener('submit', function(e) {
    e.preventDefault();
    
    const targetMonthly = parseFloat(document.getElementById('targetMonthly').value);
    const basicDaPct = parseFloat(document.getElementById('basicDaPct').value);

    const estimatedAnnualIncome = estimateGrossIncome(targetMonthly, basicDaPct);
    const monthlyGross = estimatedAnnualIncome / 12;
    const annualTax = computeTax(Math.max(0, estimatedAnnualIncome - 75000));
    const monthlyTax = annualTax / 12;

    document.getElementById('grossIncome').textContent = formatCurrency(estimatedAnnualIncome);
    document.getElementById('monthlyGross').textContent = formatCurrency(monthlyGross);
    document.getElementById('annualTax').textContent = formatCurrency(annualTax);
    document.getElementById('monthlyTax').textContent = formatCurrency(monthlyTax);
    
    document.getElementById('result').style.display = 'block';
});
