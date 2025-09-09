def compute_tax(taxable_income):
    """
    Compute income tax with slabs, surcharge and cess (FY 2025-26, New Regime).
    """
    # Tax slabs
    slabs = [
        (400000, 0.00),
        (800000, 0.05),
        (1200000, 0.10),
        (1600000, 0.15),
        (2000000, 0.20),
        (2400000, 0.25),
        (float("inf"), 0.30)
    ]

    # Base tax
    tax = 0
    prev = 0
    for cap, rate in slabs:
        if taxable_income > prev:
            taxable_chunk = min(taxable_income, cap) - prev
            tax += taxable_chunk * rate
            prev = cap
        else:
            break

    # Section 87A rebate
    if taxable_income <= 1200000:
        return 0

    # Surcharge
    if taxable_income > 50000000:   # > 5 Cr
        surcharge_rate = 0.25
    elif taxable_income > 20000000: # > 2 Cr
        surcharge_rate = 0.25
    elif taxable_income > 10000000: # > 1 Cr
        surcharge_rate = 0.15
    elif taxable_income > 5000000:  # > 50 L
        surcharge_rate = 0.10
    else:
        surcharge_rate = 0.0

    tax_with_surcharge = tax * (1 + surcharge_rate)

    # 4% cess
    return tax_with_surcharge * 1.04


def calculate_take_home(income, basic_da_pct):
    standard_deduction = 75000
    taxable_income = max(0, income - standard_deduction)

    tax = compute_tax(taxable_income)
    post_tax_annual = income - tax

    # EPF deduction
    basic_da_annual = income * (basic_da_pct / 100)
    empf_monthly = (basic_da_annual / 12) * 0.12

    take_home_annual = post_tax_annual - empf_monthly * 12
    take_home_monthly = take_home_annual / 12

    return {
        "annual_income": income,
        "tax": tax,
        "post_tax_annual": post_tax_annual,
        "epf_monthly": empf_monthly,
        "take_home_monthly": take_home_monthly
    }


if __name__ == "__main__":
    income = float(input("Enter your annual gross income (₹): "))
    basic_da_pct = float(input("Enter percentage of Basic + DA in salary (e.g., 40): "))

    result = calculate_take_home(income, basic_da_pct)
    print("\n=== Salary Breakdown ===")
    print(f"Annual Gross Income: ₹{result['annual_income']:,.2f}")
    print(f"Total Tax (incl. surcharge & cess): ₹{result['tax']:,.2f}")
    print(f"Post-Tax Annual Income: ₹{result['post_tax_annual']:,.2f}")
    print(f"Employee EPF Deduction (Monthly): ₹{result['epf_monthly']:,.2f}")
    print(f"Take-Home Monthly Salary: ₹{result['take_home_monthly']:,.2f}")
