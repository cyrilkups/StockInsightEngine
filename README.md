# StockInsightEngine (MarketScope)

A comprehensive Streamlit-based web application for stock market analysis with interactive charts, technical indicators, and data persistence.

## Features

### Core Functionality
- **Interactive Stock Charts**: Candlestick charts with Plotly visualization
- **Volume Analysis**: Volume overlay on secondary y-axis
- **Moving Averages**: Toggleable 50-day and 200-day moving averages
- **Real-time Data**: Live stock data from Yahoo Finance API
- **Multiple Time Periods**: 1 month to 5 years, plus custom date ranges

### Stock Selection
- **Popular Stocks Dropdown**: Pre-configured list of major stocks (AAPL, MSFT, GOOGL, etc.)
- **Manual Entry**: Custom ticker symbol input with validation
- **Smart Navigation**: Quick switching between selection methods

### Company Information
- **Company Overview**: Name, sector, industry, country, exchange
- **Financial Metrics**: Market cap, P/E ratio, dividend yield, 52-week high/low
- **Business Summary**: Detailed company description

### Performance Analytics
- **Return Calculations**: Daily, monthly, YTD, and annualized returns
- **Risk Metrics**: Volatility and Sharpe ratio analysis
- **Distribution Analysis**: Histogram of daily returns

### Data Persistence
- **SQLite Database**: Local data storage with SQLAlchemy ORM
- **Watchlist Management**: Add/remove stocks from personal watchlist
- **Search History**: Track last 6 unique stock searches
- **User Preferences**: Save default settings and preferences

### User Experience
- **Theme Support**: Light and dark mode themes
- **Responsive Design**: Wide layout with organized sidebar
- **Session Management**: Persistent user state across sessions
- **Error Handling**: Comprehensive error handling and graceful fallbacks

## Technical Stack

- **Frontend**: Streamlit web framework
- **Charting**: Plotly for interactive visualizations
- **Data Source**: yfinance API for real-time stock data
- **Database**: SQLite with SQLAlchemy ORM
- **Data Processing**: Pandas and NumPy for calculations

## Installation & Setup

1. **Install Dependencies**:
   ```bash
   pip install streamlit plotly yfinance sqlalchemy pandas numpy
   ```

2. **Run the Application**:
   ```bash
   streamlit run app.py --server.port 5000
   ```

3. **Access the Application**:
   Open your browser to `http://localhost:5000`

## File Structure

