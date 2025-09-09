def compute_tax(taxable_income):
    slabs = [
        (400000, 0.00),
        (800000, 0.05),
        (1200000, 0.10),
        (1600000, 0.15),
        (2000000, 0.20),
        (2400000, 0.25),
        (float("inf"), 0.30)
    ]

    tax = 0
    prev = 0
    for cap, rate in slabs:
        if taxable_income > prev:
            taxable_chunk = min(taxable_income, cap) - prev
            tax += taxable_chunk * rate
            prev = cap
        else:
            break

    if taxable_income <= 1200000:
        return 0

    if taxable_income > 50000000:
        surcharge_rate = 0.25
    elif taxable_income > 20000000:
        surcharge_rate = 0.25
    elif taxable_income > 10000000:
        surcharge_rate = 0.15
    elif taxable_income > 5000000:
        surcharge_rate = 0.10
    else:
        surcharge_rate = 0.0

    return tax * (1 + surcharge_rate) * 1.04


def calculate_take_home_monthly(income, basic_da_pct):
    standard_deduction = 75000
    taxable_income = max(0, income - standard_deduction)
    tax = compute_tax(taxable_income)

    post_tax_annual = income - tax

    basic_da_annual = income * (basic_da_pct / 100)
    empf_monthly = (basic_da_annual / 12) * 0.12

    take_home_annual = post_tax_annual - empf_monthly * 12
    return take_home_annual / 12


def estimate_gross_income(target_monthly, basic_da_pct):
    low, high = 1_00_000, 10_00_00_000  # search space: 1L to 10Cr
    for _ in range(100):
        mid = (low + high) / 2
        calc_monthly = calculate_take_home_monthly(mid, basic_da_pct)

        if calc_monthly < target_monthly:
            low = mid
        else:
            high = mid

    return round(mid, 2)


if __name__ == "__main__":
    target_monthly = float(input("Enter your monthly in-hand salary (₹, after Tax & EPF): "))
    basic_da_pct = float(input("Enter percentage of Basic + DA in salary (e.g., 40): "))

    estimated_income = estimate_gross_income(target_monthly, basic_da_pct)
    print(f"\nEstimated Annual Gross Income: ₹{estimated_income:,.2f}")
