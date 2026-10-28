import pandas as pd
from datetime import datetime
import os
from visualize import create_charts
from predict import predict_next_month

def load_and_clean_data(csv_file):
    """Load CSV data and clean/convert dates"""
    try:
        df = pd.read_csv(csv_file)
        df['Date'] = pd.to_datetime(df['Date'])
        df['Month'] = df['Date'].dt.to_period('M')
        return df
    except FileNotFoundError:
        print(f"Error: File '{csv_file}' not found!")
        return None
    except Exception as e:
        print(f"Error loading data: {e}")
        return None

def analyze_by_category(df):
    """Group by category and calculate totals"""
    category_totals = df.groupby('Category')['Amount'].sum().sort_values(ascending=False)
    return category_totals

def analyze_by_month(df):
    """Group by month and calculate totals"""
    monthly_totals = df.groupby('Month')['Amount'].sum()
    return monthly_totals

def get_current_month_data(df):
    """Get data for the current month"""
    current_month = pd.Timestamp.now().to_period('M')
    current_month_data = df[df['Month'] == current_month]
    return current_month_data, current_month

def generate_summary(df, category_totals, monthly_totals, current_month_data, current_month):
    """Generate and print text summary"""
    print("=" * 50)
    print("💰 BUDGET & EXPENSE ANALYSIS SUMMARY")
    print("=" * 50)
    
    # Overall statistics
    total_spent = df['Amount'].sum()
    avg_monthly = monthly_totals.mean()
    
    print(f"\n📊 OVERALL STATISTICS:")
    print(f"Total spent: £{total_spent:.2f}")
    print(f"Average monthly spend: £{avg_monthly:.2f}")
    print(f"Number of transactions: {len(df)}")
    
    # Current month statistics
    if not current_month_data.empty:
        current_month_total = current_month_data['Amount'].sum()
        print(f"\n📅 CURRENT MONTH ({current_month}):")
        print(f"Total spent this month: £{current_month_total:.2f}")
        print(f"Transactions this month: {len(current_month_data)}")
    else:
        print(f"\n📅 CURRENT MONTH ({current_month}):")
        print("No data for current month")
    
    # Category breakdown
    print(f"\n🏷️  SPENDING BY CATEGORY:")
    for category, amount in category_totals.items():
        percentage = (amount / total_spent) * 100
        print(f"  {category}: £{amount:.2f} ({percentage:.1f}%)")
    
    # Biggest category
    biggest_category = category_totals.index[0]
    biggest_amount = category_totals.iloc[0]
    print(f"\n🔥 BIGGEST SPENDING CATEGORY:")
    print(f"  {biggest_category}: £{biggest_amount:.2f}")
    
    # Monthly trend
    print(f"\n📈 MONTHLY SPENDING TREND:")
    for month, amount in monthly_totals.items():
        print(f"  {month}: £{amount:.2f}")

def main():
    """Main function to run the analysis"""
    csv_file = "sample_expenses.csv"
    
    print("🚀 Starting Budget & Expense Analysis...")
    
    # Load and clean data
    df = load_and_clean_data(csv_file)
    if df is None:
        return
    
    print(f"✅ Loaded {len(df)} transactions from {csv_file}")
    
    # Perform analysis
    category_totals = analyze_by_category(df)
    monthly_totals = analyze_by_month(df)
    current_month_data, current_month = get_current_month_data(df)
    
    # Generate summary
    generate_summary(df, category_totals, monthly_totals, current_month_data, current_month)
    
    # Create visualizations
    print(f"\n📊 Creating charts...")
    create_charts(category_totals, monthly_totals)
    
    # Make prediction
    print(f"\n🔮 Making spending prediction...")
    prediction = predict_next_month(monthly_totals)
    
    print(f"\n✅ Analysis complete! Check the generated charts and prediction.")

if __name__ == "__main__":
    main()
