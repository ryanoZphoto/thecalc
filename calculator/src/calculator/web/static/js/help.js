class CalculatorHelp {
    constructor() {
        this.initializeEventListeners();
        this.loadHelpContent();
    }

    initializeEventListeners() {
        // Toggle info sections
        document.querySelectorAll('.toggle-info').forEach(button => {
            button.addEventListener('click', (e) => {
                const infoContent = e.target.closest('.calculator-info')
                    .querySelector('.info-content');
                infoContent.classList.toggle('active');
                
                // Update button text
                button.textContent = infoContent.classList.contains('active') ? 'ⓧ' : 'ⓘ';
            });
        });

        // Field-specific help
        this.addFieldTooltips();
    }

    addFieldTooltips() {
        const tooltips = {
            'property-price': 'The full purchase price of the property',
            'down-payment': 'The initial payment made by the buyer',
            'interest-rate': 'Annual interest rate for the seller financing',
            'balloon-years': 'Years until the balloon payment is due (if any)',
            // Add more field-specific tooltips
        };

        Object.entries(tooltips).forEach(([id, text]) => {
            const field = document.getElementById(id);
            if (field) {
                const wrapper = document.createElement('div');
                wrapper.className = 'input-wrapper';
                field.parentNode.insertBefore(wrapper, field);
                wrapper.appendChild(field);
                
                wrapper.insertAdjacentHTML('beforeend', `
                    <span class="tooltip-icon">ⓘ</span>
                    <div class="tooltip-content">${text}</div>
                `);
            }
        });
    }

    loadHelpContent() {
        // Load any dynamic help content
        this.loadCalculatorTips();
        this.loadCommonScenarios();
    }

    loadCalculatorTips() {
        // Add dynamic tips based on user interaction
        document.querySelectorAll('input, select').forEach(field => {
            field.addEventListener('focus', () => this.showContextualHelp(field));
        });
    }

    showContextualHelp(field) {
        const helpPanel = document.createElement('div');
        helpPanel.className = 'contextual-help';
        helpPanel.textContent = this.getContextualHelpText(field.id);
        
        // Show help panel
        const existingHelp = document.querySelector('.contextual-help');
        if (existingHelp) existingHelp.remove();
        field.parentNode.appendChild(helpPanel);
    }

    getContextualHelpText(fieldId) {
        // Return contextual help based on field
        const helpText = {
            'buyer-income': 'Higher income improves buyer qualification and may allow for better terms',
            'credit-range': 'Credit score affects interest rate and down payment requirements',
            // Add more contextual help
        };
        return helpText[fieldId] || 'Enter value to continue';
    }
}

// Initialize help system
document.addEventListener('DOMContentLoaded', () => {
    new CalculatorHelp();
}); 