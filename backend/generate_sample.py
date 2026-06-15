import pandas as pd
import numpy as np
from datetime import datetime, timedelta

def generate_sales_data():
    # Generate 3 years of daily data ending yesterday
    end_date = datetime(2026, 6, 14)
    start_date = end_date - timedelta(days=365 * 3)
    
    dates = pd.date_range(start=start_date, end=end_date, freq='D')
    
    # Base sales
    base_sales = 1500
    
    # Trend: slow increase over time
    trend = np.linspace(0, 800, len(dates))
    
    # Weekly seasonality: higher on weekends
    weekly = np.array([300 if d.weekday() >= 5 else 0 for d in dates])
    
    # Yearly seasonality: peak in November/December (holiday season)
    yearly = np.array([500 * np.sin(2 * np.pi * (d.timetuple().tm_yday - 300) / 365) for d in dates])
    # shift up the yearly so it doesn't go negative mostly
    yearly = np.where(yearly > 0, yearly, yearly * 0.3)
    
    # Noise
    noise = np.random.normal(0, 100, len(dates))
    
    # Total sales
    sales = base_sales + trend + weekly + yearly + noise
    sales = np.maximum(sales, 0) # No negative sales
    sales = np.round(sales).astype(int)
    
    df = pd.DataFrame({'date': dates.strftime('%Y-%m-%d'), 'sales': sales})
    
    # Save to both frontend and backend sample data directories
    df.to_csv(r"h:\your-project-folder\future interns\task-1\frontend\public\sample_data\retail_sales_sample.csv", index=False)
    df.to_csv(r"h:\your-project-folder\future interns\task-1\backend\sample_data\retail_sales_sample.csv", index=False)
    print("Generated 3-year realistic dataset!")

if __name__ == "__main__":
    generate_sales_data()
