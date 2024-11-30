import unittest
from web_version.app import Calculator

class TestCalculator(unittest.TestCase):
    def setUp(self):
        """Initialize test cases with known values"""
        self.test_cases = [
            {
                # Standard 30-year mortgage
                'principal': 300000,
                'rate': 0.06,  # 6%
                'years': 30,
                'expected_payment': 1798.65
            },
            {
                # 15-year mortgage
                'principal': 250000,
                'rate': 0.045,  # 4.5%
                'years': 15,
                'expected_payment': 1912.48
            },
            {
                # Zero interest loan
                'principal': 100000,
                'rate': 0,
                'years': 30,
                'expected_payment': 277.78
            }
        ]

    def test_monthly_payments(self):
        """Test monthly payment calculations"""
        for case in self.test_cases:
            payment = Calculator.calculate_monthly_payment(
                case['principal'],
                case['rate'],
                case['years']
            )
            self.assertAlmostEqual(payment, case['expected_payment'], places=2)

    def test_loan_balance(self):
        """Test remaining balance calculations"""
        # Test case: $300,000 loan at 6% after 5 years
        balance = Calculator.calculate_loan_balance(300000, 0.06, 30, 5)
        expected_balance = 276147.21  # Verified with amortization tables
        self.assertAlmostEqual(balance, expected_balance, places=2)

    def test_seller_financing(self):
        """Test seller financing calculations"""
        data = {
            'original_price': 400000,
            'current_rate': 4.5,
            'original_term': 30,
            'years_remaining': 25,
            'sale_price': 450000,
            'down_payment': 50000,
            'new_rate': 6.0,
            'loan_term': 30,
            'balloon_years': 5
        }
        
        results = Calculator.calculate_seller_financing(data)
        self.assertIsNotNone(results)
        self.assertIn('current_mortgage', results)
        self.assertIn('new_financing', results)

    def test_investment_analysis(self):
        """Test investment property calculations"""
        data = {
            'purchase_price': 350000,
            'down_payment': 70000,
            'rate': 5.5,
            'monthly_rent': 2500,
            'property_tax': 4200,
            'insurance': 1800,
            'maintenance': 2,
            'vacancy': 5,
            'management': 8
        }
        
        results = Calculator.calculate_investment(data)
        self.assertIsNotNone(results)
        self.assertIn('monthly', results)
        self.assertIn('annual', results)
        self.assertIn('returns', results) 