class RiskAnalyzer:
    def __init__(self):
        self.risk_weights = {
            'documentation': 0.3,
            'compliance': 0.4,
            'enforceability': 0.3,
            'capital': 0.4,
            'cashflow': 0.3,
            'leverage': 0.3,
            'valuation': 0.4,
            'liquidity': 0.3,
            'competition': 0.3,
            'management': 0.3,
            'maintenance': 0.3,
            'tenant': 0.4
        }

    def get_risk_score(self, risk):
        """Convert risk level to score."""
        if isinstance(risk, (int, float)):
            return risk
        risk_scores = {'low': 0.3, 'medium': 0.6, 'high': 0.9}
        return risk_scores.get(risk, 0.5)

    def assess_compliance_requirements(self, strategy):
        """Assess compliance requirements."""
        compliance_levels = {
            'master-lease': 0.6,
            'subject-to': 0.8,
            'wrap': 0.7,
            'lease-option': 0.5
        }
        return compliance_levels.get(strategy, 0.5)

    def assess_enforceability(self, strategy, data):
        """Assess enforceability of the strategy."""
        return 0.5  # Default medium risk

    def assess_capital_requirements(self, strategy, data):
        """Assess capital requirements."""
        return 0.5  # Default medium risk

    def assess_cashflow_risk(self, strategy, data):
        """Assess cashflow risk."""
        return 0.5  # Default medium risk

    def assess_leverage_risk(self, strategy, data):
        """Assess leverage risk."""
        return 0.5  # Default medium risk

    def assess_valuation_risk(self, strategy, data):
        """Assess valuation risk."""
        return 0.5  # Default medium risk

    def assess_liquidity_risk(self, strategy, data):
        """Assess liquidity risk."""
        return 0.5  # Default medium risk

    def assess_competition_risk(self, strategy, data):
        """Assess competition risk."""
        return 0.5  # Default medium risk

    def assess_management_risk(self, strategy, data):
        """Assess management risk."""
        return 0.5  # Default medium risk

    def assess_maintenance_risk(self, strategy, data):
        """Assess maintenance risk."""
        return 0.5  # Default medium risk

    def assess_tenant_risk(self, strategy, data):
        """Assess tenant risk."""
        return 0.5  # Default medium risk

    def analyze_legal_risks(self, strategy, data):
        risks = {
            'documentation': self.assess_documentation_complexity(strategy),
            'compliance': self.assess_compliance_requirements(strategy),
            'enforceability': self.assess_enforceability(strategy, data)
        }
        return self.calculate_risk_level(risks)
    
    def analyze_financial_risks(self, strategy, data):
        risks = {
            'capital': self.assess_capital_requirements(strategy, data),
            'cashflow': self.assess_cashflow_risk(strategy, data),
            'leverage': self.assess_leverage_risk(strategy, data)
        }
        return self.calculate_risk_level(risks)
    
    def analyze_market_risks(self, strategy, data):
        risks = {
            'valuation': self.assess_valuation_risk(strategy, data),
            'liquidity': self.assess_liquidity_risk(strategy, data),
            'competition': self.assess_competition_risk(strategy, data)
        }
        return self.calculate_risk_level(risks)
    
    def analyze_operational_risks(self, strategy, data):
        risks = {
            'management': self.assess_management_risk(strategy, data),
            'maintenance': self.assess_maintenance_risk(strategy, data),
            'tenant': self.assess_tenant_risk(strategy, data)
        }
        return self.calculate_risk_level(risks)

    def calculate_risk_level(self, risks):
        risk_scores = [self.get_risk_score(risk) for risk in risks.values()]
        avg_score = sum(risk_scores) / len(risk_scores)
        
        if avg_score >= 0.7:
            return 'high'
        elif avg_score >= 0.4:
            return 'medium'
        return 'low'

    def assess_documentation_complexity(self, strategy):
        complexity_scores = {
            'master-lease': 0.7,
            'subject-to': 0.8,
            'wrap': 0.9,
            'lease-option': 0.6
        }
        return complexity_scores.get(strategy, 0.5)
    
    # Add more risk assessment methods... 