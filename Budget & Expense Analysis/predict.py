import numpy as np
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_absolute_error, r2_score

def predict_next_month(monthly_totals):
    """Predict next month's spending using linear regression"""
    
    if len(monthly_totals) < 2:
        print("⚠️  Not enough data for prediction (need at least 2 months)")
        return None
    
    # Prepare data for regression
    months = np.arange(len(monthly_totals)).reshape(-1, 1)
    amounts = monthly_totals.values
    
    # Create and fit linear regression model
    model = LinearRegression()
    model.fit(months, amounts)
    
    # Make prediction for next month
    next_month = len(monthly_totals)
    prediction = model.predict([[next_month]])[0]
    
    # Calculate model performance metrics
    y_pred = model.predict(months)
    mae = mean_absolute_error(amounts, y_pred)
    r2 = r2_score(amounts, y_pred)
    
    # Print prediction results
    print("🔮 SPENDING PREDICTION:")
    print(f"Predicted spending for next month: £{prediction:.2f}")
    print(f"Model confidence (R²): {r2:.3f}")
    print(f"Average prediction error: £{mae:.2f}")
    
    # Add trend analysis
    trend = "increasing" if model.coef_[0] > 0 else "decreasing"
    trend_strength = "strong" if abs(model.coef_[0]) > 10 else "moderate"
    print(f"Spending trend: {trend_strength} {trend} trend")
    
    # Calculate confidence interval (simple approach)
    residuals = amounts - y_pred
    std_error = np.std(residuals)
    confidence_interval = 1.96 * std_error  # 95% confidence
    
    print(f"95% confidence interval: £{prediction - confidence_interval:.2f} - £{prediction + confidence_interval:.2f}")
    
    return {
        'prediction': prediction,
        'confidence': r2,
        'mae': mae,
        'trend': trend,
        'trend_strength': trend_strength,
        'confidence_interval': confidence_interval
    }

def analyze_trends(monthly_totals):
    """Analyze spending trends and patterns"""
    
    if len(monthly_totals) < 3:
        return
    
    amounts = monthly_totals.values
    
    # Calculate month-over-month changes
    month_over_month = np.diff(amounts)
    
    print("\n📊 TREND ANALYSIS:")
    
    # Overall trend
    if len(month_over_month) > 0:
        avg_change = np.mean(month_over_month)
        if avg_change > 0:
            print(f"Average monthly increase: £{avg_change:.2f}")
        else:
            print(f"Average monthly decrease: £{abs(avg_change):.2f}")
    
    # Volatility
    volatility = np.std(amounts)
    print(f"Spending volatility: £{volatility:.2f}")
    
    # Seasonal patterns (if we have enough data)
    if len(amounts) >= 6:
        # Simple seasonal analysis - compare first half vs second half
        first_half = np.mean(amounts[:len(amounts)//2])
        second_half = np.mean(amounts[len(amounts)//2:])
        
        if abs(first_half - second_half) > volatility * 0.5:
            if first_half > second_half:
                print("📉 Spending appears to be decreasing over time")
            else:
                print("📈 Spending appears to be increasing over time")
        else:
            print("📊 Spending appears to be relatively stable")
