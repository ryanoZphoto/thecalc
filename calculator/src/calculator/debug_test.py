from calculator.core.calc import Calculator

def test_mortgage_calculation():
    # Test case for monthly payment calculation
    result = Calculator.calculate_monthly_payment(
        principal=200000,  # $200,000 loan
        rate=0.05,        # 5% interest
        years=30          # 30-year term
    )
    print(f"Monthly payment: ${result:.2f}")

if __name__ == "__main__":
    test_mortgage_calculation() 