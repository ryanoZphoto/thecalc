// Function to gather form data
function getFormData(prefix) {
    log(`Getting form data for ${prefix}`);
    
    try {
        const data = {
            price: parseFloat(document.getElementById(prefix + 'Price').value) || 0,
            downPayment: parseFloat(document.getElementById(prefix + 'DownPayment').value) || 0,
            closingDate: document.getElementById(prefix + 'ClosingDate').value,
            contingencies: ['inspection', 'financing', 'appraisal', 'sale'].filter(
                c => document.getElementById(prefix + c.charAt(0).toUpperCase() + c.slice(1)).checked
            ),
            includedItems: document.getElementById(prefix + 'Items').value
                .split(',')
                .map(item => item.trim())
                .filter(item => item.length > 0),
            needsTime: prefix === 'seller' ? document.getElementById('sellerNeedsTime').checked : false
        };
        
        log(`${prefix} data collected:`, data);
        return data;
    } catch (error) {
        log(`Error getting ${prefix} data:`, error);
        throw error;
    }
}

// Function to analyze negotiation
function analyzeNegotiation() {
    log('Starting negotiation analysis');
    
    try {
        // Get form data
        const buyerTerms = getFormData('buyer');
        const sellerTerms = getFormData('seller');

        // Calculate price difference
        const priceDiff = sellerTerms.price - buyerTerms.price;
        
        // Display price analysis
        displayPriceAnalysis(buyerTerms.price, sellerTerms.price);

        // Display differences
        displayDifferences(buyerTerms, sellerTerms);

        // Generate and display suggestions
        displaySuggestions(buyerTerms, sellerTerms, priceDiff);

        // Show results
        document.getElementById('negotiationResults').style.display = 'block';
        
        log('Analysis complete');
    } catch (error) {
        log('Error in analyzeNegotiation:', error);
        alert('There was an error analyzing the negotiation. Please check all inputs and try again.');
    }
}

// Function to display price analysis
function displayPriceAnalysis(buyerPrice, sellerPrice) {
    log('Displaying price analysis');
    
    const container = document.getElementById('priceAnalysis');
    const priceDiff = sellerPrice - buyerPrice;
    const percentDiff = (priceDiff / sellerPrice) * 100;
    
    container.innerHTML = `
        <div class="row">
            <div class="col-md-6">
                <p><strong>Buyer's Offer:</strong> ${formatCurrency(buyerPrice)}</p>
                <p><strong>Seller's Ask:</strong> ${formatCurrency(sellerPrice)}</p>
            </div>
            <div class="col-md-6">
                <p><strong>Price Gap:</strong> ${formatCurrency(priceDiff)}</p>
                <p><strong>Percentage Difference:</strong> ${percentDiff.toFixed(1)}%</p>
            </div>
        </div>
    `;
}

// Function to display differences
function displayDifferences(buyerTerms, sellerTerms) {
    log('Displaying differences');
    
    const container = document.getElementById('gapAnalysis');
    const differences = [];

    // Check down payment
    if (buyerTerms.downPayment !== sellerTerms.downPayment) {
        differences.push({
            item: 'Down Payment',
            buyer: `${buyerTerms.downPayment}%`,
            seller: `${sellerTerms.downPayment}%`
        });
    }

    // Check closing date
    if (buyerTerms.closingDate !== sellerTerms.closingDate) {
        differences.push({
            item: 'Closing Date',
            buyer: formatDate(buyerTerms.closingDate),
            seller: formatDate(sellerTerms.closingDate)
        });
    }

    // Check contingencies
    const buyerOnlyContingencies = buyerTerms.contingencies.filter(x => !sellerTerms.contingencies.includes(x));
    const sellerOnlyContingencies = sellerTerms.contingencies.filter(x => !buyerTerms.contingencies.includes(x));
    
    if (buyerOnlyContingencies.length > 0 || sellerOnlyContingencies.length > 0) {
        differences.push({
            item: 'Contingencies',
            buyer: buyerOnlyContingencies.join(', ') || 'None',
            seller: sellerOnlyContingencies.join(', ') || 'None'
        });
    }

    // Check included items
    const buyerOnlyItems = buyerTerms.includedItems.filter(x => !sellerTerms.includedItems.includes(x));
    const sellerOnlyItems = sellerTerms.includedItems.filter(x => !buyerTerms.includedItems.includes(x));
    
    if (buyerOnlyItems.length > 0 || sellerOnlyItems.length > 0) {
        differences.push({
            item: 'Included Items',
            buyer: buyerOnlyItems.join(', ') || 'None',
            seller: sellerOnlyItems.join(', ') || 'None'
        });
    }

    // Display differences table
    if (differences.length > 0) {
        container.innerHTML = `
            <table class="table table-sm">
                <thead>
                    <tr>
                        <th>Item</th>
                        <th>Buyer's Terms</th>
                        <th>Seller's Terms</th>
                    </tr>
                </thead>
                <tbody>
                    ${differences.map(diff => `
                        <tr>
                            <td>${diff.item}</td>
                            <td>${diff.buyer}</td>
                            <td>${diff.seller}</td>
                        </tr>
                    `).join('')}
                </tbody>
            </table>
        `;
    } else {
        container.innerHTML = '<p class="text-muted">No significant differences found.</p>';
    }
}

// Function to display suggestions
function displaySuggestions(buyerTerms, sellerTerms, priceDiff) {
    log('Displaying suggestions');
    
    const container = document.getElementById('suggestions');
    const suggestions = [];

    // Price gap suggestions
    if (priceDiff > 0) {
        suggestions.push({
            title: 'Bridge Price Gap',
            items: [
                `Meet in the middle at ${formatCurrency(buyerTerms.price + (priceDiff/2))}`,
                'Consider seller financing for part of the difference',
                'Adjust closing costs sharing',
                'Include home warranty'
            ]
        });
    }

    // Down payment suggestions
    if (buyerTerms.downPayment < sellerTerms.downPayment) {
        suggestions.push({
            title: 'Down Payment Solutions',
            items: [
                'Increase earnest money deposit',
                'Provide proof of funds/strong pre-approval',
                'Consider seller financing for the difference'
            ]
        });
    }

    // Closing date suggestions
    if (buyerTerms.closingDate !== sellerTerms.closingDate) {
        suggestions.push({
            title: 'Timeline Solutions',
            items: [
                'Consider rent-back agreement',
                'Adjust closing date with price consideration',
                'Explore bridge loan options'
            ]
        });
    }

    // Display suggestions
    container.innerHTML = suggestions.map((suggestion, index) => `
        <div class="card mb-2">
            <div class="card-header" id="heading${index}">
                <h6 class="mb-0">
                    <button class="btn btn-link" type="button" data-bs-toggle="collapse" 
                            data-bs-target="#collapse${index}">
                        ${suggestion.title}
                    </button>
                </h6>
            </div>
            <div id="collapse${index}" class="collapse ${index === 0 ? 'show' : ''}" 
                 data-bs-parent="#suggestions">
                <div class="card-body">
                    <ul class="mb-0">
                        ${suggestion.items.map(item => `<li>${item}</li>`).join('')}
                    </ul>
                </div>
            </div>
        </div>
    `).join('');

    // Display summary
    displaySummary(buyerTerms, sellerTerms, suggestions);
}

// Function to display summary
function displaySummary(buyerTerms, sellerTerms, suggestions) {
    log('Displaying summary');
    
    const container = document.getElementById('negotiationSummary');
    const priceDiff = sellerTerms.price - buyerTerms.price;
    
    container.innerHTML = `
        <p>The current negotiation has a price gap of ${formatCurrency(priceDiff)} 
           (${((priceDiff/sellerTerms.price) * 100).toFixed(1)}% of asking price).</p>
        <p>Key areas for negotiation:</p>
        <ul>
            ${suggestions.map(s => `<li>${s.title}</li>`).join('')}
        </ul>
        <p class="mb-0">Review the suggested solutions above and consider presenting multiple options 
           to find common ground.</p>
    `;
}

// Helper function to format currency
function formatCurrency(amount) {
    return new Intl.NumberFormat('en-US', {
        style: 'currency',
        currency: 'USD'
    }).format(amount);
}

// Helper function to format dates
function formatDate(dateString) {
    return new Date(dateString).toLocaleDateString('en-US', {
        year: 'numeric',
        month: 'long',
        day: 'numeric'
    });
}

// Make sure analyzeNegotiation is globally available
window.analyzeNegotiation = analyzeNegotiation; 