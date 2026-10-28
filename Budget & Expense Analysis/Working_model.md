# Budget & Expense Analysis - Working Model Documentation

## 📋 Table of Contents
1. [System Overview](#system-overview)
2. [Core Components](#core-components)
3. [UK Tax Calculation System](#uk-tax-calculation-system)
4. [Financial Health Algorithm](#financial-health-algorithm)
5. [Prediction Engine](#prediction-engine)
6. [Data Flow & Architecture](#data-flow--architecture)
7. [User Interface Components](#user-interface-components)
8. [Technical Implementation](#technical-implementation)

---

## 🎯 System Overview

The Budget & Expense Analysis web app is a comprehensive financial management tool that:
- **Calculates UK taxes and National Insurance** for 2025-26 tax year
- **Tracks and analyzes expenses** by category and time
- **Predicts future spending** using machine learning
- **Provides financial health scoring** and recommendations
- **Visualizes data** through interactive charts and dashboards

### Key Features:
✅ **Real-time expense tracking**  
✅ **UK tax system integration**  
✅ **ML-powered predictions**  
✅ **Financial health monitoring**  
✅ **Interactive data visualization**  

---

## 🔧 Core Components

### 1. Session State Management
```python
def initialize_session_state():
    if 'expenses' not in st.session_state:
        st.session_state.expenses = []
    if 'categories' not in st.session_state:
        st.session_state.categories = ['Food', 'Transport', 'Entertainment', 'Shopping', 'Bills', 'Other']
    if 'income' not in st.session_state:
        st.session_state.income = 0.0
```
**Purpose**: Maintains user data across Streamlit sessions, ensuring data persistence during app usage.

### 2. Expense Data Structure
Each expense is stored as a dictionary:
```python
expense = {
    'Date': datetime_object,
    'Category': string,
    'Amount': float
}
```

---

## 💷 UK Tax Calculation System

### How It Works:
The app implements the complete UK tax system for 2025-26, converting annual income to monthly take-home pay.

### Tax Calculation Function:
```python
def calculate_uk_tax(gross_income, period='monthly'):
```

### 1. Tax Bands (2025-26):
- **Personal Allowance**: £12,570 (tax-free)
- **Basic Rate (20%)**: £12,571 - £50,270
- **Higher Rate (40%)**: £50,271 - £125,140
- **Additional Rate (45%)**: £125,141+

### 2. National Insurance Rates:
- **12%** on earnings between £12,570 - £50,270
- **2%** on earnings above £50,270

### 3. Calculation Process:

#### Step 1: Convert to Annual
```python
if period == 'monthly':
    annual_income = gross_income * 12
```

#### Step 2: Calculate Income Tax
```python
taxable_income = max(0, annual_income - personal_allowance)

if taxable_income <= (basic_rate_threshold - personal_allowance):
    income_tax = taxable_income * basic_rate
elif taxable_income <= (higher_rate_threshold - personal_allowance):
    basic_tax = (basic_rate_threshold - personal_allowance) * basic_rate
    higher_tax = (taxable_income - (basic_rate_threshold - personal_allowance)) * higher_rate
    income_tax = basic_tax + higher_tax
```

#### Step 3: Calculate National Insurance
```python
if annual_income <= ni_threshold:
    national_insurance = 0
elif annual_income <= ni_upper_threshold:
    national_insurance = (annual_income - ni_threshold) * ni_basic_rate
else:
    ni_basic = (ni_upper_threshold - ni_threshold) * ni_basic_rate
    ni_higher = (annual_income - ni_upper_threshold) * ni_higher_rate
    national_insurance = ni_basic + ni_higher
```

#### Step 4: Calculate Take-Home Pay
```python
annual_take_home = annual_income - income_tax - national_insurance
monthly_take_home = annual_take_home / 12
```

### Example Calculation:
**Annual Salary**: £35,000
1. **Income Tax**: (£35,000 - £12,570) × 20% = £4,486
2. **National Insurance**: (£35,000 - £12,570) × 12% = £2,691.60
3. **Total Deductions**: £4,486 + £2,691.60 = £7,177.60
4. **Annual Take-Home**: £35,000 - £7,177.60 = £27,822.40
5. **Monthly Take-Home**: £27,822.40 ÷ 12 = £2,318.53

---

## 📊 Financial Health Algorithm

### How Financial Health is Calculated:

```python
def calculate_financial_health(income, expenses, category_totals=None):
```

### 1. Basic Metrics:
```python
remaining_balance = income - total_expenses
savings_rate = (remaining_balance / income * 100)
expense_ratio = (total_expenses / income * 100)
```

### 2. Health Score Logic:
```python
if savings_rate >= 20:
    health_score = 100  # Excellent
elif savings_rate >= 10:
    health_score = 75   # Good
elif savings_rate >= 0:
    health_score = 50   # Fair
else:
    health_score = 25   # Poor (overspending)
```

### 3. Category Analysis:
```python
for category, amount in category_totals.items():
    category_ratios[category] = (amount / income * 100)
```

### Health Status Meanings:
- **Excellent (100)**: Saving 20%+ of income
- **Good (75)**: Saving 10-19% of income
- **Fair (50)**: Breaking even (0-9% savings)
- **Poor (25)**: Spending more than earning

---

## 🔮 Prediction Engine

### How Predictions Work:
The app uses **Linear Regression** from scikit-learn to predict next month's spending based on historical data.

### Prediction Function:
```python
def predict_next_month(monthly_totals):
```

### Step-by-Step Process:

#### 1. Data Preparation:
```python
months = np.arange(len(monthly_totals)).reshape(-1, 1)  # X values (time)
amounts = monthly_totals.values                          # Y values (spending)
```

#### 2. Model Training:
```python
model = LinearRegression()
model.fit(months, amounts)
```

#### 3. Make Prediction:
```python
next_month = len(monthly_totals)
prediction = model.predict([[next_month]])[0]
```

#### 4. Calculate Accuracy Metrics:
```python
y_pred = model.predict(months)
mae = mean_absolute_error(amounts, y_pred)    # Mean Absolute Error
r2 = r2_score(amounts, y_pred)               # R² Score (confidence)
```

#### 5. Trend Analysis:
```python
trend = "increasing" if model.coef_[0] > 0 else "decreasing"
trend_strength = "strong" if abs(model.coef_[0]) > 10 else "moderate"
```

#### 6. Confidence Interval:
```python
residuals = amounts - y_pred
std_error = np.std(residuals)
confidence_interval = 1.96 * std_error  # 95% confidence
```

### Prediction Output:
```python
return {
    'prediction': prediction,           # Next month's predicted spending
    'confidence': r2,                  # Model confidence (0-1)
    'mae': mae,                        # Average prediction error
    'trend': trend,                    # "increasing" or "decreasing"
    'trend_strength': trend_strength,  # "strong" or "moderate"
    'confidence_interval': confidence_interval  # ±error range
}
```

### Example Prediction:
**Historical Data**: [£800, £850, £900, £950]
1. **Linear Model**: Finds trend (+£50/month)
2. **Next Month Prediction**: £1,000
3. **Confidence**: 95% (R² = 0.95)
4. **Error Range**: ±£25
5. **Result**: "Next month: £1,000 ± £25"

---

## 🔄 Data Flow & Architecture

### 1. User Input Flow:
```
User Input → Session State → Data Processing → Analysis → Visualization
```

### 2. Tax Calculation Flow:
```
Annual Income → UK Tax Calculation → Monthly Take-Home → Financial Health
```

### 3. Prediction Flow:
```
Historical Expenses → Monthly Grouping → Linear Regression → Future Prediction
```

### 4. Analysis Pipeline:
```python
def analyze_expenses():
    df = pd.DataFrame(st.session_state.expenses)
    df['Date'] = pd.to_datetime(df['Date'])
    df['Month'] = df['Date'].dt.to_period('M')
    
    # Calculate statistics
    total_spent = df['Amount'].sum()
    category_totals = df.groupby('Category')['Amount'].sum()
    monthly_totals = df.groupby('Month')['Amount'].sum()
    
    return analysis_results
```

---

## 🎨 User Interface Components

### 1. Sidebar Controls:
- **Annual Income Input**: Tax calculation trigger
- **Expense Entry**: Date, category, amount inputs
- **Category Management**: Add/remove categories
- **Data Export**: CSV download functionality

### 2. Main Dashboard:
- **Quick Stats**: Total spent, monthly average, transaction count
- **Financial Health**: Health score, savings rate, remaining balance
- **Expense Table**: Interactive expense list with delete buttons

### 3. Analysis Tabs:

#### Tab 1: Charts
- **Pie Chart**: Spending by category
- **Bar Chart**: Category comparison

#### Tab 2: Trends
- **Line Chart**: Monthly spending over time
- **Trend Analysis**: Visual spending patterns

#### Tab 3: Predictions
- **Next Month Forecast**: ML prediction
- **Confidence Metrics**: R², MAE, trend analysis
- **Confidence Interval**: Prediction accuracy range

#### Tab 4: Details
- **Category Breakdown**: Detailed spending by category
- **Monthly Breakdown**: Time-based analysis

#### Tab 5: Income Analysis
- **Tax Breakdown**: Visual tax/NI/take-home split
- **Financial Health Gauge**: Interactive health score
- **Income vs Expenses**: Comprehensive comparison

---

## 🛠️ Technical Implementation

### 1. Libraries Used:
```python
import streamlit as st           # Web app framework
import pandas as pd             # Data manipulation
import plotly.express as px     # Interactive charts
import plotly.graph_objects as go  # Advanced visualizations
import numpy as np              # Numerical computing
from sklearn.linear_model import LinearRegression  # ML predictions
from sklearn.metrics import mean_absolute_error, r2_score  # Model evaluation
```

### 2. Data Processing:
```python
# Convert expenses to DataFrame
df = pd.DataFrame(st.session_state.expenses)
df['Date'] = pd.to_datetime(df['Date'])
df['Month'] = df['Date'].dt.to_period('M')

# Group by category and month
category_totals = df.groupby('Category')['Amount'].sum()
monthly_totals = df.groupby('Month')['Amount'].sum()
```

### 3. Visualization Creation:
```python
# Pie chart for categories
fig = px.pie(values=category_totals.values, 
             names=category_totals.index,
             title="Spending by Category")

# Line chart for trends
fig = go.Figure()
fig.add_trace(go.Scatter(x=months, y=amounts, mode='lines+markers'))
```

### 4. Session State Management:
```python
# Add expense with UI refresh
def add_expense():
    expense = {
        'Date': st.session_state.new_date,
        'Category': st.session_state.new_category,
        'Amount': float(st.session_state.new_amount)
    }
    st.session_state.expenses.append(expense)
    st.rerun()  # Refresh UI
```

---

## 🎯 Key Algorithms Summary

### 1. UK Tax Algorithm:
- **Input**: Annual gross income
- **Process**: Apply tax bands, calculate NI, deduct from gross
- **Output**: Monthly take-home pay

### 2. Financial Health Algorithm:
- **Input**: Take-home income, total expenses, category breakdown
- **Process**: Calculate savings rate, categorize health status
- **Output**: Health score (0-100), status, category ratios

### 3. Prediction Algorithm:
- **Input**: Historical monthly spending data
- **Process**: Linear regression on time series data
- **Output**: Next month prediction with confidence metrics

### 4. Analysis Algorithm:
- **Input**: Raw expense transactions
- **Process**: Group by category/month, calculate statistics
- **Output**: Comprehensive spending analysis

---

## 🔍 Example Walkthrough

### Scenario: User with £35,000 annual salary

#### 1. Tax Calculation:
- **Gross**: £35,000/year
- **Tax**: £4,486/year
- **NI**: £2,692/year
- **Take-Home**: £2,319/month

#### 2. Expense Tracking:
- **Food**: £400/month
- **Transport**: £200/month
- **Entertainment**: £150/month
- **Total**: £750/month

#### 3. Financial Health:
- **Savings**: £2,319 - £750 = £1,569/month
- **Savings Rate**: 67.6%
- **Health Score**: 100 (Excellent)

#### 4. Prediction (after 3 months):
- **Historical**: [£750, £780, £810]
- **Trend**: +£30/month (increasing)
- **Prediction**: £840 next month
- **Confidence**: 95%

---

## 💡 Key Benefits

1. **Accurate Tax Calculations**: Real UK tax rates for precise take-home pay
2. **Predictive Analytics**: ML-powered spending forecasts
3. **Real-Time Health Monitoring**: Instant financial health feedback
4. **Interactive Visualizations**: Easy-to-understand charts and graphs
5. **Comprehensive Analysis**: Category, time-based, and predictive insights

This working model provides a complete financial management solution that combines accurate tax calculations, intelligent predictions, and comprehensive expense analysis in an intuitive web interface.
