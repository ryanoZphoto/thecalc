from flask import Flask, render_template, request, jsonify
import json
from datetime import datetime

app = Flask(__name__)

class Calculator:
    @staticmethod
    def calculate_monthly_payment(principal, rate, years):
        monthly_rate = rate / 12
        num_payments = years * 12
        if monthly_rate == 0:
            return principal / num_payments
        return (principal * monthly_rate * (1 + monthly_rate)**num_payments) / ((1 + monthly_rate)**num_payments - 1)

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
    
    return jsonify({'error': 'Invalid calculation type'})

@app.route('/save_scenario', methods=['POST'])
def save_scenario():
    data = request.json
    try:
        scenarios = load_scenarios()
        scenario_id = str(len(scenarios) + 1)
        scenarios[scenario_id] = {
            'name': data.get('name'),
            'data': data.get('data'),
            'created_at': datetime.now().isoformat()
        }
        save_scenarios(scenarios)
        return jsonify({'success': True, 'id': scenario_id})
    except Exception as e:
        return jsonify({'error': str(e)})

@app.route('/scenarios', methods=['GET'])
def get_scenarios():
    try:
        scenarios = load_scenarios()
        return jsonify(scenarios)
    except Exception as e:
        return jsonify({'error': str(e)})

def load_scenarios():
    try:
        with open('scenarios.json', 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        return {}

def save_scenarios(scenarios):
    with open('scenarios.json', 'w') as f:
        json.dump(scenarios, f, indent=2)

if __name__ == '__main__':
    app.run(debug=True) 