from flask import Flask, render_template, request, jsonify
import json
from datetime import datetime


class Calculator:
    @staticmethod
    def calculate_monthly_payment(principal, rate, years):
        monthly_rate = rate / 12
        num_payments = years * 12
        if monthly_rate == 0:
            return principal / num_payments
        return (principal * monthly_rate * (1 + monthly_rate)**num_payments) / ((1 + monthly_rate)**num_payments - 1)

    @staticmethod
    def calculate_investment(purchase_price, monthly_rent, monthly_expenses):
        annual_rent = monthly_rent * 12
        annual_expenses = monthly_expenses * 12
        net_income = annual_rent - annual_expenses
        cash_flow = monthly_rent - monthly_expenses
        cap_rate = (net_income / purchase_price) * 100
        roi = (net_income / purchase_price) * 100
        break_even = purchase_price / (monthly_rent - monthly_expenses)
        return {
            'cash_flow': cash_flow,
            'cap_rate': cap_rate,
            'roi': roi,
            'break_even': break_even
        }

    @staticmethod
    def calculate_closing_costs(property_price, down_payment_percent, lender_fees):
        down_payment = property_price * (down_payment_percent / 100)
        title_insurance = property_price * 0.005  # 0.5% of property price
        total_closing = down_payment + lender_fees + title_insurance
        return {
            'down_payment': down_payment,
            'lender_fees': lender_fees,
            'title_insurance': title_insurance,
            'total_closing': total_closing
        }


app = Flask(__name__)


@app.route('/')
def home():
    return render_template('index.html')


@app.route('/calculate', methods=['POST'])
def calculate():
    data = request.json
    calc_type = data.get('type')
    
    if calc_type == 'seller_financing':
        sale_price = float(data.get('sale_price', 0))
        down_payment = float(data.get('down_payment', 0))
        rate = float(data.get('rate', 0)) / 100
        years = float(data.get('years', 30))
        
        loan_amount = sale_price - down_payment
        monthly_payment = Calculator.calculate_monthly_payment(loan_amount, rate, years)
        total_payments = monthly_payment * years * 12
        total_interest = total_payments - loan_amount
        
        return jsonify({
            'monthly_payment': round(monthly_payment, 2),
            'total_payments': round(total_payments, 2),
            'total_interest': round(total_interest, 2),
            'loan_amount': round(loan_amount, 2)
        })
    
    elif calc_type == 'investment':
        purchase_price = float(data.get('purchase_price', 0))
        monthly_rent = float(data.get('monthly_rent', 0))
        monthly_expenses = float(data.get('monthly_expenses', 0))
        
        results = Calculator.calculate_investment(
            purchase_price, monthly_rent, monthly_expenses)
        return jsonify({
            'cash_flow': round(results['cash_flow'], 2),
            'cap_rate': round(results['cap_rate'], 2),
            'roi': round(results['roi'], 2),
            'break_even': round(results['break_even'], 0)
        })
    
    elif calc_type == 'closing_costs':
        property_price = float(data.get('property_price', 0))
        down_payment_percent = float(data.get('down_payment_percent', 0))
        lender_fees = float(data.get('lender_fees', 0))
        
        results = Calculator.calculate_closing_costs(
            property_price, down_payment_percent, lender_fees)
        return jsonify({
            'down_payment': round(results['down_payment'], 2),
            'lender_fees': round(results['lender_fees'], 2),
            'title_insurance': round(results['title_insurance'], 2),
            'total_closing': round(results['total_closing'], 2)
        })
    
    return jsonify({'error': 'Invalid calculation type'})


if __name__ == '__main__':
    app.run(debug=True)