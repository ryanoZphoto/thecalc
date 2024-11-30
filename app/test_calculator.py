from decimal import Decimal
from calculator import MortgageCalculator, LoanDetails

def test_real_world_scenario():
    """Test with real numbers a realtor might use"""
    
    # Setup calculator
    calc = MortgageCalculator()
    
    # Test Case: $400,000 house, 20% down, 6.5% interest, 30 years
    loan = LoanDetails(
        principal=Decimal('400000.00'),
        down_payment=Decimal('80000.00'),
        annual_rate=Decimal('0.065'),
        term_years=30,
        property_tax=Decimal('4800.00'),  # $4,800/year
        insurance=Decimal('1200.00')      # $1,200/year
    )
    
    # Calculate monthly payment
    result = calc.calculate_monthly_payment(loan)
    
    # Print detailed breakdown
    print("\nMonthly Payment Breakdown:")
    print(f"Principal & Interest: ${result['principal_and_interest']}")
    print(f"Property Tax: ${result['property_tax']}")
    print(f"Insurance: ${result['insurance']}")
    print(f"Total Payment: ${result['total_payment']}")
    
    # Get first few months of amortization schedule
    schedule = calc.generate_amortization_schedule(loan)[:3]
    
    print("\nFirst 3 Months Amortization:")
    for month in schedule:
        print(f"\nMonth {month['payment_number']}:")
        print(f"Principal Paid: ${month['principal_payment']}")
        print(f"Interest Paid: ${month['interest_payment']}")
        print(f"Remaining Balance: ${month['remaining_balance']}")

if __name__ == "__main__":
    test_real_world_scenario() 