class PropertyComparison {
    constructor() {
        this.initializeEventListeners();
    }

    initializeEventListeners() {
        document.getElementById('compare-btn').addEventListener('click', () => this.compareProperties());
    }

    getPropertyData(prefix) {
        return {
            address: document.getElementById(`${prefix}-address`).value,
            price: parseFloat(document.getElementById(`${prefix}-price`).value) || 0,
            sqft: parseFloat(document.getElementById(`${prefix}-sqft`).value) || 0,
            beds: parseFloat(document.getElementById(`${prefix}-beds`).value) || 0,
            baths: parseFloat(document.getElementById(`${prefix}-baths`).value) || 0,
            age: parseFloat(document.getElementById(`${prefix}-age`).value) || 0,
            lot: parseFloat(document.getElementById(`${prefix}-lot`).value) || 0,
            hoa: parseFloat(document.getElementById(`${prefix}-hoa`).value) || 0,
            tax: parseFloat(document.getElementById(`${prefix}-tax`).value) || 0
        };
    }

    async compareProperties() {
        const p1 = this.getPropertyData('p1');
        const p2 = this.getPropertyData('p2');

        try {
            const response = await fetch('/compare', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ p1, p2 })
            });

            const data = await response.json();
            this.displayResults(p1, p2, data.analysis);
        } catch (error) {
            console.error('Comparison error:', error);
        }
    }

    displayResults(p1, p2, analysis) {
        const resultsDiv = document.getElementById('comparison-results');
        const pricePerSqFt1 = p1.price / p1.sqft;
        const pricePerSqFt2 = p2.price / p2.sqft;

        let html = `
            <h3>Comparison Analysis</h3>
            <table>
                <tr>
                    <th>Metric</th>
                    <th>${p1.address}</th>
                    <th>${p2.address}</th>
                </tr>
                <tr>
                    <td>Price</td>
                    <td>$${p1.price.toLocaleString()}</td>
                    <td>$${p2.price.toLocaleString()}</td>
                </tr>
                <tr>
                    <td>Price/sqft</td>
                    <td>$${pricePerSqFt1.toFixed(2)}</td>
                    <td>$${pricePerSqFt2.toFixed(2)}</td>
                </tr>
                <tr>
                    <td>Monthly Costs</td>
                    <td>$${(p1.hoa + p1.tax/12).toFixed(2)}</td>
                    <td>$${(p2.hoa + p2.tax/12).toFixed(2)}</td>
                </tr>
            </table>
            <div class="recommendation">
                <h4>Recommendation</h4>
                <p>${this.generateRecommendation(p1, p2)}</p>
            </div>
        `;

        resultsDiv.innerHTML = html;
    }

    generateRecommendation(p1, p2) {
        const factors = [];
        
        // Price comparison
        if (p1.price < p2.price) {
            factors.push(`Property 1 is ${((p2.price - p1.price) / p2.price * 100).toFixed(1)}% less expensive`);
        }
        
        // Price per square foot
        const ppsf1 = p1.price / p1.sqft;
        const ppsf2 = p2.price / p2.sqft;
        if (Math.abs(ppsf1 - ppsf2) > 10) {
            factors.push(`Property ${ppsf1 < ppsf2 ? '1' : '2'} has better price per square foot`);
        }
        
        // Monthly costs
        const monthly1 = p1.hoa + p1.tax/12;
        const monthly2 = p2.hoa + p2.tax/12;
        if (Math.abs(monthly1 - monthly2) > 100) {
            factors.push(`Property ${monthly1 < monthly2 ? '1' : '2'} has lower monthly costs`);
        }

        return factors.join('. ') + '.';
    }
}

// Initialize comparison tool when DOM is loaded
document.addEventListener('DOMContentLoaded', () => {
    new PropertyComparison();
}); 