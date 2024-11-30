class CalculatorUI {
    constructor() {
        this.expression = '';
        this.initializeEventListeners();
    }

    initializeEventListeners() {
        document.querySelectorAll('.calculator-button').forEach(button => {
            button.addEventListener('click', () => this.handleButton(button.dataset.value));
        });
    }

    handleButton(value) {
        switch(value) {
            case '=':
                this.calculate();
                break;
            case 'C':
                this.clear();
                break;
            default:
                this.appendValue(value);
        }
    }

    async calculate() {
        try {
            const response = await fetch('/calculate', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ expression: this.expression })
            });
            
            const data = await response.json();
            document.getElementById('result').value = data.result;
        } catch (error) {
            console.error('Calculation error:', error);
            document.getElementById('result').value = 'Error';
        }
    }

    clear() {
        this.expression = '';
        document.getElementById('result').value = '';
    }

    appendValue(value) {
        this.expression += value;
        document.getElementById('result').value = this.expression;
    }
}

// Initialize calculator when DOM is loaded
document.addEventListener('DOMContentLoaded', () => {
    new CalculatorUI();
}); 