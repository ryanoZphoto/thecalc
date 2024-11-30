class TabManager {
    constructor() {
        this.tabs = {
            'seller-finance': new SellerFinanceCalculator(),
            'deal-analyzer': new DealAnalyzer(),
            'rental-analysis': new RentalCalculator(),
            'flip-calculator': new FlipCalculator(),
            'wholesale': new WholesaleCalculator(),
            'marketing': new MarketingTracker()
        };
        
        this.initializeTabs();
    }

    initializeTabs() {
        const tabButtons = document.querySelectorAll('.tab-button');
        
        tabButtons.forEach(button => {
            button.addEventListener('click', () => {
                const tabId = button.getAttribute('data-tab');
                this.switchTab(tabId);
            });
        });

        // Initialize first tab
        this.switchTab('seller-finance');
    }

    switchTab(tabId) {
        // Hide all tabs
        document.querySelectorAll('.tab-content').forEach(tab => {
            tab.classList.remove('active');
        });

        // Remove active class from all buttons
        document.querySelectorAll('.tab-button').forEach(button => {
            button.classList.remove('active');
        });

        // Show selected tab
        const selectedTab = document.getElementById(tabId);
        const selectedButton = document.querySelector(`[data-tab="${tabId}"]`);

        if (selectedTab && selectedButton) {
            selectedTab.classList.add('active');
            selectedButton.classList.add('active');
            
            // Initialize calculator if needed
            if (this.tabs[tabId]) {
                this.tabs[tabId].initialize();
            }
        }
    }
} 