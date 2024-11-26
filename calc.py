import tkinter as tk
from tkinter import ttk, messagebox
from typing import Dict, Tuple, List
import locale
import json
import os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime
import uuid  # For unique scenario IDs
import webbrowser

# Set up currency formatting
locale.setlocale(locale.LC_ALL, '')

class EmailDialog(tk.Toplevel):
    def __init__(self, parent, callback):
        super().__init__(parent)
        self.callback = callback
        self.title("Send Email")
        self.geometry("400x200")
        
        # Email Address
        email_frame = ttk.Frame(self)
        email_frame.pack(padx=20, pady=10, fill='x')
        
        ttk.Label(email_frame, text="Email Address:").pack(anchor='w')
        self.email_entry = ttk.Entry(email_frame, width=40)
        self.email_entry.pack(fill='x', pady=5)
        
        # Subject
        subject_frame = ttk.Frame(self)
        subject_frame.pack(padx=20, pady=10, fill='x')
        
        ttk.Label(subject_frame, text="Subject:").pack(anchor='w')
        self.subject_entry = ttk.Entry(subject_frame, width=40)
        self.subject_entry.pack(fill='x', pady=5)
        
        # Buttons
        button_frame = ttk.Frame(self)
        button_frame.pack(pady=20)
        
        ttk.Button(button_frame, text="Send", 
                  command=self.send).pack(side='left', padx=10)
        ttk.Button(button_frame, text="Cancel", 
                  command=self.destroy).pack(side='left')

    def send(self):
        email = self.email_entry.get().strip()
        subject = self.subject_entry.get().strip()
        
        if not email:
            messagebox.showerror("Error", "Please enter an email address.")
            return
        
        self.callback(email, subject)
        self.destroy()

class ScenarioManager:
    def __init__(self):
        self.scenarios_file = 'scenarios.json'
        self.load_scenarios()

    def load_scenarios(self):
        try:
            with open(self.scenarios_file, 'r') as f:
                self.scenarios = json.load(f)
        except FileNotFoundError:
            self.scenarios = {}

    def save_scenarios(self):
        with open(self.scenarios_file, 'w') as f:
            json.dump(self.scenarios, f, indent=2)

    def add_scenario(self, name: str, data: dict) -> str:
        scenario_id = str(uuid.uuid4())
        self.scenarios[scenario_id] = {
            'name': name,
            'data': data,
            'created_at': datetime.now().isoformat(),
            'last_modified': datetime.now().isoformat()
        }
        self.save_scenarios()
        return scenario_id

    def get_scenario(self, scenario_id: str) -> dict:
        return self.scenarios.get(scenario_id)

    def delete_scenario(self, scenario_id: str):
        if scenario_id in self.scenarios:
            del self.scenarios[scenario_id]
            self.save_scenarios()

    def get_all_scenarios(self) -> dict:
        return self.scenarios


class SaveScenarioDialog(tk.Toplevel):
    def __init__(self, parent, callback):
        super().__init__(parent)
        self.callback = callback
        self.title("Save Scenario")
        self.geometry("400x150")

        # Scenario Name
        name_frame = ttk.Frame(self)
        name_frame.pack(padx=20, pady=20, fill='x')
        
        ttk.Label(name_frame, text="Scenario Name:").pack(anchor='w')
        self.name_entry = ttk.Entry(name_frame, width=40)
        self.name_entry.pack(fill='x', pady=5)
        
        # Buttons
        button_frame = ttk.Frame(self)
        button_frame.pack(pady=20)
        
        ttk.Button(button_frame, text="Save", 
                  command=self.save).pack(side='left', padx=10)
        ttk.Button(button_frame, text="Cancel", 
                  command=self.destroy).pack(side='left')

    def save(self):
        name = self.name_entry.get().strip()
        if not name:
            messagebox.showerror("Error", "Please enter a scenario name.")
            return
        self.callback(name)
        self.destroy()


class ScenarioComparisonWindow(tk.Toplevel):
    def __init__(self, parent, scenario_manager):
        super().__init__(parent)
        self.scenario_manager = scenario_manager
        self.title("Compare Scenarios")
        self.geometry("1200x800")

        # Create main container
        main_frame = ttk.Frame(self)
        main_frame.pack(expand=True, fill='both', padx=10, pady=5)

        # Scenario Selection Frame
        selection_frame = ttk.LabelFrame(main_frame, text="Select Scenarios to Compare")
        selection_frame.pack(fill='x', padx=5, pady=5)

        # Create scenario selection
        self.scenario_vars = {}
        self.create_scenario_checkboxes(selection_frame)

        # Comparison Results Frame
        self.results_frame = ttk.Frame(main_frame)
        self.results_frame.pack(expand=True, fill='both', padx=5, pady=5)

        # Compare Button
        ttk.Button(main_frame, text="Compare Selected", 
                  command=self.compare_scenarios).pack(pady=10)

    def create_scenario_checkboxes(self, parent):
        scenarios = self.scenario_manager.get_all_scenarios()
        for scenario_id, scenario_data in scenarios.items():
            var = tk.BooleanVar()
            self.scenario_vars[scenario_id] = var
            ttk.Checkbutton(parent, text=scenario_data['name'], 
                          variable=var).pack(anchor='w', padx=5, pady=2)

    def compare_scenarios(self):
        # Clear previous results
        for widget in self.results_frame.winfo_children():
            widget.destroy()

        # Get selected scenarios
        selected_scenarios = [
            (scenario_id, self.scenario_manager.get_scenario(scenario_id))
            for scenario_id, var in self.scenario_vars.items()
            if var.get()
        ]

        if len(selected_scenarios) < 2:
            messagebox.showwarning(
                "Warning", 
                "Please select at least two scenarios to compare."
            )
            return

        # Create comparison table
        self.create_comparison_table(selected_scenarios)

    def create_comparison_table(self, scenarios):
        # Create headers
        headers = ["Metric"] + [s[1]['name'] for s in scenarios]
        for col, header in enumerate(headers):
            ttk.Label(self.results_frame, text=header, 
                     style='Title.TLabel').grid(row=0, column=col, padx=5, pady=5)

        # Define metrics to compare
        metrics = [
            ('Purchase Price', 'sale_price'),
            ('Down Payment', 'down_payment'),
            ('Loan Amount', 'loan_amount'),
            ('Interest Rate', 'rate'),
            ('Monthly Payment', 'monthly_payment'),
            ('Total Cost', 'total_cost')
        ]

        # Add rows for each metric
        for row, (label, key) in enumerate(metrics, start=1):
            ttk.Label(self.results_frame, text=label).grid(
                row=row, column=0, sticky='w', padx=5, pady=2
            )
            for col, (_, scenario) in enumerate(scenarios, start=1):
                value = scenario['data'].get(key, 'N/A')
                if isinstance(value, (int, float)):
                    if key == 'rate':
                        formatted_value = f"{value * 100:.2f}%"
                    else:
                        formatted_value = f"${value:,.2f}"
                else:
                    formatted_value = str(value)
                ttk.Label(self.results_frame, text=formatted_value).grid(
                    row=row, column=col, padx=5, pady=2
                )


class EmailManager:
    def __init__(self):
        self.smtp_server = None
        self.connected = False
        
    def connect_gmail(self, to_email, subject):
        """Open Gmail in default browser with pre-filled recipient and subject"""
        email_url = f'https://mail.google.com/mail/?view=cm&fs=1&to={to_email}&su={subject}'
        webbrowser.open(email_url)
        
    def connect_apple_mail(self, to_email, subject):
        """Open Apple Mail with pre-filled recipient and subject"""
        webbrowser.open(f'mailto:{to_email}?subject={subject}')

class RealEstateCalculator:
    def __init__(self, root):
        self.root = root
        self.root.title("Real Estate Analysis Tool")
        self.root.geometry("1400x800")  # Wider to accommodate middle panel
        
        # Create main container
        self.main_container = ttk.Frame(root)
        self.main_container.pack(expand=True, fill='both', padx=10, pady=5)
        
        # Create three panels
        self.left_panel = ttk.Frame(self.main_container)
        self.left_panel.pack(side='left', expand=True, fill='both', padx=(0, 5))
        
        self.middle_panel = ttk.Frame(self.main_container)
        self.middle_panel.pack(side='left', expand=False, fill='both', padx=5)
        
        self.right_panel = ttk.Frame(self.main_container)
        self.right_panel.pack(side='right', expand=False, fill='both', padx=(5, 0))
        
        # Create notebook for left panel
        self.notebook = ttk.Notebook(self.left_panel)
        self.notebook.pack(expand=True, fill='both')
        
        # Create reference panel in middle
        self.setup_reference_panel()
        
        # Create calculation details panel on right
        self.summary_frame = ttk.LabelFrame(self.right_panel, text="Calculation Details")
        self.summary_frame.pack(expand=True, fill='both')
        self.summary_text = tk.Text(self.summary_frame, width=40, wrap=tk.WORD, 
                                  font=('Consolas', 10))
        self.summary_text.pack(expand=True, fill='both', padx=5, pady=5)
        
        # Create tabs
        self.seller_financing_tab = ttk.Frame(self.notebook)
        self.investment_tab = ttk.Frame(self.notebook)
        self.comparison_tab = ttk.Frame(self.notebook)
        self.closing_costs_tab = ttk.Frame(self.notebook)
        
        self.notebook.add(self.seller_financing_tab, text="Seller Financing")
        self.notebook.add(self.investment_tab, text="Investment Analysis")
        self.notebook.add(self.comparison_tab, text="Loan Comparison")
        self.notebook.add(self.closing_costs_tab, text="Closing Costs")
        
        # Set up tabs
        self.setup_seller_financing_tab()
        self.setup_investment_tab()
        self.setup_comparison_tab()
        self.setup_closing_costs_tab()
        
        # Style
        style = ttk.Style()
        style.configure('Title.TLabel', font=('Helvetica', 12, 'bold'))
        style.configure('Result.TLabel', font=('Helvetica', 10))
        
        # Load saved references
        self.load_references()
        
        # Add Email Button to each tab
        self.add_email_button(self.seller_financing_tab)
        self.add_email_button(self.investment_tab)
        self.add_email_button(self.comparison_tab)
        self.add_email_button(self.closing_costs_tab)
        
        # Add Save Scenario button to each tab
        self.add_scenario_buttons()
        
        self.scenario_manager = ScenarioManager()
        self.email_manager = EmailManager()  # Initialize email manager

    def add_email_button(self, parent):
        """Add email button to the given parent widget."""
        email_frame = ttk.Frame(parent)
        email_frame.pack(side='bottom', pady=5)
        ttk.Button(email_frame, text="Email Results", 
                  command=lambda: self.send_email(parent)).pack()

    def send_email(self, tab):
        """Show email dialog and send calculation results via email."""
        EmailDialog(self.root, self.handle_email_send)

    def handle_email_send(self, to_email, subject):
        """Handle the email sending process after dialog input"""
        try:
            if os.name == 'darwin':  # macOS
                self.email_manager.connect_apple_mail(to_email, subject)
            else:  # Windows/Linux
                self.email_manager.connect_gmail(to_email, subject)
        except Exception as e:
            messagebox.showerror("Error", f"Could not open email client: {str(e)}")

    def setup_reference_panel(self):
        """Create the reference panel with common rates and notes."""
        # Main reference frame
        ref_frame = ttk.LabelFrame(self.middle_panel, text="Reference Information")
        ref_frame.pack(expand=True, fill='both', padx=5, pady=5)
        
        # Property Tax Rates
        tax_frame = ttk.LabelFrame(ref_frame, text="Property Tax Rates")
        tax_frame.pack(fill='x', padx=5, pady=5)
        
        self.tax_notes = tk.Text(tax_frame, height=4, width=30, wrap=tk.WORD)
        self.tax_notes.pack(padx=5, pady=5)
        self.tax_notes.insert('1.0', "Enter local property tax rates here...")
        
        # Insurance Rates
        insurance_frame = ttk.LabelFrame(ref_frame, text="Insurance Rates")
        insurance_frame.pack(fill='x', padx=5, pady=5)
        
        self.insurance_notes = tk.Text(insurance_frame, height=4, width=30, wrap=tk.WORD)
        self.insurance_notes.pack(padx=5, pady=5)
        self.insurance_notes.insert('1.0', "Enter typical insurance rates here...")
        
        # Market Rates
        market_frame = ttk.LabelFrame(ref_frame, text="Current Market Rates")
        market_frame.pack(fill='x', padx=5, pady=5)
        
        self.market_notes = tk.Text(market_frame, height=4, width=30, wrap=tk.WORD)
        self.market_notes.pack(padx=5, pady=5)
        self.market_notes.insert('1.0', "Enter current market rates here...")
        
        # Local Fees
        fees_frame = ttk.LabelFrame(ref_frame, text="Local Fees & Costs")
        fees_frame.pack(fill='x', padx=5, pady=5)
        
        self.fees_notes = tk.Text(fees_frame, height=4, width=30, wrap=tk.WORD)
        self.fees_notes.pack(padx=5, pady=5)
        self.fees_notes.insert('1.0', "Enter common local fees here...")
        
        # Custom Notes
        notes_frame = ttk.LabelFrame(ref_frame, text="Additional Notes")
        notes_frame.pack(fill='x', padx=5, pady=5)
        
        self.custom_notes = tk.Text(notes_frame, height=6, width=30, wrap=tk.WORD)
        self.custom_notes.pack(padx=5, pady=5)
        self.custom_notes.insert('1.0', "Enter any additional notes here...")
        
        # Save Button
        ttk.Button(ref_frame, text="Save References", 
                  command=self.save_references).pack(pady=10)

    def save_references(self):
        """Save reference information to a file."""
        try:
            references = {
                'tax_notes': self.tax_notes.get('1.0', tk.END).strip(),
                'insurance_notes': self.insurance_notes.get('1.0', tk.END).strip(),
                'market_notes': self.market_notes.get('1.0', tk.END).strip(),
                'fees_notes': self.fees_notes.get('1.0', tk.END).strip(),
                'custom_notes': self.custom_notes.get('1.0', tk.END).strip()
            }
            
            with open('references.json', 'w') as f:
                json.dump(references, f)
            
            messagebox.showinfo("Success", "References saved successfully!")
        except Exception as e:
            messagebox.showerror("Error", f"Could not save references: {str(e)}")

    def load_references(self):
        """Load saved reference information."""
        try:
            if os.path.exists('references.json'):
                with open('references.json', 'r') as f:
                    references = json.load(f)
                
                self.tax_notes.delete('1.0', tk.END)
                self.tax_notes.insert('1.0', references.get('tax_notes', ''))
                
                self.insurance_notes.delete('1.0', tk.END)
                self.insurance_notes.insert('1.0', references.get('insurance_notes', ''))
                
                self.market_notes.delete('1.0', tk.END)
                self.market_notes.insert('1.0', references.get('market_notes', ''))
                
                self.fees_notes.delete('1.0', tk.END)
                self.fees_notes.insert('1.0', references.get('fees_notes', ''))
                
                self.custom_notes.delete('1.0', tk.END)
                self.custom_notes.insert('1.0', references.get('custom_notes', ''))
        except Exception as e:
            messagebox.showerror("Error", f"Could not load references: {str(e)}")

    def update_summary(self, text: str):
        """Update the calculation summary panel."""
        self.summary_text.delete(1.0, tk.END)
        self.summary_text.insert(tk.END, text)

    def setup_seller_financing_tab(self):
        # Current Mortgage Frame
        current_frame = ttk.LabelFrame(self.seller_financing_tab, text="Current Mortgage", padding="10")
        current_frame.pack(fill='x', padx=10, pady=5)
        
        ttk.Label(current_frame, text="Original Purchase Price:").grid(row=0, column=0, sticky='w')
        self.original_price = ttk.Entry(current_frame)
        self.original_price.grid(row=0, column=1)
        self.original_price.insert(0, "190000")
        
        ttk.Label(current_frame, text="Interest Rate (%):").grid(row=1, column=0, sticky='w')
        self.current_rate = ttk.Entry(current_frame)
        self.current_rate.grid(row=1, column=1)
        self.current_rate.insert(0, "3.0")
        
        ttk.Label(current_frame, text="Original Loan Term (years):").grid(row=2, column=0, sticky='w')
        self.original_term = ttk.Entry(current_frame)
        self.original_term.grid(row=2, column=1)
        self.original_term.insert(0, "30")
        
        ttk.Label(current_frame, text="Years Remaining:").grid(row=3, column=0, sticky='w')
        self.years_remaining = ttk.Entry(current_frame)
        self.years_remaining.grid(row=3, column=1)
        self.years_remaining.insert(0, "26")
        
        # New Financing Frame
        new_frame = ttk.LabelFrame(self.seller_financing_tab, text="New Seller Financing", padding="10")
        new_frame.pack(fill='x', padx=10, pady=5)
        
        ttk.Label(new_frame, text="Sale Price:").grid(row=0, column=0, sticky='w')
        self.sale_price = ttk.Entry(new_frame)
        self.sale_price.grid(row=0, column=1)
        self.sale_price.insert(0, "420000")
        
        ttk.Label(new_frame, text="Down Payment:").grid(row=1, column=0, sticky='w')
        self.down_payment = ttk.Entry(new_frame)
        self.down_payment.grid(row=1, column=1)
        self.down_payment.insert(0, "50000")
        
        ttk.Label(new_frame, text="Interest Rate (%):").grid(row=2, column=0, sticky='w')
        self.new_rate = ttk.Entry(new_frame)
        self.new_rate.grid(row=2, column=1)
        self.new_rate.insert(0, "1.5")
        
        ttk.Label(new_frame, text="Loan Term (years):").grid(row=3, column=0, sticky='w')
        self.loan_term = ttk.Entry(new_frame)
        self.loan_term.grid(row=3, column=1)
        self.loan_term.insert(0, "30")
        
        ttk.Label(new_frame, text="Balloon Payment Year:").grid(row=4, column=0, sticky='w')
        self.balloon_years = ttk.Entry(new_frame)
        self.balloon_years.grid(row=4, column=1)
        self.balloon_years.insert(0, "11")
        
        # Results Frame
        self.results_frame = ttk.LabelFrame(self.seller_financing_tab, text="Results", padding="10")
        self.results_frame.pack(fill='both', expand=True, padx=10, pady=5)
        
        # Calculate Button
        ttk.Button(self.seller_financing_tab, text="Calculate", 
                  command=self.calculate_seller_financing).pack(pady=10)

    def setup_investment_tab(self):
        # Investment Analysis Frame
        analysis_frame = ttk.LabelFrame(self.investment_tab, text="Rental Property Analysis", padding="10")
        analysis_frame.pack(fill='x', padx=10, pady=5)
        
        # Basic Info
        basic_frame = ttk.LabelFrame(analysis_frame, text="Property Information", padding="5")
        basic_frame.pack(fill='x', padx=5, pady=5)
        
        ttk.Label(basic_frame, text="Purchase Price:").grid(row=0, column=0, sticky='w')
        self.inv_purchase_price = ttk.Entry(basic_frame)
        self.inv_purchase_price.grid(row=0, column=1)
        self.inv_purchase_price.insert(0, "420000")
        
        ttk.Label(basic_frame, text="Down Payment:").grid(row=1, column=0, sticky='w')
        self.inv_down_payment = ttk.Entry(basic_frame)
        self.inv_down_payment.grid(row=1, column=1)
        self.inv_down_payment.insert(0, "50000")
        
        ttk.Label(basic_frame, text="Interest Rate (%):").grid(row=2, column=0, sticky='w')
        self.inv_rate = ttk.Entry(basic_frame)
        self.inv_rate.grid(row=2, column=1)
        self.inv_rate.insert(0, "1.5")
        
        # Rental Income
        income_frame = ttk.LabelFrame(analysis_frame, text="Income Analysis", padding="5")
        income_frame.pack(fill='x', padx=5, pady=5)
        
        ttk.Label(income_frame, text="Monthly Rent:").grid(row=0, column=0, sticky='w')
        self.monthly_rent = ttk.Entry(income_frame)
        self.monthly_rent.grid(row=0, column=1)
        self.monthly_rent.insert(0, "2500")
        
        ttk.Label(income_frame, text="Vacancy Rate (%):").grid(row=1, column=0, sticky='w')
        self.vacancy_rate = ttk.Entry(income_frame)
        self.vacancy_rate.grid(row=1, column=1)
        self.vacancy_rate.insert(0, "5")
        
        # Operating Expenses
        expense_frame = ttk.LabelFrame(analysis_frame, text="Annual Operating Expenses", padding="5")
        expense_frame.pack(fill='x', padx=5, pady=5)
        
        ttk.Label(expense_frame, text="Property Tax:").grid(row=0, column=0, sticky='w')
        self.property_tax = ttk.Entry(expense_frame)
        self.property_tax.grid(row=0, column=1)
        self.property_tax.insert(0, "3000")
        
        ttk.Label(expense_frame, text="Insurance:").grid(row=1, column=0, sticky='w')
        self.insurance = ttk.Entry(expense_frame)
        self.insurance.grid(row=1, column=1)
        self.insurance.insert(0, "1200")
        
        ttk.Label(expense_frame, text="Maintenance:").grid(row=2, column=0, sticky='w')
        self.maintenance = ttk.Entry(expense_frame)
        self.maintenance.grid(row=2, column=1)
        self.maintenance.insert(0, "1800")
        
        ttk.Label(expense_frame, text="Utilities:").grid(row=3, column=0, sticky='w')
        self.utilities = ttk.Entry(expense_frame)
        self.utilities.grid(row=3, column=1)
        self.utilities.insert(0, "0")
        
        ttk.Label(expense_frame, text="Property Management (%):").grid(row=4, column=0, sticky='w')
        self.mgmt_fee = ttk.Entry(expense_frame)
        self.mgmt_fee.grid(row=4, column=1)
        self.mgmt_fee.insert(0, "10")
        
        # Appreciation Analysis
        appreciation_frame = ttk.LabelFrame(analysis_frame, text="Appreciation Analysis", padding="5")
        appreciation_frame.pack(fill='x', padx=5, pady=5)
        
        ttk.Label(appreciation_frame, text="Annual Property Appreciation (%):").grid(row=0, column=0, sticky='w')
        self.appreciation_rate = ttk.Entry(appreciation_frame)
        self.appreciation_rate.grid(row=0, column=1)
        self.appreciation_rate.insert(0, "3")
        
        ttk.Label(appreciation_frame, text="Annual Rent Increase (%):").grid(row=1, column=0, sticky='w')
        self.rent_increase = ttk.Entry(appreciation_frame)
        self.rent_increase.grid(row=1, column=1)
        self.rent_increase.insert(0, "2")
        
        # Results Frame
        self.investment_results_frame = ttk.LabelFrame(self.investment_tab, text="Investment Analysis Results", padding="10")
        self.investment_results_frame.pack(fill='both', expand=True, padx=10, pady=5)
        
        # Calculate Button
        ttk.Button(self.investment_tab, text="Analyze Investment", 
                  command=self.calculate_investment).pack(pady=10)

    def setup_comparison_tab(self):
        # Loan Comparison Frame
        comparison_frame = ttk.LabelFrame(self.comparison_tab, text="Compare Loan Scenarios", padding="10")
        comparison_frame.pack(fill='x', padx=10, pady=5)
        
        ttk.Label(comparison_frame, text="Purchase Price:").grid(row=0, column=0, sticky='w')
        self.compare_price = ttk.Entry(comparison_frame)
        self.compare_price.grid(row=0, column=1)
        self.compare_price.insert(0, "420000")
        
        # Additional loan parameters
        ttk.Label(comparison_frame, text="Points Paid:").grid(row=1, column=0, sticky='w')
        self.points_paid = ttk.Entry(comparison_frame)
        self.points_paid.grid(row=1, column=1)
        self.points_paid.insert(0, "0")
        
        ttk.Label(comparison_frame, text="PMI Required:").grid(row=2, column=0, sticky='w')
        self.pmi_required = ttk.Checkbutton(comparison_frame)
        self.pmi_required.grid(row=2, column=1)
        
        ttk.Label(comparison_frame, text="Tax Rate (%):").grid(row=3, column=0, sticky='w')
        self.tax_rate = ttk.Entry(comparison_frame)
        self.tax_rate.grid(row=3, column=1)
        self.tax_rate.insert(0, "25")
        
        # Early payoff analysis
        payoff_frame = ttk.LabelFrame(comparison_frame, text="Early Payoff Analysis", padding="5")
        payoff_frame.grid(row=4, column=0, columnspan=2, sticky='ew', pady=5)
        
        ttk.Label(payoff_frame, text="Extra Monthly Payment:").grid(row=0, column=0, sticky='w')
        self.extra_payment = ttk.Entry(payoff_frame)
        self.extra_payment.grid(row=0, column=1)
        self.extra_payment.insert(0, "0")
        
        # Results Frame with Scrollbar
        results_container = ttk.Frame(self.comparison_tab)
        results_container.pack(fill='both', expand=True, padx=10, pady=5)
        
        self.comparison_results_frame = ttk.LabelFrame(results_container, text="Comparison Results", padding="10")
        self.comparison_results_frame.pack(fill='both', expand=True)
        
        # Calculate Button
        ttk.Button(self.comparison_tab, text="Compare Scenarios", 
                  command=self.calculate_comparison).pack(pady=10)

    def setup_closing_costs_tab(self):
        # Closing Costs Frame
        costs_frame = ttk.LabelFrame(self.closing_costs_tab, text="Calculate Closing Costs", padding="10")
        costs_frame.pack(fill='x', padx=10, pady=5)
        
        # Property Information
        ttk.Label(costs_frame, text="Purchase Price:").grid(row=0, column=0, sticky='w')
        self.closing_price = ttk.Entry(costs_frame)
        self.closing_price.grid(row=0, column=1)
        self.closing_price.insert(0, "420000")
        
        ttk.Label(costs_frame, text="Loan Amount:").grid(row=1, column=0, sticky='w')
        self.closing_loan = ttk.Entry(costs_frame)
        self.closing_loan.grid(row=1, column=1)
        self.closing_loan.insert(0, "370000")
        
        # Buyer's Prepaid Items
        prepaid_frame = ttk.LabelFrame(costs_frame, text="Prepaid Items", padding="5")
        prepaid_frame.grid(row=2, column=0, columnspan=2, sticky='ew', pady=5)
        
        ttk.Label(prepaid_frame, text="Months of Insurance:").grid(row=0, column=0, sticky='w')
        self.prepaid_insurance = ttk.Entry(prepaid_frame)
        self.prepaid_insurance.grid(row=0, column=1)
        self.prepaid_insurance.insert(0, "12")
        
        ttk.Label(prepaid_frame, text="Months of Tax:").grid(row=1, column=0, sticky='w')
        self.prepaid_tax = ttk.Entry(prepaid_frame)
        self.prepaid_tax.grid(row=1, column=1)
        self.prepaid_tax.insert(0, "6")
        
        # Title and Recording
        title_frame = ttk.LabelFrame(costs_frame, text="Title and Recording", padding="5")
        title_frame.grid(row=3, column=0, columnspan=2, sticky='ew', pady=5)
        
        ttk.Label(title_frame, text="Title Insurance Rate (%):").grid(row=0, column=0, sticky='w')
        self.title_rate = ttk.Entry(title_frame)
        self.title_rate.grid(row=0, column=1)
        self.title_rate.insert(0, "0.5")
        
        # Results Frame
        self.closing_results_frame = ttk.LabelFrame(self.closing_costs_tab, text="Closing Costs", padding="10")
        self.closing_results_frame.pack(fill='both', expand=True, padx=10, pady=5)
        
        # Calculate Button
        ttk.Button(self.closing_costs_tab, text="Calculate Costs", 
                  command=self.calculate_closing_costs).pack(pady=10)

    def calculate_monthly_payment(self, principal: float, annual_rate: float, years: int) -> float:
        monthly_rate = annual_rate / 12
        num_payments = years * 12
        
        if monthly_rate == 0:
            return principal / num_payments
        
        return principal * (monthly_rate * (1 + monthly_rate)**num_payments) / \
               ((1 + monthly_rate)**num_payments - 1)

    def calculate_loan_balance(self, original_principal: float, annual_rate: float, 
                             original_term: int, years_elapsed: int) -> float:
        """Calculate remaining balance based on original term and years elapsed."""
        monthly_rate = annual_rate / 12
        monthly_payment = self.calculate_monthly_payment(original_principal, annual_rate, original_term)
        
        remaining_balance = original_principal
        months_elapsed = years_elapsed * 12
        
        for _ in range(months_elapsed):
            interest = remaining_balance * monthly_rate
            principal_paid = monthly_payment - interest
            remaining_balance -= principal_paid
        
        return remaining_balance

    def format_currency(self, amount: float) -> str:
        return locale.currency(amount, grouping=True)

    def format_percent(self, amount: float) -> str:
        return f"{amount:.2f}%"

    def calculate_seller_financing(self):
        try:
            summary = []
            summary.append("=== Current Mortgage Calculations ===\n")
            
            # Get current mortgage values
            original_price = float(self.original_price.get())
            current_rate = float(self.current_rate.get()) / 100
            original_term = int(self.original_term.get())
            years_remaining = int(self.years_remaining.get())
            years_elapsed = original_term - years_remaining
            
            # Calculate current mortgage details
            monthly_rate = current_rate / 12
            original_payment = self.calculate_monthly_payment(original_price, current_rate, original_term)
            
            summary.append(f"Original Loan Amount: {self.format_currency(original_price)}")
            summary.append(f"Annual Interest Rate: {current_rate*100:.2f}%")
            summary.append(f"Monthly Interest Rate: {monthly_rate*100:.3f}%")
            summary.append(f"Original Monthly Payment: {self.format_currency(original_payment)}")
            summary.append(f"Years Elapsed: {years_elapsed}")
            summary.append(f"Payments Made: {years_elapsed * 12}")
            
            # Calculate current balance
            current_balance = self.calculate_loan_balance(
                original_price, 
                current_rate,
                original_term,
                years_elapsed
            )
            
            total_paid = original_payment * (years_elapsed * 12)
            interest_paid = total_paid - (original_price - current_balance)
            
            summary.append(f"Total Amount Paid: {self.format_currency(total_paid)}")
            summary.append(f"Principal Paid: {self.format_currency(original_price - current_balance)}")
            summary.append(f"Interest Paid: {self.format_currency(interest_paid)}")
            summary.append(f"Current Balance: {self.format_currency(current_balance)}\n")
            
            # Get new financing values
            summary.append("=== New Financing Calculations ===\n")
            
            sale_price = float(self.sale_price.get())
            down_payment = float(self.down_payment.get())
            new_rate = float(self.new_rate.get()) / 100
            loan_term = int(self.loan_term.get())
            balloon_years = int(self.balloon_years.get())
            
            summary.append(f"Sale Price: {self.format_currency(sale_price)}")
            summary.append(f"Down Payment: {self.format_currency(down_payment)}")
            summary.append(f"Loan Amount: {self.format_currency(sale_price - down_payment)}")
            summary.append(f"Interest Rate: {new_rate*100:.2f}%")
            summary.append(f"Monthly Rate: {(new_rate/12)*100:.3f}%")
            
            # Calculate new financing
            loan_amount = sale_price - down_payment
            monthly_payment = self.calculate_monthly_payment(loan_amount, new_rate, loan_term)
            
            summary.append(f"Monthly Payment: {self.format_currency(monthly_payment)}")
            
            # Calculate balloon payment
            remaining_balance = loan_amount
            total_interest = 0
            total_principal = 0
            
            for month in range(balloon_years * 12):
                interest = remaining_balance * new_rate / 12
                principal_paid = monthly_payment - interest
                remaining_balance -= principal_paid
                total_interest += interest
                total_principal += principal_paid
            
            total_payments = monthly_payment * (balloon_years * 12)
            
            summary.append(f"\nAfter {balloon_years} years ({balloon_years * 12} payments):")
            summary.append(f"Total Payments Made: {self.format_currency(total_payments)}")
            summary.append(f"Total Principal Paid: {self.format_currency(total_principal)}")
            summary.append(f"Total Interest Paid: {self.format_currency(total_interest)}")
            summary.append(f"Balloon Payment: {self.format_currency(remaining_balance)}")
            summary.append(f"\nTotal Cost Breakdown:")
            summary.append(f"Down Payment: {self.format_currency(down_payment)}")
            summary.append(f"Total Payments: {self.format_currency(total_payments)}")
            summary.append(f"Balloon Payment: {self.format_currency(remaining_balance)}")
            summary.append(f"Total Cost: {self.format_currency(total_payments + down_payment + remaining_balance)}")
            
            # Update summary panel
            self.update_summary("\n".join(summary))
            
            # Clear previous results
            for widget in self.results_frame.winfo_children():
                widget.destroy()
            
            # Display results
            ttk.Label(self.results_frame, text="Current Mortgage:", style='Title.TLabel').pack(anchor='w')
            ttk.Label(self.results_frame, 
                     text=f"Original Term: {original_term} years ({years_remaining} years remaining)", 
                     style='Result.TLabel').pack(anchor='w')
            ttk.Label(self.results_frame, 
                     text=f"Current Balance: {self.format_currency(current_balance)}", 
                     style='Result.TLabel').pack(anchor='w')
            
            ttk.Label(self.results_frame, text="\nNew Financing:", style='Title.TLabel').pack(anchor='w')
            ttk.Label(self.results_frame, 
                     text=f"Monthly Payment: {self.format_currency(monthly_payment)}", 
                     style='Result.TLabel').pack(anchor='w')
            ttk.Label(self.results_frame, 
                     text=f"Balloon Payment (Year {balloon_years}): {self.format_currency(remaining_balance)}", 
                     style='Result.TLabel').pack(anchor='w')
            
            ttk.Label(self.results_frame, text="\nPayment Totals:", style='Title.TLabel').pack(anchor='w')
            ttk.Label(self.results_frame, 
                     text=f"Total Payments: {self.format_currency(total_payments)}", 
                     style='Result.TLabel').pack(anchor='w')
            ttk.Label(self.results_frame, 
                     text=f"Total Cost: {self.format_currency(total_payments + down_payment + remaining_balance)}", 
                     style='Result.TLabel').pack(anchor='w')
            
        except ValueError as e:
            messagebox.showerror("Error", "Please enter valid numbers in all fields.")

    def calculate_investment(self):
        try:
            summary = []
            summary.append("=== Investment Property Analysis ===\n")
            
            # Get basic property information
            purchase_price = float(self.inv_purchase_price.get())
            down_payment = float(self.inv_down_payment.get())
            rate = float(self.inv_rate.get()) / 100
            loan_amount = purchase_price - down_payment
            
            # Get income information
            monthly_rent = float(self.monthly_rent.get())
            vacancy_rate = float(self.vacancy_rate.get()) / 100
            
            # Calculate effective gross income
            annual_rent = monthly_rent * 12
            vacancy_loss = annual_rent * vacancy_rate
            effective_gross_income = annual_rent - vacancy_loss
            
            # Get operating expenses
            property_tax = float(self.property_tax.get())
            insurance = float(self.insurance.get())
            maintenance = float(self.maintenance.get())
            utilities = float(self.utilities.get())
            mgmt_fee = float(self.mgmt_fee.get()) / 100 * effective_gross_income
            
            # Calculate loan payment
            monthly_payment = self.calculate_monthly_payment(loan_amount, rate, 30)
            annual_debt_service = monthly_payment * 12
            
            # Calculate operating expenses
            total_expenses = property_tax + insurance + maintenance + utilities + mgmt_fee
            
            # Calculate NOI and cash flow
            noi = effective_gross_income - total_expenses
            cash_flow = noi - annual_debt_service
            
            # Calculate returns
            cap_rate = (noi / purchase_price) * 100
            cash_on_cash = (cash_flow / down_payment) * 100
            
            # Calculate DSCR
            dscr = noi / annual_debt_service
            
            # Operating expense ratio
            expense_ratio = (total_expenses / effective_gross_income) * 100
            
            # Appreciation analysis
            appreciation_rate = float(self.appreciation_rate.get()) / 100
            rent_increase = float(self.rent_increase.get()) / 100
            
            # 5-year projection
            summary.append("Property Information:")
            summary.append(f"Purchase Price: {self.format_currency(purchase_price)}")
            summary.append(f"Down Payment: {self.format_currency(down_payment)} ({down_payment/purchase_price*100:.1f}%)")
            summary.append(f"Loan Amount: {self.format_currency(loan_amount)}")
            summary.append(f"Interest Rate: {rate*100:.2f}%")
            summary.append(f"Monthly Payment: {self.format_currency(monthly_payment)}\n")
            
            summary.append("Income Analysis:")
            summary.append(f"Monthly Rent: {self.format_currency(monthly_rent)}")
            summary.append(f"Annual Rent: {self.format_currency(annual_rent)}")
            summary.append(f"Vacancy Loss: {self.format_currency(vacancy_loss)}")
            summary.append(f"Effective Gross Income: {self.format_currency(effective_gross_income)}\n")
            
            summary.append("Operating Expenses:")
            summary.append(f"Property Tax: {self.format_currency(property_tax)}")
            summary.append(f"Insurance: {self.format_currency(insurance)}")
            summary.append(f"Maintenance: {self.format_currency(maintenance)}")
            summary.append(f"Utilities: {self.format_currency(utilities)}")
            summary.append(f"Property Management: {self.format_currency(mgmt_fee)}")
            summary.append(f"Total Operating Expenses: {self.format_currency(total_expenses)}")
            summary.append(f"Operating Expense Ratio: {expense_ratio:.1f}%\n")
            
            summary.append("Financial Metrics:")
            summary.append(f"Net Operating Income (NOI): {self.format_currency(noi)}")
            summary.append(f"Annual Debt Service: {self.format_currency(annual_debt_service)}")
            summary.append(f"Annual Cash Flow: {self.format_currency(cash_flow)}")
            summary.append(f"Monthly Cash Flow: {self.format_currency(cash_flow/12)}")
            summary.append(f"Cap Rate: {cap_rate:.2f}%")
            summary.append(f"Cash on Cash Return: {cash_on_cash:.2f}%")
            summary.append(f"Debt Service Coverage Ratio: {dscr:.2f}\n")
            
            summary.append("5-Year Projection:")
            property_value = purchase_price
            current_rent = monthly_rent
            
            for year in range(1, 6):
                property_value *= (1 + appreciation_rate)
                current_rent *= (1 + rent_increase)
                equity = property_value - loan_amount
                
                summary.append(f"\nYear {year}:")
                summary.append(f"Property Value: {self.format_currency(property_value)}")
                summary.append(f"Monthly Rent: {self.format_currency(current_rent)}")
                summary.append(f"Equity: {self.format_currency(equity)}")
                summary.append(f"Return on Equity: {(cash_flow/equity)*100:.2f}%")
            
            # Update summary panel
            self.update_summary("\n".join(summary))
            
            # Clear previous results
            for widget in self.investment_results_frame.winfo_children():
                widget.destroy()
            
            # Display key metrics in results frame
            ttk.Label(self.investment_results_frame, text="Key Investment Metrics:", 
                     style='Title.TLabel').pack(anchor='w')
            ttk.Label(self.investment_results_frame, 
                     text=f"Monthly Cash Flow: {self.format_currency(cash_flow/12)}", 
                     style='Result.TLabel').pack(anchor='w')
            ttk.Label(self.investment_results_frame, 
                     text=f"Cap Rate: {cap_rate:.2f}%", 
                     style='Result.TLabel').pack(anchor='w')
            ttk.Label(self.investment_results_frame, 
                     text=f"Cash on Cash Return: {cash_on_cash:.2f}%", 
                     style='Result.TLabel').pack(anchor='w')
            ttk.Label(self.investment_results_frame, 
                     text=f"DSCR: {dscr:.2f}", 
                     style='Result.TLabel').pack(anchor='w')
            
        except ValueError as e:
            messagebox.showerror("Error", "Please enter valid numbers in all fields.")

    def calculate_comparison(self):
        try:
            summary = []
            summary.append("=== Loan Comparison Analysis ===\n")
            
            purchase_price = float(self.compare_price.get())
            points_paid = float(self.points_paid.get())
            tax_rate = float(self.tax_rate.get()) / 100
            extra_payment = float(self.extra_payment.get())
            
            # Define scenarios
            down_payments = [
                purchase_price * 0.12,  # 12%
                purchase_price * 0.20,  # 20%
                purchase_price * 0.30   # 30%
            ]
            interest_rates = [0.015, 0.02, 0.025]  # 1.5%, 2%, 2.5%
            
            # Clear previous results
            for widget in self.comparison_results_frame.winfo_children():
                widget.destroy()
            
            # Create headers
            headers = ["Down Payment", "Rate", "Monthly", "Total Interest", "Years to Pay"]
            for col, header in enumerate(headers):
                ttk.Label(self.comparison_results_frame, text=header, 
                         style='Title.TLabel').grid(row=0, column=col, padx=5, pady=5)
            
            row = 1
            scenarios = []
            
            for down_payment in down_payments:
                for rate in interest_rates:
                    loan_amount = purchase_price - down_payment
                    base_payment = self.calculate_monthly_payment(loan_amount, rate, 30)
                    
                    # Calculate with extra payment
                    total_payment = base_payment + extra_payment
                    remaining_balance = loan_amount
                    months = 0
                    total_interest = 0
                    
                    while remaining_balance > 0 and months < 360:
                        interest = remaining_balance * (rate / 12)
                        total_interest += interest
                        principal = total_payment - interest
                        remaining_balance -= principal
                        months += 1
                    
                    years_to_pay = months / 12
                    
                    # Calculate tax savings
                    first_year_interest = loan_amount * rate
                    tax_savings = first_year_interest * tax_rate
                    
                    # Points cost
                    points_cost = loan_amount * (points_paid / 100)
                    
                    # PMI (if down payment < 20%)
                    pmi_required = down_payment < (purchase_price * 0.2)
                    monthly_pmi = (loan_amount * 0.005) / 12 if pmi_required else 0
                    
                    scenario = {
                        'down_payment': down_payment,
                        'down_payment_percent': (down_payment / purchase_price) * 100,
                        'rate': rate * 100,
                        'monthly_payment': base_payment,
                        'total_payment': total_payment,
                        'total_interest': total_interest,
                        'years_to_pay': years_to_pay,
                        'tax_savings': tax_savings,
                        'points_cost': points_cost,
                        'monthly_pmi': monthly_pmi
                    }
                    scenarios.append(scenario)
                    
                    # Display in grid
                    ttk.Label(self.comparison_results_frame, 
                             text=f"{self.format_currency(down_payment)} ({scenario['down_payment_percent']:.1f}%)", 
                             style='Result.TLabel').grid(row=row, column=0, padx=5, pady=2)
                    ttk.Label(self.comparison_results_frame, 
                             text=f"{rate*100:.1f}%", 
                             style='Result.TLabel').grid(row=row, column=1, padx=5, pady=2)
                    ttk.Label(self.comparison_results_frame, 
                             text=self.format_currency(base_payment), 
                             style='Result.TLabel').grid(row=row, column=2, padx=5, pady=2)
                    ttk.Label(self.comparison_results_frame, 
                             text=self.format_currency(total_interest), 
                             style='Result.TLabel').grid(row=row, column=3, padx=5, pady=2)
                    ttk.Label(self.comparison_results_frame, 
                             text=f"{years_to_pay:.1f}", 
                             style='Result.TLabel').grid(row=row, column=4, padx=5, pady=2)
                    row += 1
            
            # Add detailed analysis to summary
            summary.append("Scenario Details:\n")
            for scenario in scenarios:
                summary.append(f"Down Payment: {self.format_currency(scenario['down_payment'])} "
                             f"({scenario['down_payment_percent']:.1f}%)")
                summary.append(f"Interest Rate: {scenario['rate']:.1f}%")
                summary.append(f"Base Monthly Payment: {self.format_currency(scenario['monthly_payment'])}")
                if extra_payment > 0:
                    summary.append(f"Extra Monthly Payment: {self.format_currency(extra_payment)}")
                    summary.append(f"Total Monthly Payment: {self.format_currency(scenario['total_payment'])}")
                summary.append(f"Years to Pay: {scenario['years_to_pay']:.1f}")
                summary.append(f"Total Interest: {self.format_currency(scenario['total_interest'])}")
                summary.append(f"First Year Tax Savings: {self.format_currency(scenario['tax_savings'])}")
                if scenario['monthly_pmi'] > 0:
                    summary.append(f"Monthly PMI: {self.format_currency(scenario['monthly_pmi'])}")
                if points_paid > 0:
                    summary.append(f"Points Cost: {self.format_currency(scenario['points_cost'])}")
                summary.append("")
            
            # Update summary panel
            self.update_summary("\n".join(summary))
            
        except ValueError as e:
            messagebox.showerror("Error", "Please enter valid numbers in all fields.")

    def calculate_closing_costs(self):
        try:
            summary = []
            summary.append("=== Closing Costs Analysis ===\n")
            
            # Get values
            purchase_price = float(self.closing_price.get())
            loan_amount = float(self.closing_loan.get())
            prepaid_insurance_months = float(self.prepaid_insurance.get())
            prepaid_tax_months = float(self.prepaid_tax.get())
            title_rate = float(self.title_rate.get()) / 100
            
            # Calculate buyer's costs
            loan_origination = loan_amount * 0.01
            appraisal_fee = 500
            credit_report = 50
            tax_service = 75
            flood_certification = 25
            title_insurance = purchase_price * title_rate
            recording_fees = 250
            
            # Calculate prepaids
            insurance_rate = purchase_price * 0.003  # Estimated annual rate
            tax_rate = purchase_price * 0.015  # Estimated annual rate
            prepaid_insurance = (insurance_rate / 12) * prepaid_insurance_months
            prepaid_tax = (tax_rate / 12) * prepaid_tax_months
            
            # Calculate escrow/impounds
            escrow_insurance = (insurance_rate / 12) * 2  # 2 months cushion
            escrow_tax = (tax_rate / 12) * 2  # 2 months cushion
            
            # Calculate seller's costs
            realtor_fees = purchase_price * 0.06
            transfer_tax = purchase_price * 0.001
            seller_other_fees = 500
            
            # Calculate totals
            total_buyer_closing = (loan_origination + appraisal_fee + credit_report + 
                                 tax_service + flood_certification + title_insurance + 
                                 recording_fees)
            total_prepaids = prepaid_insurance + prepaid_tax
            total_escrow = escrow_insurance + escrow_tax
            total_seller_costs = realtor_fees + transfer_tax + seller_other_fees
            
            # Clear previous results
            for widget in self.closing_results_frame.winfo_children():
                widget.destroy()
            
            # Build summary
            summary.append("Buyer's Closing Costs:")
            summary.append(f"Loan Origination: {self.format_currency(loan_origination)}")
            summary.append(f"Appraisal: {self.format_currency(appraisal_fee)}")
            summary.append(f"Credit Report: {self.format_currency(credit_report)}")
            summary.append(f"Tax Service: {self.format_currency(tax_service)}")
            summary.append(f"Flood Certification: {self.format_currency(flood_certification)}")
            summary.append(f"Title Insurance: {self.format_currency(title_insurance)}")
            summary.append(f"Recording Fees: {self.format_currency(recording_fees)}")
            summary.append(f"Total Closing Costs: {self.format_currency(total_buyer_closing)}\n")
            
            summary.append("Prepaids:")
            summary.append(f"Insurance ({prepaid_insurance_months} months): "
                         f"{self.format_currency(prepaid_insurance)}")
            summary.append(f"Property Tax ({prepaid_tax_months} months): "
                         f"{self.format_currency(prepaid_tax)}")
            summary.append(f"Total Prepaids: {self.format_currency(total_prepaids)}\n")
            
            summary.append("Escrow/Impounds:")
            summary.append(f"Insurance Reserves: {self.format_currency(escrow_insurance)}")
            summary.append(f"Tax Reserves: {self.format_currency(escrow_tax)}")
            summary.append(f"Total Escrow: {self.format_currency(total_escrow)}\n")
            
            summary.append("Total Buyer Funds Needed:")
            total_buyer_needed = total_buyer_closing + total_prepaids + total_escrow
            summary.append(f"Total Funds Needed: {self.format_currency(total_buyer_needed)}\n")
            
            summary.append("Seller's Costs:")
            summary.append(f"Realtor Fees: {self.format_currency(realtor_fees)}")
            summary.append(f"Transfer Tax: {self.format_currency(transfer_tax)}")
            summary.append(f"Other Fees: {self.format_currency(seller_other_fees)}")
            summary.append(f"Total Seller Costs: {self.format_currency(total_seller_costs)}")
            
            # Calculate seller's net proceeds
            net_proceeds = purchase_price - total_seller_costs - loan_amount
            summary.append(f"\nSeller's Net Proceeds: {self.format_currency(net_proceeds)}")
            
            # Update summary panel
            self.update_summary("\n".join(summary))
            
            # Display results in frame
            ttk.Label(self.closing_results_frame, text="Buyer's Costs:", 
                     style='Title.TLabel').pack(anchor='w')
            ttk.Label(self.closing_results_frame, 
                     text=f"Closing Costs: {self.format_currency(total_buyer_closing)}", 
                     style='Result.TLabel').pack(anchor='w')
            ttk.Label(self.closing_results_frame, 
                     text=f"Prepaids: {self.format_currency(total_prepaids)}", 
                     style='Result.TLabel').pack(anchor='w')
            ttk.Label(self.closing_results_frame, 
                     text=f"Escrow: {self.format_currency(total_escrow)}", 
                     style='Result.TLabel').pack(anchor='w')
            ttk.Label(self.closing_results_frame, 
                     text=f"Total Funds Needed: {self.format_currency(total_buyer_needed)}", 
                     style='Result.TLabel').pack(anchor='w')
            
            ttk.Label(self.closing_results_frame, text="\nSeller's Costs:", 
                     style='Title.TLabel').pack(anchor='w')
            ttk.Label(self.closing_results_frame, 
                     text=f"Total Costs: {self.format_currency(total_seller_costs)}", 
                     style='Result.TLabel').pack(anchor='w')
            ttk.Label(self.closing_results_frame, 
                     text=f"Net Proceeds: {self.format_currency(net_proceeds)}", 
                     style='Result.TLabel').pack(anchor='w')
            
        except ValueError as e:
            messagebox.showerror("Error", "Please enter valid numbers in all fields.")

    def add_scenario_buttons(self):
        """Add Save Scenario button to each calculator tab."""
        for tab in [self.seller_financing_tab, self.investment_tab, 
                   self.comparison_tab, self.closing_costs_tab]:
            button_frame = ttk.Frame(tab)
            button_frame.pack(side='bottom', pady=10)
            
            ttk.Button(button_frame, text="Save Scenario", 
                      command=lambda t=tab: self.save_scenario(t)).pack(side='left', padx=5)
            ttk.Button(button_frame, text="Compare Scenarios", 
                      command=self.show_comparison).pack(side='left', padx=5)

    def save_scenario(self, tab):
        """Save current calculation as a scenario."""
        # Get current calculation data
        current_data = self.get_current_calculation_data(tab)
        if not current_data:
            return

        # Show save dialog
        SaveScenarioDialog(self.root, 
                          lambda name: self.complete_scenario_save(name, current_data))

    def complete_scenario_save(self, name: str, data: dict):
        """Complete the scenario saving process."""
        try:
            self.scenario_manager.add_scenario(name, data)
            messagebox.showinfo("Success", "Scenario saved successfully!")
        except Exception as e:
            messagebox.showerror("Error", f"Could not save scenario: {str(e)}")

    def get_current_calculation_data(self, tab) -> dict:
        """Get the current calculation data based on the active tab."""
        try:
            if tab == self.seller_financing_tab:
                return {
                    'sale_price': float(self.sale_price.get()),
                    'down_payment': float(self.down_payment.get()),
                    'rate': float(self.new_rate.get()) / 100,
                    'loan_amount': float(self.sale_price.get()) - float(self.down_payment.get()),
                    'monthly_payment': float(self.calculate_monthly_payment(
                        float(self.sale_price.get()) - float(self.down_payment.get()),
                        float(self.new_rate.get()) / 100,
                        30
                    )),
                    'total_cost': float(self.sale_price.get())
                }
            # Add similar data collection for other tabs
            return {}
        except ValueError:
            messagebox.showerror("Error", "Please ensure all fields contain valid numbers.")
            return None

    def show_comparison(self):
        """Show the scenario comparison window."""
        ScenarioComparisonWindow(self.root, self.scenario_manager)


def main():
    root = tk.Tk()
    app = RealEstateCalculator(root)
    root.mainloop()


if __name__ == "__main__":
    main()
