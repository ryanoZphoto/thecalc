"""Web application module for the calculator suite."""

from pathlib import Path
from flask import (
    Flask,
    render_template,
    jsonify,
    request,
    url_for
)
from docxtpl import DocxTemplate

from calculator.core.calc import Calculator
from calculator.core.risk_analyzer import RiskAnalyzer


app = Flask(
    __name__,
    static_folder='static',
    template_folder='templates'
)


@app.after_request
def add_header(response):
    """Ensure static files aren't cached during development."""
    response.headers['Cache-Control'] = 'no-store'
    return response


risk_analyzer = RiskAnalyzer()


@app.route('/')
def index():
    """Render the calculator suite web interface."""
    return render_template('index.html')


@app.route('/calculate', methods=['POST'])
def calculate():
    """Handle calculation requests."""
    data = request.get_json()
    calc_type = data.get('type')
    calculator = Calculator()
    
    try:
        if calc_type == 'investment':
            results = calculator.calculate_investment_metrics(data)
        elif calc_type == 'closing_costs':
            results = calculator.calculate_closing_costs(data)
        else:
            return jsonify({'error': 'Invalid calculation type'})
            
        return jsonify(results)
        
    except Exception as e:
        return jsonify({'error': str(e)}), 400


@app.route('/generate-document', methods=['POST'])
def generate_document():
    """Generate document from template."""
    data = request.get_json()
    template_name = data.get('template')
    doc_data = data.get('data')
    
    template_path = (
        Path(__file__).parent
        / 'templates'
        / 'documents'
        / template_name
    )
    
    if not template_path.exists():
        return jsonify({'error': 'Template not found'}), 404
    
    doc = DocxTemplate(template_path)
    doc.render(doc_data)
    
    output_path = (
        Path(__file__).parent
        / 'static'
        / 'generated'
        / f'generated_{template_name}'
    )
    doc.save(output_path)
    
    return jsonify({
        'success': True,
        'file_url': url_for(
            'static',
            filename=f'generated/generated_{template_name}'
        )
    })


@app.route('/analyze-risks', methods=['POST'])
def analyze_risks():
    """Analyze risks for a given strategy."""
    data = request.get_json()
    strategy = data.get('strategy')
    property_data = data.get('property')
    
    risk_analysis = {
        'legal': risk_analyzer.analyze_legal_risks(
            strategy,
            property_data
        ),
        'financial': risk_analyzer.analyze_financial_risks(
            strategy,
            property_data
        ),
        'market': risk_analyzer.analyze_market_risks(
            strategy,
            property_data
        ),
        'operational': risk_analyzer.analyze_operational_risks(
            strategy,
            property_data
        )
    }
    
    return jsonify(risk_analysis)


if __name__ == '__main__':
    app.run(debug=True) 