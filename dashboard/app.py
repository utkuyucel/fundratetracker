from flask import Flask, render_template, jsonify, request
import requests
from datetime import datetime, timedelta
from config import DashboardConfig, get_logger

config = DashboardConfig()
logger = get_logger(__name__)

app = Flask(__name__)

# FastAPI backend URL from config
API_BASE_URL = config.API_BASE_URL

class FedRateDashboard:
    def __init__(self, api_base_url):
        self.api_base_url = api_base_url
    
    def get_latest_rate(self):
        """Get latest Federal Funds Rate"""
        try:
            response = requests.get(f"{self.api_base_url}/api/rates/latest")
            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            logger.error(f"Error fetching latest rate: {e}")
            return None
    
    def get_historical_data(self, start_date=None, end_date=None, limit=500):
        """Get historical rate data"""
        try:
            params = {"limit": limit}
            if start_date:
                params["start_date"] = start_date
            if end_date:
                params["end_date"] = end_date
                
            response = requests.get(f"{self.api_base_url}/api/rates/historical", params=params)
            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            logger.error(f"Error fetching historical data: {e}")
            return {"data": [], "count": 0}

dashboard = FedRateDashboard(API_BASE_URL)

@app.route('/')
def index():
    """Main dashboard page"""
    latest_rate = dashboard.get_latest_rate()
    
    # Get summary stats directly from API endpoint
    try:
        response = requests.get(f"{API_BASE_URL}/api/analytics/summary")
        response.raise_for_status()
        analytics = response.json()
    except requests.RequestException as e:
        logger.error(f"Error fetching analytics: {e}")
        analytics = None
    
    return render_template('dashboard.html', 
                         latest_rate=latest_rate,
                         analytics=analytics)

@app.route('/api/chart-data')
def chart_data():
    """API endpoint for chart data"""
    period = request.args.get('period', '1year')
    
    # Calculate date range based on period
    end_date = datetime.now()
    if period == '1month':
        start_date = end_date - timedelta(days=30)
    elif period == '3months':
        start_date = end_date - timedelta(days=90)
    elif period == '6months':
        start_date = end_date - timedelta(days=180)
    elif period == '1year':
        start_date = end_date - timedelta(days=365)
    elif period == '5years':
        start_date = end_date - timedelta(days=1825)
    else:
        start_date = None
    
    start_str = start_date.strftime('%Y-%m-%d') if start_date else None
    end_str = end_date.strftime('%Y-%m-%d')
    
    historical_data = dashboard.get_historical_data(start_str, end_str)
    
    # Format data for charts
    dates = [item['date'] for item in reversed(historical_data['data'])]
    rates = [item['rate'] for item in reversed(historical_data['data'])]
    rate_changes = [item['rate_change'] for item in reversed(historical_data['data'])]
    
    # Calculate moving averages (if we have enough data)
    ma_30 = []
    ma_90 = []
    ma_365 = []
    
    for i in range(len(rates)):
        # 30-day moving average
        if i >= 29:  # Need at least 30 data points
            ma_30.append(sum(rates[i-29:i+1]) / 30)
        else:
            ma_30.append(None)
        
        # 90-day moving average
        if i >= 89:  # Need at least 90 data points
            ma_90.append(sum(rates[i-89:i+1]) / 90)
        else:
            ma_90.append(None)
        
        # 365-day moving average
        if i >= 364:  # Need at least 365 data points
            ma_365.append(sum(rates[i-364:i+1]) / 365)
        else:
            ma_365.append(None)
    
    chart_data = {
        'dates': dates,
        'rates': rates,
        'rate_changes': rate_changes,
        'moving_averages': {
            'ma_30': ma_30,
            'ma_90': ma_90,
            'ma_365': ma_365
        }
    }
    
    return jsonify(chart_data)

@app.route('/health')
def health():
    """Health check endpoint"""
    return jsonify({
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "service": "Fed Rate Dashboard",
        "api_connection": API_BASE_URL
    })

if __name__ == '__main__':
    app.run(debug=config.DEBUG, host=config.HOST, port=config.PORT)
