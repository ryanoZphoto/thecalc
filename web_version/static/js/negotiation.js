// Negotiation Scenario Manager
class NegotiationScenario {
    constructor() {
        console.log('Initializing NegotiationScenario');
        this.buyerTerms = {};
        this.sellerTerms = {};
        this.commonGround = {};
        this.suggestions = [];
    }

    // Set initial terms for both parties
    setTerms(party, terms) {
        console.log(`Setting terms for ${party}:`, terms);
        if (party === 'buyer') {
            this.buyerTerms = terms;
        } else {
            this.sellerTerms = terms;
        }
        this.analyzeTerms();
    }

    // Analyze differences and find potential compromises
    analyzeTerms() {
        console.log('Analyzing terms');
        this.commonGround = {};
        this.suggestions = [];

        // Find matching terms
        for (let key in this.buyerTerms) {
            if (this.sellerTerms[key] === this.buyerTerms[key]) {
                this.commonGround[key] = this.buyerTerms[key];
            }
        }

        console.log('Common ground found:', this.commonGround);

        // Analyze price difference
        if (this.buyerTerms.price && this.sellerTerms.price) {
            const priceDiff = this.sellerTerms.price - this.buyerTerms.price;
            console.log('Price difference:', priceDiff);
            if (priceDiff > 0) {
                this.analyzePriceGap(priceDiff);
            }
        }

        // Analyze closing timeline
        this.analyzeClosingTimeline();

        // Analyze contingencies
        this.analyzeContingencies();

        // Analyze included items
        this.analyzeIncludedItems();

        console.log('Analysis complete. Suggestions:', this.suggestions);
    }

    // Generate creative solutions for price gaps
    analyzePriceGap(gap) {
        const suggestions = [];
        
        // Seller financing options
        if (gap > 20000) {
            suggestions.push({
                type: 'financing',
                description: 'Consider seller financing for part of the purchase price',
                details: {
                    amount: Math.round(gap * 0.5),
                    term: '2-5 years',
                    benefit: 'Reduces buyer\'s immediate cash needs while providing seller with interest income'
                }
            });
        }

        // Closing cost negotiations
        suggestions.push({
            type: 'closing_costs',
            description: 'Split the difference in closing costs',
            details: {
                amount: Math.round(gap * 0.1),
                benefit: 'Reduces total cash needed at closing'
            }
        });

        // Rent-back options
        if (this.sellerTerms.needsTime) {
            suggestions.push({
                type: 'rent_back',
                description: 'Offer seller rent-back period in exchange for price reduction',
                details: {
                    duration: '1-2 months',
                    savings: Math.round(gap * 0.1),
                    benefit: 'Gives seller flexibility for moving while reducing price'
                }
            });
        }

        // Home warranty
        suggestions.push({
            type: 'warranty',
            description: 'Include home warranty in the deal',
            details: {
                cost: 500,
                benefit: 'Provides buyer protection and reduces seller liability'
            }
        });

        this.suggestions.push(...suggestions);
    }

    // Analyze closing timeline differences
    analyzeClosingTimeline() {
        if (this.buyerTerms.closingDate && this.sellerTerms.closingDate) {
            const buyerDate = new Date(this.buyerTerms.closingDate);
            const sellerDate = new Date(this.sellerTerms.closingDate);
            const daysDiff = Math.abs((buyerDate - sellerDate) / (1000 * 60 * 60 * 24));

            if (daysDiff > 14) {
                this.suggestions.push({
                    type: 'timeline',
                    description: 'Bridge closing date gap with temporary housing solution',
                    details: {
                        gap: Math.round(daysDiff),
                        options: ['Short-term rental', 'Extended stay hotel', 'Rent-back agreement']
                    }
                });
            }
        }
    }

    // Analyze contingency differences
    analyzeContingencies() {
        const buyerContingencies = this.buyerTerms.contingencies || [];
        const sellerContingencies = this.sellerTerms.contingencies || [];

        // Find contingencies that seller wants removed
        const contingencyDiffs = buyerContingencies.filter(x => !sellerContingencies.includes(x));

        if (contingencyDiffs.length > 0) {
            contingencyDiffs.forEach(contingency => {
                this.suggestions.push({
                    type: 'contingency',
                    description: `Address ${contingency} contingency`,
                    details: {
                        options: this.getContingencyOptions(contingency)
                    }
                });
            });
        }
    }

    // Get specific options for different contingency types
    getContingencyOptions(contingency) {
        const options = {
            'inspection': [
                'Shorten inspection period',
                'Set maximum repair amount',
                'Pre-listing inspection sharing'
            ],
            'financing': [
                'Provide proof of funds',
                'Increase earnest money',
                'Multiple lender pre-approvals'
            ],
            'appraisal': [
                'Appraisal gap coverage',
                'Preliminary appraisal review',
                'Seller price adjustment clause'
            ],
            'sale': [
                'Kick-out clause',
                'Bridge loan option',
                'Rent-back flexibility'
            ]
        };
        return options[contingency] || ['Discuss terms with both parties'];
    }

    // Analyze included/excluded items
    analyzeIncludedItems() {
        const buyerItems = this.buyerTerms.includedItems || [];
        const sellerItems = this.sellerTerms.includedItems || [];

        const itemDiffs = buyerItems.filter(x => !sellerItems.includes(x));

        if (itemDiffs.length > 0) {
            this.suggestions.push({
                type: 'items',
                description: 'Negotiate included items',
                details: {
                    items: itemDiffs,
                    options: [
                        'Separate purchase agreement',
                        'Price adjustment',
                        'Replacement options'
                    ]
                }
            });
        }
    }

    // Get all suggestions with priority ranking
    getSuggestions() {
        return this.suggestions.sort((a, b) => {
            const priority = {
                'financing': 1,
                'closing_costs': 2,
                'contingency': 3,
                'timeline': 4,
                'items': 5
            };
            return priority[a.type] - priority[b.type];
        });
    }

    // Calculate potential savings from all suggestions
    calculatePotentialSavings() {
        return this.suggestions.reduce((total, suggestion) => {
            if (suggestion.details && suggestion.details.amount) {
                return total + suggestion.details.amount;
            }
            return total;
        }, 0);
    }
}

// Initialize negotiation manager and make it globally available
console.log('Creating global negotiation manager');
window.negotiationManager = new NegotiationScenario(); 