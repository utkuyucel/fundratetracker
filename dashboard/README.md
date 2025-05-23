# Flask Dashboard for Federal Funds Rate Analytics

A beautiful, interactive web dashboard for visualizing Federal Reserve interest rate data.

## Features

- 📊 **Interactive Time Series Charts** - Plotly.js powered visualizations
- 📈 **Multiple Time Periods** - 1M, 3M, 6M, 1Y, 5Y, and All-time views
- 📋 **Moving Averages** - 30-day, 90-day and 365-day moving averages
- 🎨 **Modern UI** - Bootstrap 5 with custom styling
- 📱 **Responsive Design** - Works on desktop, tablet, and mobile
- 🔄 **Live Data** - Connects to FastAPI backend for real-time data

## Architecture

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Flask App     │───►│   FastAPI       │───►│   PostgreSQL    │
│   Dashboard     │    │   Backend       │    │   Database      │
│   (Port 5001)   │    │   (Port 8000)   │    │   (Port 5432)   │
└─────────────────┘    └─────────────────┘    └─────────────────┘
```

## Dashboard Features

### Main Dashboard (`/`)
- **Summary Cards**: Current rate, historical high/low, average rate
- **Interactive Time Series Chart**: Federal Funds Rate over time
- **Moving Averages**: 30-day, 90-day, and 365-day averages
- **Period Selector**: Quick filters for different time ranges

## API Endpoints

- `GET /` - Main dashboard page
- `GET /health` - Health check
- `GET /api/chart-data?period=<period>` - Chart data for specified period

### Period Parameters
- `1month` - Last 30 days
- `3months` - Last 90 days  
- `6months` - Last 180 days
- `1year` - Last 365 days
- `5years` - Last 5 years
- `all` - All available data

## Quick Start

### Option 1: Docker (Recommended)

Run the entire system (API backend, database, Redis, and dashboard) using Docker:

```bash
# Navigate to the project root directory
cd /home/utku/fundratetracker

# Start all services with Docker Compose
docker-compose up -d

# Access the dashboard at:
# http://localhost:5001
```

### Option 2: Local Development

#### Prerequisites
- Python 3.11+
- FastAPI backend running on port 8000
- Virtual environment support

#### Installation

1. **Navigate to dashboard directory**:
   ```bash
   cd /home/utku/fundratetracker/dashboard
   ```

2. **Create and activate virtual environment**:
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Start the dashboard**:
   ```bash
   python app.py
   ```

5. **Access the dashboard**:
   - Dashboard: http://localhost:5001
   - Health Check: http://localhost:5001/health

#### Using the Startup Script

Alternatively, use the provided startup script:
```bash
chmod +x run.sh
./run.sh
```

## Dependencies

- **Flask 3.0.0** - Web framework
- **requests 2.31.0** - HTTP client for API calls
- **Bootstrap 5.3.0** - UI framework (CDN)
- **Plotly.js** - Interactive charting (CDN)
- **Font Awesome 6.4.0** - Icons (CDN)

## File Structure

```
dashboard/
├── app.py                 # Main Flask application
├── requirements.txt       # Python dependencies
├── run.sh                # Startup script
├── venv/                 # Virtual environment
├── templates/
│   ├── dashboard.html    # Main dashboard template
│   └── analytics.html    # Analytics page template
└── static/
    ├── css/
    │   └── dashboard.css # Custom styles
    └── js/
        ├── dashboard.js  # Dashboard functionality
        └── analytics.js  # Analytics page functionality
```

## Configuration

### Backend API URL
Edit the `API_BASE_URL` in `app.py` to point to your FastAPI backend:
```python
API_BASE_URL = "http://localhost:8000"
```

### Port Configuration
Change the Flask port in `app.py`:
```python
app.run(debug=True, host='0.0.0.0', port=5000)
```

## Features in Detail

### Time Series Visualization
- **Interactive Charts**: Zoom, pan, hover for details
- **Multiple Periods**: Quick period selection buttons
- **Real-time Updates**: Data refreshes from live API
- **Responsive Design**: Adapts to screen size

### Analytics Dashboard
- **Statistical Summary**: Min, max, average, current rate
- **Moving Averages**: Trend analysis with multiple timeframes
- **Distribution Analysis**: Histogram of rate frequencies
- **Key Insights**: Automated analysis and comparisons

### User Experience
- **Loading States**: Smooth loading indicators
- **Error Handling**: Graceful error messages
- **Mobile-Friendly**: Responsive design for all devices
- **Modern UI**: Clean, professional interface

## Development

### Adding New Features
1. Create new routes in `app.py`
2. Add corresponding templates in `templates/`
3. Add JavaScript functionality in `static/js/`
4. Style with CSS in `static/css/dashboard.cs 
### Debugging
Enable Flask debug mode (already enabled):
```python
app.run(debug=True)
```

### Testing
Test API endpoints:
```bash
# Health check
curl http://localhost:5000/health

# Chart data
curl "http://localhost:5000/api/chart-data?period=1year"
```

## Integration with FastAPI Backend

The Flask dashboard consumes data from the FastAPI backend:

1. **Latest Rate**: `/api/rates/latest`
2. **Historical Data**: `/api/rates/historical`
3. **Analytics Summary**: `/api/analytics/summary`

Ensure the FastAPI backend is running before starting the dashboard.

## Production Deployment

For production deployment:

1. **Use WSGI Server**:
   ```bash
   pip install gunicorn
   gunicorn -w 4 -b 0.0.0.0:5000 app:app
   ```

2. **Environment Variables**:
   ```bash
   export FLASK_ENV=production
   export API_BASE_URL=https://your-api-domain.com
   ```

3. **Reverse Proxy**: Use nginx or similar for static files and SSL

## Troubleshooting

### Common Issues

1. **FastAPI Backend Not Available**:
   - Ensure Docker containers are running: `docker-compose up -d`
   - Check FastAPI health: `curl http://localhost:8000/health`

2. **Module Not Found Errors**:
   - Activate virtual environment: `source venv/bin/activate`
   - Install dependencies: `pip install -r requirements.txt`

3. **Chart Not Loading**:
   - Check browser console for JavaScript errors
   - Verify API endpoints are responding
   - Check network connectivity

4. **Permission Errors**:
   - Make startup script executable: `chmod +x run.sh`
   - Check file permissions in directory

### Log Analysis
Flask logs will show in the terminal. Common patterns:
- `INFO:werkzeug` - Normal HTTP requests
- `ERROR:app` - Application errors
- `WARNING:werkzeug` - Development server warnings

## License

This dashboard is part of the Federal Funds Rate Analytics Platform project.

## Author

**Utku Yucel**
- Email: utkuyucel35@gmail.com
- GitHub: @utkuyucel
