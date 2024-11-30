# Real Estate Calculator Web App

A web-based real estate calculator for comparing different financing scenarios.

## Features
- Seller Financing Calculator
- Scenario Comparison
- Save and Load Scenarios
- Responsive Design

## Local Development
1. Install Python 3.8 or higher
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Run the development server:
   ```bash
   python app.py
   ```
4. Open http://localhost:5000 in your browser

## Deployment to Render (Free Hosting)
1. Create a [Render](https://render.com) account
2. Click "New +" and select "Web Service"
3. Connect your GitHub repository
4. Configure the service:
   - Name: real-estate-calculator
   - Environment: Python 3
   - Build Command: `pip install -r requirements.txt`
   - Start Command: `gunicorn app:app`
5. Click "Create Web Service"

## Deployment to Heroku (Alternative)
1. Create a [Heroku](https://heroku.com) account
2. Install Heroku CLI
3. Login to Heroku:
   ```bash
   heroku login
   ```
4. Create a new Heroku app:
   ```bash
   heroku create your-app-name
   ```
5. Deploy:
   ```bash
   git push heroku main
   ```

## Usage
1. Enter property details in the calculator
2. Click "Calculate" to see results
3. Save scenarios for comparison
4. View and compare saved scenarios

## Contributing
1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request