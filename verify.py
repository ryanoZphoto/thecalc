def calculate_monthly_payment(principal: float, annual_rate: float, years: int) -> float:
    """Calculate the monthly payment for a mortgage."""
    monthly_rate = annual_rate / 12
    num_payments = years * 12
    
    return principal * (monthly_rate * (1 + monthly_rate)**num_payments) / \
           ((1 + monthly_rate)**num_payments - 1)

def calculate_loan_balance(principal: float, annual_rate: float, years_elapsed: int) -> float:
    """Calculate remaining balance after years elapsed."""
    monthly_rate = annual_rate / 12
    monthly_payment = calculate_monthly_payment(principal, annual_rate, 30)
    
    remaining_balance = principal
    months_elapsed = years_elapsed * 12
    
    for _ in range(months_elapsed):
        interest = remaining_balance * monthly_rate
        principal_paid = monthly_payment - interest
        remaining_balance -= principal_paid
    
    return remaining_balance

if __name__ == "__main__":
    # Current mortgage verification
    original_loan = 190000
    rate = 0.03
    years_elapsed = 4

    monthly_payment = calculate_monthly_payment(original_loan, rate, 30)
    current_balance = calculate_loan_balance(original_loan, rate, years_elapsed)

    print("\nCurrent Mortgage Verification:")
    print(f"Original Loan Amount: ${original_loan:,.2f}")
    print(f"Monthly Payment: ${monthly_payment:.2f}")
    print(f"Current Balance after {years_elapsed} years: ${current_balance:,.2f}")

    # New loan verification
    sale_price = 420000
    down_payment = 50000
    new_rate = 0.015
    balloon_years = 11

    loan_amount = sale_price - down_payment
    new_monthly = calculate_monthly_payment(loan_amount, new_rate, 30)

    # Calculate balloon payment
    remaining_balance = loan_amount
    for _ in range(balloon_years * 12):
        interest = remaining_balance * (new_rate / 12)
        principal_paid = new_monthly - interest
        remaining_balance -= principal_paid

    total_payments = new_monthly * (balloon_years * 12)

    print("\nNew Loan Verification:")
    print(f"Loan Amount: ${loan_amount:,.2f}")
    print(f"Monthly Payment: ${new_monthly:.2f}")
    print(f"Balloon Payment after {balloon_years} years: ${remaining_balance:,.2f}")
    print(f"Total Payments Made: ${total_payments:,.2f}")
    print(f"Total Cost: ${total_payments + down_payment + remaining_balance:,.2f}") 