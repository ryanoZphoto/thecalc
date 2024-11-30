class NegotiationCalculator {
    constructor() {
        this.initializeEventListeners();
    }

    initializeEventListeners() {
        document.getElementById('calculate-offer').addEventListener('click', () => this.calculateOffer());
    }

    async calculateOffer() {
        const data = {
            listingPrice: parseFloat(document.getElementById('listing-price').value) || 0,
            marketValue: parseFloat(document.getElementById('market-value').value) || 0,
            daysOnMarket: parseFloat(document.getElementById('days-on-market').value) || 0,
            comparableSales: parseFloat(document.getElementById('comparable-sales').value) || 0,
            repairCosts: parseFloat(document.getElementById('repair-costs').value) || 0,
            marketCondition: document.getElementById('market-condition').value
        };

        try {
            const response = await fetch('/negotiate', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(data)
            });

            const result = await response.json();
            this.displayResults(data, result);
        } catch (error) {
            console.error('Negotiation calculation error:', error);
        }
    }

    displayResults(data, result) {
        const resultsDiv = document.getElementById('negotiation-results');
        const recommendedOffer = this.calculateRecommendedOffer(data);
        
        let html = `
            <h3>Negotiation Analysis</h3>
            <div class="analysis">
                <p>Recommended Offer: $${recommendedOffer.toLocaleString()}</p>
                <p>This is ${((recommendedOffer / data.listingPrice - 1) * 100).toFixed(1)}% ${
                    recommendedOffer > data.listingPrice ? 'above' : 'below'
                } listing price</p>
                <h4>Factors Considered:</h4>
                <ul>
                    ${this.generateFactorsList(data)}
                </ul>
                <h4>Negotiation Strategy:</h4>
                ${this.generateStrategy(data, recommendedOffer)}
            </div>
        `;

        resultsDiv.innerHTML = html;
    }

    calculateRecommendedOffer(data) {
        let baseValue = data.marketValue || data.listingPrice;
        
        // Adjust for market conditions
        const marketFactor = {
            'hot': 1.02,    // Hot market: might need to offer above asking
            'neutral': 1,    // Neutral market: around asking
            'cold': 0.95     // Cold market: room for negotiation
        }[data.marketCondition];
        
        // Adjust for days on market
        const domFactor = Math.max(0.95, 1 - (data.daysOnMarket / 1000));
        
        // Adjust for repairs
        const repairFactor = 1 - (data.repairCosts / data.listingPrice);
        
        return baseValue * marketFactor * domFactor * repairFactor;
    }

    generateFactorsList(data) {
        const factors = [];
        
        if (data.daysOnMarket > 60) {
            factors.push('Extended time on market suggests negotiation flexibility');
        }
        
        if (data.repairCosts > 0) {
            factors.push(`Repair costs of $${data.repairCosts.toLocaleString()} considered`);
        }
        
        if (data.marketCondition === 'hot') {
            factors.push('Strong seller\'s market may require competitive offer');
        } else if (data.marketCondition === 'cold') {
            factors.push('Buyer\'s market provides negotiation leverage');
        }

        return factors.map(f => `<li>${f}</li>`).join('');
    }

    generateStrategy(data, recommendedOffer) {
        const strategy = [];
        
        if (recommendedOffer < data.listingPrice) {
            strategy.push('Start with a lower offer supported by:');
            if (data.daysOnMarket > 60) {
                strategy.push('- Mention the extended market time');
            }
            if (data.repairCosts > 0) {
                strategy.push('- Detail repair costs with estimates');
            }
        } else {
            strategy.push('Consider a strong offer because:');
            if (data.marketCondition === 'hot') {
                strategy.push('- Current seller\'s market conditions');
            }
            if (data.comparableSales > data.listingPrice) {
                strategy.push('- Comparable sales support the value');
            }
        }

        return strategy.map(s => `<p>${s}</p>`).join('');
    }
}

// Initialize negotiation calculator when DOM is loaded
document.addEventListener('DOMContentLoaded', () => {
    new NegotiationCalculator();
}); 