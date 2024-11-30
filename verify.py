"""Verification module for calculator functionality."""

from typing import Tuple


def calculate_monthly_payment(
    principal: float,
    annual_rate: float,
    years: int
) -> float:
    """
    Calculate the monthly payment for a mortgage.
    
    Args:
        principal: Loan amount
        annual_rate: Annual interest rate as decimal
        years: Loan term in years
        
    Returns:
        Monthly payment amount
    """
    monthly_rate = annual_rate / 12
    num_payments = years * 12
    
    numerator = principal * monthly_rate * (1 + monthly_rate)**num_payments
    denominator = (1 + monthly_rate)**num_payments - 1
    return numerator / denominator


def calculate_loan_balance(
    principal: float,
    annual_rate: float,
    years_elapsed: int
) -> float:
    """
    Calculate remaining balance after years elapsed.
    
    Args:
        principal: Original loan amount
        annual_rate: Annual interest rate as decimal
        years_elapsed: Number of years elapsed
        
    Returns:
        Remaining loan balance
    """
    monthly_rate = annual_rate / 12
    monthly_payment = calculate_monthly_payment(principal, annual_rate, 30)
    
    remaining_balance = principal
    months_elapsed = years_elapsed * 12
    
    for _ in range(months_elapsed):
        interest = remaining_balance * monthly_rate
        principal_paid = monthly_payment - interest
        remaining_balance -= principal_paid
    
    return remaining_balance


def verify_current_mortgage() -> Tuple[float, float, float]:
    """
    Verify current mortgage calculations.
    
    Returns:
        Tuple containing (original loan, monthly payment, current balance)
    """
    original_loan = 190000
    rate = 0.03
    years_elapsed = 4

    monthly_payment = calculate_monthly_payment(original_loan, rate, 30)
    current_balance = calculate_loan_balance(original_loan, rate, years_elapsed)
    
    return original_loan, monthly_payment, current_balance


def verify_new_loan() -> Tuple[float, float, float, float]:
    """
    Verify new loan calculations.
    
    Returns:
        Tuple containing (loan amount, monthly payment, balloon payment, total cost)
    """
    sale_price = 420000
    down_payment = 50000
    new_rate = 0.015
    balloon_years = 11

    loan_amount = sale_price - down_payment
    monthly_payment = calculate_monthly_payment(loan_amount, new_rate, 30)

    remaining_balance = loan_amount
    for _ in range(balloon_years * 12):
        interest = remaining_balance * (new_rate / 12)
        principal_paid = monthly_payment - interest
        remaining_balance -= principal_paid

    total_payments = monthly_payment * (balloon_years * 12)
    total_cost = total_payments + down_payment + remaining_balance
    
    return loan_amount, monthly_payment, remaining_balance, total_cost


def main():
    """Run verification tests and display results."""
    # Verify current mortgage
    orig_loan, monthly_pmt, curr_balance = verify_current_mortgage()
    
    print("\nCurrent Mortgage Verification:")
    print(f"Original Loan Amount: ${orig_loan:,.2f}")
    print(f"Monthly Payment: ${monthly_pmt:.2f}")
    print(f"Current Balance after 4 years: ${curr_balance:,.2f}")

    # Verify new loan
    loan_amt, new_pmt, balloon_pmt, total = verify_new_loan()
    
    print("\nNew Loan Verification:")
    print(f"Loan Amount: ${loan_amt:,.2f}")
    print(f"Monthly Payment: ${new_pmt:.2f}")
    print(f"Balloon Payment after 11 years: ${balloon_pmt:,.2f}")
    print(f"Total Cost: ${total:,.2f}")


if __name__ == "__main__":
    main()