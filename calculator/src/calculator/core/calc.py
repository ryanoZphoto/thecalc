"""Core calculator module providing calculation functionality."""

from typing import Dict, Any


class Calculator:
    """Core calculator functionality."""
    
    @staticmethod
    def calculate_monthly_payment(
        principal: float,
        rate: float,
        years: int
    ) -> float:
        """
        Calculate monthly mortgage payment.
        Calculate the monthly mortgage payment using the standard amortization formula.
        
        The formula used is:
        P * (r * (1 + r)^n) / ((1 + r)^n - 1)
        
        Where:
        P = Principal
        r = Monthly interest rate
        n = Total number of payments
        For 0% interest rate, uses simple division of principal by number of payments.
        
        Args:
            principal: Loan amount
            rate: Annual interest rate as decimal (e.g., 0.05 for 5%)
            years: Loan term in years
            
        Returns:
            Monthly payment amount
            
        Examples:
            >>> Calculator.calculate_monthly_payment(200000, 0.05, 30)
            1073.64
        """
        # ⬤ Breakpoint 1 (Line 40)
        if principal < 0 or rate < 0 or years <= 0:
            raise ValueError("Principal and rate must be non-negative, years must be positive")
            
        # ⬤ Breakpoint 2 (Line 43)
        monthly_rate = rate / 12
        num_payments = years * 12
        
        # ⬤ Breakpoint 3 (Line 46)
        if monthly_rate == 0:
            return principal / num_payments
            
        # ⬤ Breakpoint 4 (Line 51)
        numerator = principal * monthly_rate * (1 + monthly_rate)**num_payments
        denominator = (1 + monthly_rate)**num_payments - 1
        return numerator / denominator

    @staticmethod
    def calculate_loan_balance(
        original_principal: float,
        annual_rate: float,
        original_term: int,
        years_elapsed: int
    ) -> float:
        """
        Calculate remaining loan balance.
        
        Args:
            original_principal: Original loan amount
            annual_rate: Annual interest rate as decimal
            original_term: Original loan term in years
            years_elapsed: Years elapsed since loan start
            
        Returns:
            Remaining loan balance
            
        Examples:
            >>> Calculator.calculate_loan_balance(200000, 0.05, 30, 5)
            180371.80
        """
        if original_principal < 0 or annual_rate < 0:
            raise ValueError("Principal and rate must be non-negative")
        if original_term <= 0 or years_elapsed < 0:
            raise ValueError("Term must be positive, elapsed years must be non-negative")
        if years_elapsed > original_term:
            raise ValueError("Elapsed years cannot exceed original term")
            
        # ⬤ Breakpoint 5 (Line 80)
        monthly_rate = annual_rate / 12
        
        monthly_payment = Calculator.calculate_monthly_payment(
            original_principal,
            annual_rate,
            original_term
        )
        
        remaining_balance = original_principal
        months_elapsed = years_elapsed * 12
        
        for _ in range(months_elapsed):  # ⬤ Breakpoint 6 (Line 91)
            interest = remaining_balance * monthly_rate
            principal_paid = monthly_payment - interest
            remaining_balance -= principal_paid
        
        return remaining_balance

    @staticmethod
    def calculate_investment_metrics(data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Calculate investment property metrics.
        
        Args:
            data: Dictionary containing investment property data including:
                purchase_price: Purchase price of property
                down_payment: Down payment amount
                rate: Annual interest rate (as percentage)
                monthly_rent: Monthly rental income
                vacancy_rate: Expected vacancy rate (as percentage)
                other_income: Additional monthly income
                parking_income: Monthly parking income
                laundry_income: Monthly laundry income
                property_tax: Annual property tax
                insurance: Annual insurance cost
                maintenance: Annual maintenance cost
                utilities: Annual utilities cost
                mgmt_fee: Property management fee (as percentage)
                loan_term: Loan term in years
            
        Returns:
            Dictionary containing calculated metrics:
                monthly_payment: Monthly mortgage payment
                annual_cash_flow: Annual cash flow
                noi: Net Operating Income
                cap_rate: Capitalization Rate
                cash_on_cash: Cash on Cash Return
                total_expenses: Total Annual Expenses
                
        Examples:
            >>> data = {
            ...     'purchase_price': 200000,
            ...     'down_payment': 40000,
            ...     'rate': 5,
            ...     'monthly_rent': 2000,
            ...     'vacancy_rate': 5,
            ...     'loan_term': 30
            ... }
            >>> Calculator.calculate_investment_metrics(data)
            {
                'monthly_payment': 858.91,
                'annual_cash_flow': 12000,
                'noi': 22800,
                'cap_rate': 11.4,
                'cash_on_cash': 30.0,
                'total_expenses': 1200
            }
        """
        # Input validation first
        if not isinstance(data, dict):
            raise TypeError("Input must be a dictionary")
            
        # Get and validate basic property information
        purchase_price = float(data.get('purchase_price', 0))
        down_payment = float(data.get('down_payment', 0))
        rate = float(data.get('rate', 0)) / 100
        loan_term = int(data.get('loan_term', 30))
        
        if purchase_price < 0 or down_payment < 0 or rate < 0:
            raise ValueError("Financial values cannot be negative")
        if down_payment > purchase_price:
            raise ValueError("Down payment cannot exceed purchase price")
        if loan_term <= 0:
            raise ValueError("Loan term must be positive")
            
        loan_amount = purchase_price - down_payment
        
        # Get and validate income information
        monthly_rent = float(data.get('monthly_rent', 0))
        vacancy_rate = float(data.get('vacancy_rate', 0)) / 100
        
        if monthly_rent < 0:
            raise ValueError("Rent cannot be negative")
        if vacancy_rate < 0 or vacancy_rate > 1:
            raise ValueError("Vacancy rate must be between 0 and 100")
            
        annual_rent = monthly_rent * 12
        vacancy_loss = annual_rent * vacancy_rate
        effective_gross_income = annual_rent - vacancy_loss
        
        # Additional income validation and calculation
        other_income = float(data.get('other_income', 0))
        parking_income = float(data.get('parking_income', 0))
        laundry_income = float(data.get('laundry_income', 0))
        
        if other_income < 0 or parking_income < 0 or laundry_income < 0:
            raise ValueError("Income values cannot be negative")
            
        effective_gross_income += other_income + parking_income + laundry_income
        
        # Expense validation and calculation
        property_tax = float(data.get('property_tax', 0))
        insurance = float(data.get('insurance', 0))
        maintenance = float(data.get('maintenance', 0))
        utilities = float(data.get('utilities', 0))
        mgmt_fee_rate = float(data.get('mgmt_fee', 0)) / 100
        
        if property_tax < 0 or insurance < 0 or maintenance < 0 or utilities < 0:
            raise ValueError("Expense values cannot be negative")
        if mgmt_fee_rate < 0 or mgmt_fee_rate > 1:
            raise ValueError("Management fee rate must be between 0 and 100")
            
        mgmt_fee = mgmt_fee_rate * effective_gross_income
        
        # Calculate loan payment
        monthly_payment = Calculator.calculate_monthly_payment(
                loan_amount,
                rate,
            loan_term
        )
        annual_debt_service = monthly_payment * 12
        
        # Calculate operating metrics
        total_expenses = (
            property_tax +
            insurance +
            maintenance +
            utilities +
            mgmt_fee
        )
        noi = effective_gross_income - total_expenses
        cash_flow = noi - annual_debt_service
        
        cap_rate = 0 if purchase_price == 0 else (noi / purchase_price) * 100
        cash_on_cash = 0 if down_payment == 0 else (cash_flow / down_payment) * 100
        
        return {
            'monthly_payment': monthly_payment,
            'annual_cash_flow': cash_flow,
            'noi': noi,
            'cap_rate': cap_rate,
            'cash_on_cash': cash_on_cash,
            'total_expenses': total_expenses
        }

    @staticmethod
    def calculate_closing_costs(data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Calculate closing costs for a real estate transaction.
        
        Args:
            data: Dictionary containing transaction data including:
                purchase_price: Purchase price of property
                loan_amount: Amount being borrowed
                state: State where property is located (affects rates)
                
        Returns:
            Dictionary containing:
                total_closing_costs: Total closing costs
                itemized_costs: Breakdown of individual costs
                
        Examples:
            >>> data = {
            ...     'purchase_price': 200000,
            ...     'loan_amount': 160000
            ... }
            >>> Calculator.calculate_closing_costs(data)
            {
                'total_closing_costs': 3600,
                'itemized_costs': {
                    'loan_origination': 1600,
                    'appraisal': 500,
                    'credit_report': 50,
                    'tax_service': 75,
                    'flood_cert': 25,
                    'title_insurance': 1000,
                    'recording': 350
                }
            }
        """
        if not isinstance(data, dict):
            raise TypeError("Input must be a dictionary")
            
        purchase_price = float(data.get('purchase_price', 0))
        loan_amount = float(data.get('loan_amount', 0))
        
        if purchase_price < 0 or loan_amount < 0:
            raise ValueError("Financial values cannot be negative")
        if loan_amount > purchase_price:
            raise ValueError("Loan amount cannot exceed purchase price")
            
        # Calculate standard closing costs
        loan_origination = loan_amount * 0.01
        appraisal_fee = 500
        credit_report = 50
        tax_service = 75
        flood_certification = 25
        title_insurance = purchase_price * 0.005
        recording_fees = 350
        
        total_buyer_closing = (
            loan_origination +
            appraisal_fee +
            credit_report +
            tax_service +
            flood_certification +
            title_insurance +
            recording_fees
        )
        
        return {
            'total_closing_costs': total_buyer_closing,
            'itemized_costs': {
                'loan_origination': loan_origination,
                'appraisal': appraisal_fee,
                'credit_report': credit_report,
                'tax_service': tax_service,
                'flood_cert': flood_certification,
                'title_insurance': title_insurance,
                'recording': recording_fees
            }
        }