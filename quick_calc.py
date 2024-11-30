def calculate_monthly_payment(principal, annual_rate, years):
    """
    Calculate monthly mortgage payment
    principal: loan amount
    annual_rate: annual interest rate (as decimal, e.g., 0.05 for 5%)
    years: loan term in years
    """
    # Convert annual rate to monthly
    monthly_rate = annual_rate / 12
    
    # Total number of payments
    n_payments = years * 12
    
    # Handle zero interest case
    if annual_rate == 0:
        return principal / n_payments
        
    # Calculate monthly payment using amortization formula
    monthly_payment = principal * (
        (monthly_rate * (1 + monthly_rate)**n_payments) / 
        ((1 + monthly_rate)**n_payments - 1)
    )
    
    return round(monthly_payment, 2)

# Example usage
if __name__ == "__main__":
    # Example: $300,000 loan at 6.5% for 30 years
    loan_amount = 300000
    interest_rate = 0.065  # 6.5%
    term = 30
    
    payment = calculate_monthly_payment(loan_amount, interest_rate, term)
    print(f"\nLoan Amount: ${loan_amount:,}")
    print(f"Interest Rate: {interest_rate*100}%")
    print(f"Term: {term} years")
    print(f"Monthly Payment: ${payment:,.2f}")