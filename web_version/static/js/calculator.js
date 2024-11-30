// Basic mortgage calculator
function calculateMortgage() {
    const price = parseFloat(document.getElementById('purchasePrice').value);
    const down = parseFloat(document.getElementById('downPayment').value);
    const rate = parseFloat(document.getElementById('interestRate').value);
    const term = parseFloat(document.getElementById('loanTerm').value);
    const tax = parseFloat(document.getElementById('propertyTax').value);
    const insurance = parseFloat(document.getElementById('insurance').value);

    if (!price || !down || !rate || !term || !tax || !insurance) return;

    const principal = price - down;
    const monthlyRate = rate / 1200;
    const payments = term * 12;
    
    const monthlyPI = principal * (monthlyRate * Math.pow(1 + monthlyRate, payments)) / (Math.pow(1 + monthlyRate, payments) - 1);
    const monthlyEscrow = (tax + insurance) / 12;
    const totalMonthly = monthlyPI + monthlyEscrow;
    
    const totalPayments = totalMonthly * payments;
    const totalInterest = (monthlyPI * payments) - principal;

    const results = [
        {
            label: 'Monthly Payment',
            value: totalMonthly,
            detail: `Principal & Interest: ${formatCurrency(monthlyPI)} + Escrow: ${formatCurrency(monthlyEscrow)}`
        },
        {
            label: 'Down Payment',
            value: down,
            detail: `${((down / price) * 100).toFixed(1)}% of purchase price`
        },
        {
            label: 'Loan Amount',
            value: principal,
            detail: `${((principal / price) * 100).toFixed(1)}% of purchase price`
        },
        {
            label: 'Total Interest',
            value: totalInterest,
            detail: `Over ${term} years`
        },
        {
            label: 'Total Cost',
            value: totalPayments + down,
            detail: 'Including down payment and escrow'
        }
    ];

    displayResults('basicResults', results);
}

// Investment calculator
function calculateInvestment() {
    // Get all input values
    const inputs = {
        purchasePrice: getFloat('invPurchasePrice'),
        arv: getFloat('arv'),
        rehabCost: getFloat('rehabCost'),
        holdingPeriod: getFloat('holdingPeriod'),
        downPaymentPercent: getFloat('invDownPayment'),
        interestRate: getFloat('invInterestRate'),
        loanTerm: getFloat('invLoanTerm'),
        closingCosts: getFloat('closingCosts'),
        monthlyRent: getFloat('monthlyRent'),
        otherIncome: getFloat('otherIncome'),
        rentIncrease: getFloat('rentIncrease'),
        vacancyRate: getFloat('vacancyRate'),
        propertyTax: getFloat('invPropertyTax'),
        insurance: getFloat('invInsurance'),
        maintenancePercent: getFloat('maintenance'),
        propertyMgmtPercent: getFloat('propertyMgmt'),
        utilities: getFloat('utilities'),
        capexReserve: getFloat('capexReserve'),
        appreciation: getFloat('appreciation'),
        inflation: getFloat('inflation')
    };

    // Calculate loan details
    const downPayment = inputs.purchasePrice * (inputs.downPaymentPercent / 100);
    const loanAmount = inputs.purchasePrice - downPayment;
    const monthlyRate = inputs.interestRate / 1200;
    const numberOfPayments = inputs.loanTerm * 12;
    const monthlyMortgage = loanAmount * (monthlyRate * Math.pow(1 + monthlyRate, numberOfPayments)) 
                          / (Math.pow(1 + monthlyRate, numberOfPayments) - 1);

    // Calculate income
    const potentialRentalIncome = (inputs.monthlyRent + inputs.otherIncome) * 12;
    const vacancyLoss = potentialRentalIncome * (inputs.vacancyRate / 100);
    const effectiveGrossIncome = potentialRentalIncome - vacancyLoss;

    // Calculate expenses
    const annualMortgage = monthlyMortgage * 12;
    const maintenanceCost = inputs.purchasePrice * (inputs.maintenancePercent / 100);
    const propertyMgmt = effectiveGrossIncome * (inputs.propertyMgmtPercent / 100);
    const capexReserve = effectiveGrossIncome * (inputs.capexReserve / 100);
    const annualUtilities = inputs.utilities * 12;
    
    const totalExpenses = annualMortgage + inputs.propertyTax + inputs.insurance + 
                        maintenanceCost + propertyMgmt + capexReserve + annualUtilities;

    // Calculate cash flow
    const annualCashFlow = effectiveGrossIncome - totalExpenses;
    const monthlyCashFlow = annualCashFlow / 12;

    // Calculate returns
    const totalInvestment = downPayment + inputs.rehabCost + 
                          (loanAmount * (inputs.closingCosts / 100));
    const cashOnCash = (annualCashFlow / totalInvestment) * 100;

    // Calculate 5-year projections
    const futureValue = inputs.purchasePrice * Math.pow(1 + (inputs.appreciation / 100), inputs.holdingPeriod);
    const equity = futureValue - loanAmount;
    const totalReturn = (equity - totalInvestment + (annualCashFlow * inputs.holdingPeriod)) / totalInvestment * 100;

    // BRRRR Analysis
    const brrrrLTV = (loanAmount / inputs.arv) * 100;
    const equityCreated = inputs.arv - inputs.purchasePrice - inputs.rehabCost;
    const refiPotential = inputs.arv * 0.75;

    // Risk Metrics
    const dscr = effectiveGrossIncome / (annualMortgage + inputs.propertyTax + inputs.insurance);
    const grossRentMultiplier = inputs.purchasePrice / potentialRentalIncome;
    const capRate = (effectiveGrossIncome - (totalExpenses - annualMortgage)) / inputs.purchasePrice * 100;

    const results = [
        {
            label: 'Monthly Cash Flow',
            value: monthlyCashFlow,
            detail: `Net income after all expenses`
        },
        {
            label: 'Cash-on-Cash Return',
            value: cashOnCash,
            detail: `Annual cash flow / Total investment`,
            isPercentage: true
        },
        {
            label: 'Cap Rate',
            value: capRate,
            detail: `Net Operating Income / Property Value`,
            isPercentage: true
        },
        {
            label: 'Total ROI (5 Year)',
            value: totalReturn,
            detail: `Including appreciation and cash flow`,
            isPercentage: true
        },
        {
            label: 'Debt Service Coverage Ratio',
            value: dscr,
            detail: `Income / Debt obligations (>1.25 is good)`,
            isRatio: true
        },
        {
            label: 'Gross Rent Multiplier',
            value: grossRentMultiplier,
            detail: `Price / Annual Rent (lower is better)`,
            isRatio: true
        },
        {
            label: 'Equity Created',
            value: equityCreated,
            detail: `Through forced appreciation (rehab)`
        },
        {
            label: 'BRRRR Refinance Potential',
            value: refiPotential,
            detail: `Maximum refinance amount at 75% LTV`
        }
    ];

    displayInvestmentResults('investmentResults', results);
}

// Helper functions
function displayResults(containerId, results) {
    const container = document.getElementById(containerId);
    container.style.display = 'block';
    
    container.innerHTML = results.map(result => `
        <div class="result-row">
            <div>
                <div class="result-label">${result.label}</div>
                <div class="result-detail">${result.detail}</div>
            </div>
            <div class="result-value">${formatCurrency(result.value)}</div>
        </div>
    `).join('');
}

function displayInvestmentResults(containerId, results) {
    const container = document.getElementById(containerId);
    container.style.display = 'block';
    
    container.innerHTML = results.map(result => `
        <div class="result-row">
            <div>
                <div class="result-label">${result.label}</div>
                <div class="result-detail">${result.detail}</div>
            </div>
            <div class="result-value">
                ${result.isPercentage ? formatPercent(result.value) :
                  result.isRatio ? formatRatio(result.value) :
                  formatCurrency(result.value)}
            </div>
        </div>
    `).join('');
}

function formatCurrency(amount) {
    return new Intl.NumberFormat('en-US', {
        style: 'currency',
        currency: 'USD',
        minimumFractionDigits: 0,
        maximumFractionDigits: 0
    }).format(amount);
}

function formatPercent(value) {
    return value.toFixed(2) + '%';
}

function formatRatio(value) {
    return value.toFixed(2) + 'x';
}

function getFloat(elementId) {
    return parseFloat(document.getElementById(elementId).value) || 0;
}

function toggleHelp(elementId) {
    const element = document.getElementById(elementId);
    if (element.style.display === 'none') {
        element.style.display = 'block';
    } else {
        element.style.display = 'none';
    }
}

// Event listeners
document.addEventListener('DOMContentLoaded', function() {
    // Auto-save notes
    ['propertyNotes', 'marketNotes', 'costNotes'].forEach(id => {
        const element = document.getElementById(id);
        if (element) {
            // Load saved notes
            const savedNotes = localStorage.getItem(id);
            if (savedNotes) {
                element.value = savedNotes;
            }
            
            // Save notes as you type
            element.addEventListener('input', function() {
                localStorage.setItem(id, this.value);
            });
        }
    });

    // Update down payment percentage
    const downPaymentInput = document.getElementById('downPayment');
    if (downPaymentInput) {
        downPaymentInput.addEventListener('input', function() {
            const price = parseFloat(document.getElementById('purchasePrice').value) || 0;
            const down = parseFloat(this.value) || 0;
            const percentage = ((down / price) * 100).toFixed(1);
            document.getElementById('downPaymentPercent').textContent = `${percentage}% of purchase price`;
        });
    }

    // Auto-calculate when any input changes
    document.querySelectorAll('input[type="number"]').forEach(input => {
        input.addEventListener('input', function() {
            if (this.closest('#basicForm')) {
                calculateMortgage();
            } else if (this.closest('#investmentForm')) {
                calculateInvestment();
            }
        });
    });

    // Initial calculations
    calculateMortgage();
    calculateInvestment();
}); 