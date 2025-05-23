# Federal Funds Rate Analytics Platform - Portfolio Project

## Project Overview
A production-ready data engineering project that demonstrates ETL pipelines, containerization, and financial data analytics using Federal Reserve interest rate data from Alpha Vantage API.

## Architecture

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Alpha Vantage │────│  Python ETL     │────│   PostgreSQL    │
│      API        │    │   Pipeline      │    │    Database     │
└─────────────────┘    └─────────────────┘    └─────────────────┘
                              │
                              │
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│     Redis       │────│    FastAPI      │────│   Analytics     │
│    Cache        │    │   Web Server    │    │   Dashboard     │
└─────────────────┘    └─────────────────┘    └─────────────────┘
```

## File Structure
```
fed-rate-analytics/
├── docker-compose.yml
├── Dockerfile
├── .env.example
├── .env
├── README.md
├── app/
│   ├── main.py
│   ├── etl_pipeline.py
│   ├── database.py
│   ├── analytics.py
│   ├── scheduler.py
│   └── requirements.txt
└── sql/
    └── init.sql
```

## Tech Stack
- **Backend**: Python 3.11, FastAPI, SQLAlchemy
- **Database**: PostgreSQL 15
- **Cache**: Redis 7
- **Data Processing**: Pandas, NumPy
- **Containerization**: Docker, Docker Compose
- **API**: Alpha Vantage Federal Reserve Data
- **Scheduling**: Python Schedule

## Features
- ✅ **Automated ETL Pipeline** - Extracts, transforms, and loads Federal Funds Rate data
- ✅ **RESTful API** - Comprehensive endpoints for data access and analytics
- ✅ **Time-Series Analytics** - Moving averages, volatility calculations, statistical summaries
- ✅ **Containerized Architecture** - Production-ready Docker setup
- ✅ **Data Persistence** - PostgreSQL with optimized indexing
- ✅ **Caching Layer** - Redis for performance optimization
- ✅ **Health Monitoring** - API health checks and logging
- ✅ **Scheduled Jobs** - Automated data fetching and processing

## Quick Start

### Prerequisites
- Docker and Docker Compose installed
- Alpha Vantage API key (free at https://www.alphavantage.co/support/#api-key)

### Setup Instructions

1. **Clone and navigate to project**:
   ```bash
   cd /home/utku/fundratetracker/fed-rate-analytics
   ```

2. **Configure environment** (already set up with your API key):
   ```bash
   # .env file is already configured with your Alpha Vantage key
   cat .env
   ```

3. **Launch services**:
   ```bash
   docker-compose up -d
   ```

4. **Wait for services to be ready** (about 30 seconds):
   ```bash
   docker-compose logs -f
   ```

5. **Test the API**:
   ```bash
   curl http://localhost:8000/health
   curl http://localhost:8000/api/pipeline/trigger
   curl http://localhost:8000/api/rates/latest
   ```

## API Endpoints

### Core Endpoints
- `GET /` - API information and version
- `GET /health` - Health check status

### Data Endpoints
- `GET /api/rates/latest` - Get the most recent Federal Funds Rate
- `GET /api/rates/historical` - Historical data with optional date filtering
  - Query params: `start_date`, `end_date`, `limit`
  - Date format: `YYYY-MM-DD`

### Analytics Endpoints
- `GET /api/analytics/summary` - Comprehensive statistical summary
- `GET /api/analytics/moving-averages` - Moving averages (30, 90, 365 days)

### Pipeline Management
- `POST /api/pipeline/trigger` - Manually trigger ETL pipeline

## Example API Usage

```bash
# Get latest rate
curl http://localhost:8000/api/rates/latest

# Get historical data for 2023
curl "http://localhost:8000/api/rates/historical?start_date=2023-01-01&end_date=2023-12-31"

# Get analytics summary
curl http://localhost:8000/api/analytics/summary

# Trigger data refresh
curl -X POST http://localhost:8000/api/pipeline/trigger
```

## Data Schema

### Federal Funds Rates Table
```sql
federal_funds_rates (
    id SERIAL PRIMARY KEY,
    date DATE NOT NULL UNIQUE,
    rate DECIMAL(5,2) NOT NULL,
    rate_change DECIMAL(5,2),
    created_at TIMESTAMP,
    updated_at TIMESTAMP
)
```

### Analytics Table
```sql
rate_analytics (
    id SERIAL PRIMARY KEY,
    calculation_date DATE NOT NULL,
    avg_30_day DECIMAL(5,2),
    avg_90_day DECIMAL(5,2),
    avg_365_day DECIMAL(5,2),
    volatility_30_day DECIMAL(8,4),
    min_rate_ytd DECIMAL(5,2),
    max_rate_ytd DECIMAL(5,2),
    created_at TIMESTAMP
)
```

## Development

### Local Development Setup
```bash
# Install Python dependencies
cd app && pip install -r requirements.txt

# Run database migrations
# (handled automatically by docker-compose)

# Start FastAPI development server
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

### Monitoring and Logs
```bash
# View all service logs
docker-compose logs -f

# View specific service logs
docker-compose logs -f app
docker-compose logs -f postgres
docker-compose logs -f redis

# Check service status
docker-compose ps
```

### Database Access
```bash
# Connect to PostgreSQL
docker exec -it fed_postgres psql -U dataeng -d fed_analytics

# Common queries
SELECT COUNT(*) FROM federal_funds_rates;
SELECT * FROM federal_funds_rates ORDER BY date DESC LIMIT 10;
```

## Portfolio Highlights

### Data Engineering
- **ETL Pipeline**: Robust extract, transform, load process with error handling
- **Data Modeling**: Optimized PostgreSQL schema with proper indexing
- **API Integration**: Professional integration with Alpha Vantage financial API

### Software Architecture
- **Microservices**: Containerized services with clear separation of concerns
- **Scalability**: Redis caching and optimized database queries
- **Reliability**: Health checks, error handling, and comprehensive logging

### DevOps & Production
- **Containerization**: Docker Compose orchestration for local and production deployment
- **Configuration Management**: Environment-based configuration with .env files
- **Monitoring**: Health endpoints and structured logging

### Data Analytics
- **Time-Series Analysis**: Moving averages and volatility calculations
- **Statistical Computing**: NumPy and Pandas for efficient data processing
- **Financial Metrics**: Federal Reserve economic indicators and trends

## Technical Decisions

### Why PostgreSQL?
- Excellent support for time-series data with date indexing
- ACID compliance for financial data integrity
- Mature ecosystem and performance optimization

### Why FastAPI?
- Automatic API documentation with OpenAPI/Swagger
- Type hints and data validation with Pydantic
- High performance and modern Python async support

### Why Redis?
- Fast caching layer for frequently accessed analytics
- Simple key-value storage for computed metrics
- Excellent Docker integration

## Future Enhancements
- [ ] Real-time data streaming with WebSockets
- [ ] Interactive dashboard with Plotly/Dash
- [ ] Machine learning models for rate prediction
- [ ] Kubernetes deployment configuration
- [ ] CI/CD pipeline with GitHub Actions
- [ ] Prometheus metrics and Grafana dashboards

## Author
**Utku Yucel**
- Email: utkuyucel35@gmail.com
- GitHub: @utkuyucel

## License
This project is licensed under the MIT License - see the LICENSE file for details.
