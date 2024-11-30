from calculator.core.calc import Calculator


def test_mortgage_calculation():
    """Test basic mortgage calculation"""
    # Test case 1: Standard mortgage
    result1 = Calculator.calculate_monthly_payment(
        principal=200000,  # $200,000 loan
        rate=0.05,        # 5% interest
        years=30          # 30-year term
    )
    print(f"Standard Mortgage Payment: ${result1:.2f}")

    # Test case 2: Seller financing
    result2 = Calculator.calculate_monthly_payment(
        principal=420000,  # $420,000 loan
        rate=0.015,       # 1.5% interest
        years=30          # 30-year term
    )
    print(f"Seller Financing Payment: ${result2:.2f}")

if __name__ == "__main__":
    test_mortgage_calculation() 