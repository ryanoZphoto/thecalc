"""Web application for real estate calculations."""

import locale
from datetime import datetime
from pathlib import Path
from typing import Dict, Any

from flask import Flask, render_template, jsonify, request


# Set locale for currency formatting
locale.setlocale(locale.LC_ALL, '')


class Calculator:
    """Calculator class for financial computations."""
    
    @staticmethod
    def calculate_monthly_payment(
        principal: float,
        rate: float,
        years: int
    ) -> float:
        """Calculate monthly mortgage payment."""
        monthly_rate = rate / 12
        num_payments = years * 12
        
        if monthly_rate == 0:
            return principal / num_payments
            
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
        """Calculate remaining balance based on original term and years elapsed."""
        monthly_rate = annual_rate / 12
        monthly_payment = Calculator.calculate_monthly_payment(
            original_principal,
            annual_rate,
            original_term
        )
        
        remaining_balance = original_principal
        months_elapsed = years_elapsed * 12
        
        for _ in range(months_elapsed):
            interest = remaining_balance * monthly_rate
            principal_paid = monthly_payment - interest
            remaining_balance -= principal_paid
        
        return remaining_balance

    # ... rest of Calculator class methods ...


app = Flask(__name__)


@app.after_request
def add_header(response):
    """Ensure static files aren't cached during development."""
    response.headers['Cache-Control'] = 'no-store'
    return response


@app.route('/')
def index():
    """Render the main calculator interface."""
    return render_template('index.html')


@app.route('/calculate', methods=['POST'])
def calculate():
    """Handle calculation requests."""
    data = request.get_json()
    calc_type = data.get('type')
    
    try:
        calculator = Calculator()
        
        if calc_type == 'seller_financing':
            results = calculator.calculate_seller_financing(data)
        elif calc_type == 'investment':
            results = calculator.calculate_investment(data)
        elif calc_type == 'closing_costs':
            results = calculator.calculate_closing_costs(data)
        else:
            return jsonify({'error': 'Invalid calculation type'})
            
        return jsonify(results)
        
    except Exception as e:
        return jsonify({'error': str(e)}), 400


if __name__ == '__main__':
    app.run(debug=True)
