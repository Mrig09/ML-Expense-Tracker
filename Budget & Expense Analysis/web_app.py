import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import numpy as np
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_absolute_error, r2_score
from datetime import datetime, date
import io

# Page configuration
st.set_page_config(
    page_title="💰 Budget & Expense Analysis",
    page_icon="💰",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
st.markdown("""
<style>
    .main-header {
        font-size: 3rem;
        font-weight: bold;
        text-align: center;
        color: #1f77b4;
        margin-bottom: 2rem;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.1);
    }
    .metric-card {
        background-color: #f0f2f6;
        padding: 1rem;
        border-radius: 0.5rem;
        border-left: 4px solid #1f77b4;
    }
    .stButton > button {
        width: 100%;
        background-color: #1f77b4;
        color: white;
        border: none;
        padding: 0.5rem 1rem;
        border-radius: 0.5rem;
        font-weight: bold;
    }
    .stButton > button:hover {
        background-color: #0d5aa7;
    }
    .income-section {
        background-color: #e8f5e8;
        padding: 1rem;
        border-radius: 0.5rem;
        border-left: 4px solid #28a745;
    }
    .financial-health {
        background-color: #fff3cd;
        padding: 1rem;
        border-radius: 0.5rem;
        border-left: 4px solid #ffc107;
    }
</style>
""", unsafe_allow_html=True)

def initialize_session_state():
    """Initialize session state variables"""
    if 'expenses' not in st.session_state:
        st.session_state.expenses = []
    if 'categories' not in st.session_state:
        st.session_state.categories = ['Food', 'Transport', 'Entertainment', 'Shopping', 'Bills', 'Other']
    if 'income' not in st.session_state:
        st.session_state.income = 0.0

def calculate_uk_tax(gross_income, period='monthly'):
    """Calculate UK tax and National Insurance for 2025-26 tax year"""
    
    # Convert to annual if monthly
    if period == 'monthly':
        annual_income = gross_income * 12
    else:
        annual_income = gross_income
    
    # UK Tax Bands 2025-26
    personal_allowance = 12570
    basic_rate_threshold = 50270
    higher_rate_threshold = 125140
    
    # Tax rates
    basic_rate = 0.20
    higher_rate = 0.40
    additional_rate = 0.45
    
    # National Insurance rates
    ni_basic_rate = 0.12
    ni_higher_rate = 0.02
    
    # Calculate Income Tax
    taxable_income = max(0, annual_income - personal_allowance)
    
    if taxable_income <= 0:
        income_tax = 0
    elif taxable_income <= (basic_rate_threshold - personal_allowance):
        income_tax = taxable_income * basic_rate
    elif taxable_income <= (higher_rate_threshold - personal_allowance):
        basic_tax = (basic_rate_threshold - personal_allowance) * basic_rate
        higher_tax = (taxable_income - (basic_rate_threshold - personal_allowance)) * higher_rate
        income_tax = basic_tax + higher_tax
    else:
        basic_tax = (basic_rate_threshold - personal_allowance) * basic_rate
        higher_tax = (higher_rate_threshold - basic_rate_threshold) * higher_rate
        additional_tax = (taxable_income - (higher_rate_threshold - personal_allowance)) * additional_rate
        income_tax = basic_tax + higher_tax + additional_tax
    
    # Calculate National Insurance
    ni_threshold = 12570
    ni_upper_threshold = 50270
    
    if annual_income <= ni_threshold:
        national_insurance = 0
    elif annual_income <= ni_upper_threshold:
        national_insurance = (annual_income - ni_threshold) * ni_basic_rate
    else:
        ni_basic = (ni_upper_threshold - ni_threshold) * ni_basic_rate
        ni_higher = (annual_income - ni_upper_threshold) * ni_higher_rate
        national_insurance = ni_basic + ni_higher
    
    # Calculate take-home salary
    annual_take_home = annual_income - income_tax - national_insurance
    monthly_take_home = annual_take_home / 12
    
    return {
        'gross_income': gross_income,
        'annual_gross': annual_income,
        'income_tax': income_tax / 12 if period == 'monthly' else income_tax,
        'national_insurance': national_insurance / 12 if period == 'monthly' else national_insurance,
        'take_home': monthly_take_home if period == 'monthly' else annual_take_home,
        'annual_take_home': annual_take_home,
        'effective_tax_rate': ((income_tax + national_insurance) / annual_income * 100) if annual_income > 0 else 0
    }

def add_expense():
    """Add expense to the list"""
    if st.session_state.new_amount and st.session_state.new_category and st.session_state.new_date:
        expense = {
            'Date': st.session_state.new_date,
            'Category': st.session_state.new_category,
            'Amount': float(st.session_state.new_amount)
        }
        st.session_state.expenses.append(expense)
        
        st.success("✅ Expense added successfully!")
        st.rerun()

def delete_expense(index):
    """Delete expense at given index"""
    if 0 <= index < len(st.session_state.expenses):
        deleted_expense = st.session_state.expenses.pop(index)
        st.success(f"🗑️ Deleted expense: {deleted_expense['Category']} - £{deleted_expense['Amount']:.2f}")
        st.rerun()

def analyze_expenses():
    """Analyze expenses and return statistics"""
    if not st.session_state.expenses:
        return None
    
    df = pd.DataFrame(st.session_state.expenses)
    df['Date'] = pd.to_datetime(df['Date'])
    df['Month'] = df['Date'].dt.to_period('M')
    
    # Calculate statistics
    total_spent = df['Amount'].sum()
    avg_monthly = df.groupby('Month')['Amount'].sum().mean() if len(df['Month'].unique()) > 0 else 0
    transaction_count = len(df)
    
    # Category analysis
    category_totals = df.groupby('Category')['Amount'].sum().sort_values(ascending=False)
    
    # Monthly analysis
    monthly_totals = df.groupby('Month')['Amount'].sum()
    
    return {
        'df': df,
        'total_spent': total_spent,
        'avg_monthly': avg_monthly,
        'transaction_count': transaction_count,
        'category_totals': category_totals,
        'monthly_totals': monthly_totals
    }

def calculate_financial_health(income, expenses, category_totals=None):
    """Calculate financial health metrics"""
    if income <= 0:
        return None
    
    # Handle both total expenses (number) and category expenses (dict)
    if isinstance(expenses, (int, float)):
        total_expenses = expenses
        # Use category_totals if provided, otherwise empty dict
        if category_totals is None:
            category_totals = {}
    else:
        # If expenses is a dict, calculate total and use it
        total_expenses = sum(expenses.values()) if expenses else 0
        category_totals = expenses
    
    # Basic metrics
    remaining_balance = income - total_expenses
    savings_rate = (remaining_balance / income * 100) if income > 0 else 0
    expense_ratio = (total_expenses / income * 100) if income > 0 else 0
    
    # Spending categories as % of income
    category_ratios = {}
    if category_totals is not None and not (hasattr(category_totals, 'empty') and category_totals.empty) and income > 0:
        for category, amount in category_totals.items():
            category_ratios[category] = (amount / income * 100)
    
    # Financial health score (0-100)
    if savings_rate >= 20:
        health_score = 100
        health_status = "Excellent"
        health_color = "success"
    elif savings_rate >= 10:
        health_score = 75
        health_status = "Good"
        health_color = "success"
    elif savings_rate >= 0:
        health_score = 50
        health_status = "Fair"
        health_color = "warning"
    else:
        health_score = 25
        health_status = "Poor"
        health_color = "error"
    
    return {
        'remaining_balance': remaining_balance,
        'savings_rate': savings_rate,
        'expense_ratio': expense_ratio,
        'category_ratios': category_ratios,
        'health_score': health_score,
        'health_status': health_status,
        'health_color': health_color
    }

def create_pie_chart(category_totals):
    """Create pie chart for spending by category"""
    fig = px.pie(
        values=category_totals.values,
        names=category_totals.index,
        title="Spending by Category",
        color_discrete_sequence=px.colors.qualitative.Set3
    )
    fig.update_traces(textposition='inside', textinfo='percent+label')
    fig.update_layout(height=400, showlegend=False)
    return fig

def create_line_chart(monthly_totals):
    """Create line chart for monthly spending trends"""
    months = [str(m) for m in monthly_totals.index]
    amounts = monthly_totals.values
    
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=months,
        y=amounts,
        mode='lines+markers',
        line=dict(color='#1f77b4', width=3),
        marker=dict(size=8, color='#1f77b4'),
        fill='tonexty',
        fillcolor='rgba(31, 119, 180, 0.3)',
        name='Monthly Spending'
    ))
    
    fig.update_layout(
        title="Monthly Spending Trend",
        xaxis_title="Month",
        yaxis_title="Amount (£)",
        height=400,
        showlegend=False
    )
    
    return fig

def create_bar_chart(category_totals):
    """Create bar chart for spending by category"""
    fig = px.bar(
        x=category_totals.index,
        y=category_totals.values,
        title="Spending by Category",
        color=category_totals.values,
        color_continuous_scale='Blues'
    )
    fig.update_layout(
        xaxis_title="Category",
        yaxis_title="Amount (£)",
        height=400,
        showlegend=False
    )
    return fig

def predict_next_month(monthly_totals):
    """Predict next month's spending using linear regression"""
    if len(monthly_totals) < 2:
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
    
    # Add trend analysis
    trend = "increasing" if model.coef_[0] > 0 else "decreasing"
    trend_strength = "strong" if abs(model.coef_[0]) > 10 else "moderate"
    
    # Calculate confidence interval
    residuals = amounts - y_pred
    std_error = np.std(residuals)
    confidence_interval = 1.96 * std_error  # 95% confidence
    
    return {
        'prediction': prediction,
        'confidence': r2,
        'mae': mae,
        'trend': trend,
        'trend_strength': trend_strength,
        'confidence_interval': confidence_interval
    }

def export_to_csv():
    """Export expenses to CSV"""
    if st.session_state.expenses:
        df = pd.DataFrame(st.session_state.expenses)
        csv = df.to_csv(index=False)
        return csv
    return None

def main():
    st.markdown('<h1 class="main-header">💰 Budget & Expense Analysis</h1>', unsafe_allow_html=True)
    
    # Initialize session state
    initialize_session_state()
    
    # Sidebar for input
    with st.sidebar:
        # Income Section
        st.header("💷 Annual Income & Tax")
        annual_income_input = st.number_input(
            "Annual Gross Income (£)",
            min_value=0.0,
            step=1000.0,
            value=float(st.session_state.income * 12) if st.session_state.income > 0 else 0.0,
            help="Enter your annual gross salary before tax (e.g., £30,000)"
        )
        
        if st.button("💾 Update Annual Income"):
            st.session_state.income = annual_income_input / 12  # Store as monthly for consistency
            st.success("✅ Annual income updated!")
            st.rerun()
        
        # Show tax breakdown if income > 0
        if st.session_state.income > 0:
            # Calculate tax on annual basis, then show monthly
            tax_info = calculate_uk_tax(st.session_state.income * 12, 'annual')
            monthly_take_home = tax_info['take_home'] / 12
            monthly_tax = tax_info['income_tax'] / 12
            monthly_ni = tax_info['national_insurance'] / 12
            
            st.markdown("---")
            st.subheader("📊 Annual Tax Calculation")
            st.metric("Annual Gross Income", f"£{tax_info['gross_income']:,.0f}")
            st.metric("Annual Income Tax", f"£{tax_info['income_tax']:,.0f}")
            st.metric("Annual National Insurance", f"£{tax_info['national_insurance']:,.0f}")
            st.metric("Annual Take-Home", f"£{tax_info['take_home']:,.0f}")
            st.metric("Effective Tax Rate", f"{tax_info['effective_tax_rate']:.1f}%")
            
            # Monthly breakdown
            st.markdown("---")
            st.subheader("📅 Monthly Breakdown")
            st.metric("Monthly Take-Home", f"£{monthly_take_home:.2f}")
            st.metric("Monthly Tax", f"£{monthly_tax:.2f}")
            st.metric("Monthly NI", f"£{monthly_ni:.2f}")
            
            # Tax band information
            st.markdown("---")
            st.subheader("🎯 Tax Band Information")
            if tax_info['gross_income'] <= 12570:
                st.info("📊 **Personal Allowance** - No tax on income up to £12,570")
            elif tax_info['gross_income'] <= 50270:
                st.info("📊 **Basic Rate** - 20% tax on income between £12,571 - £50,270")
            elif tax_info['gross_income'] <= 125140:
                st.warning("📊 **Higher Rate** - 40% tax on income between £50,271 - £125,140")
            else:
                st.error("📊 **Additional Rate** - 45% tax on income above £125,140")
        
        st.divider()
        
        st.header("📝 Add New Expense")
        
        # Date input
        st.date_input(
            "Date",
            value=date.today(),
            key="new_date"
        )
        
        # Category input
        st.selectbox(
            "Category",
            options=st.session_state.categories,
            key="new_category"
        )
        
        # Amount input
        st.number_input(
            "Amount (£)",
            min_value=0.01,
            step=0.01,
            key="new_amount"
        )
        
        # Add expense button
        if st.button("➕ Add Expense"):
            add_expense()
        
        st.divider()
        
        # Category management
        st.header("🏷️ Manage Categories")
        new_category = st.text_input("Add new category")
        if st.button("Add Category") and new_category:
            if new_category not in st.session_state.categories:
                st.session_state.categories.append(new_category)
                st.success(f"✅ Added category: {new_category}")
                st.rerun()
        
        # Export functionality
        st.divider()
        st.header("📤 Export Data")
        csv_data = export_to_csv()
        if csv_data:
            st.download_button(
                label="📥 Download CSV",
                data=csv_data,
                file_name=f"expenses_{datetime.now().strftime('%Y%m%d')}.csv",
                mime="text/csv"
            )
    
    # Main content area
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.header("📊 Expense Overview")
        
        # Display expenses table
        if st.session_state.expenses:
            df_display = pd.DataFrame(st.session_state.expenses)
            # Convert Date to datetime first, then format it
            df_display['Date'] = pd.to_datetime(df_display['Date']).dt.strftime('%Y-%m-%d')
            
            # Add delete buttons
            for i, row in df_display.iterrows():
                col_a, col_b, col_c, col_d, col_e = st.columns([3, 2, 2, 1, 1])
                with col_a:
                    st.write(f"**{row['Date']}**")
                with col_b:
                    st.write(f"**{row['Category']}**")
                with col_c:
                    st.write(f"**£{row['Amount']:.2f}**")
                with col_d:
                    if st.button("🗑️", key=f"delete_{i}"):
                        delete_expense(i)
                        st.rerun()
                with col_e:
                    st.write("")
        else:
            st.info("📝 No expenses added yet. Use the sidebar to add your first expense!")
    
    with col2:
        st.header("📈 Quick Stats")
        
        # Analyze expenses
        analysis = analyze_expenses()
        
        if analysis:
            # Display key metrics
            st.metric("Total Spent", f"£{analysis['total_spent']:.2f}")
            st.metric("Monthly Average", f"£{analysis['avg_monthly']:.2f}")
            st.metric("Transactions", analysis['transaction_count'])
            
            # Biggest category
            if not analysis['category_totals'].empty:
                biggest_category = analysis['category_totals'].index[0]
                biggest_amount = analysis['category_totals'].iloc[0]
                st.metric("Biggest Category", f"{biggest_category}")
                st.metric("Category Amount", f"£{biggest_amount:.2f}")
        else:
            st.info("Add some expenses to see statistics!")
        
        # Financial Health Section
        if st.session_state.income > 0:
            st.markdown("---")
            st.header("💚 Financial Health")
            
            # Calculate financial health using monthly take-home pay
            if analysis:
                # Calculate monthly take-home from annual tax calculation
                tax_info = calculate_uk_tax(st.session_state.income * 12, 'annual')
                monthly_take_home = tax_info['take_home'] / 12
                
                financial_health = calculate_financial_health(
                    monthly_take_home,  # Use actual take-home pay, not gross
                    analysis['total_spent'],
                    analysis['category_totals']
                )
                
                if financial_health:
                    # Financial health score
                    if financial_health['health_color'] == 'success':
                        st.success(f"🏆 {financial_health['health_status']}")
                    elif financial_health['health_color'] == 'warning':
                        st.warning(f"⚠️ {financial_health['health_status']}")
                    else:
                        st.error(f"🚨 {financial_health['health_status']}")
                    
                    st.metric("Savings Rate", f"{financial_health['savings_rate']:.1f}%")
                    st.metric("Remaining Balance", f"£{financial_health['remaining_balance']:.2f}")
                    st.metric("Monthly Take-Home", f"£{monthly_take_home:.2f}")
                    
                    # Show top spending categories as % of take-home income
                    if financial_health['category_ratios']:
                        st.subheader("Top Categories (% of Take-Home)")
                        top_categories = sorted(financial_health['category_ratios'].items(), 
                                             key=lambda x: x[1], reverse=True)[:3]
                        for category, percentage in top_categories:
                            st.metric(category, f"{percentage:.1f}%")
    
    # Analysis and visualizations
    if st.session_state.expenses:
        analysis = analyze_expenses()
        
        # Create tabs for different views
        tab1, tab2, tab3, tab4, tab5 = st.tabs(["📊 Charts", "📈 Trends", "🔮 Predictions", "📋 Details", "💷 Income Analysis"])
        
        with tab1:
            st.header("Visualizations")
            
            col1, col2 = st.columns(2)
            
            with col1:
                # Pie chart
                pie_fig = create_pie_chart(analysis['category_totals'])
                st.plotly_chart(pie_fig, use_container_width=True)
            
            with col2:
                # Bar chart
                bar_fig = create_bar_chart(analysis['category_totals'])
                st.plotly_chart(bar_fig, use_container_width=True)
        
        with tab2:
            st.header("Monthly Trends")
            
            if len(analysis['monthly_totals']) > 1:
                line_fig = create_line_chart(analysis['monthly_totals'])
                st.plotly_chart(line_fig, use_container_width=True)
            else:
                st.info("Need at least 2 months of data to show trends!")
        
        with tab3:
            st.header("Spending Predictions")
            
            if len(analysis['monthly_totals']) >= 2:
                prediction = predict_next_month(analysis['monthly_totals'])
                
                if prediction:
                    col1, col2, col3, col4 = st.columns(4)
                    
                    with col1:
                        st.metric("Next Month", f"£{prediction['prediction']:.2f}")
                    
                    with col2:
                        st.metric("Confidence", f"{prediction['confidence']:.1%}")
                    
                    with col3:
                        st.metric("Trend", f"{prediction['trend_strength'].title()} {prediction['trend']}")
                    
                    with col4:
                        st.metric("Error Range", f"±£{prediction['mae']:.2f}")
                    
                    # Confidence interval
                    st.info(f"95% confidence interval: £{prediction['prediction'] - prediction['confidence_interval']:.2f} - £{prediction['prediction'] + prediction['confidence_interval']:.2f}")
                    
                    # Trend explanation
                    if prediction['trend'] == 'increasing':
                        st.warning("⚠️ Your spending appears to be trending upward. Consider reviewing your budget!")
                    else:
                        st.success("✅ Great! Your spending appears to be trending downward.")
            else:
                st.info("Need at least 2 months of data to make predictions!")
        
        with tab4:
            st.header("Detailed Analysis")
            
            col1, col2 = st.columns(2)
            
            with col1:
                st.subheader("Category Breakdown")
                category_df = pd.DataFrame({
                    'Category': analysis['category_totals'].index,
                    'Amount': analysis['category_totals'].values,
                    'Percentage': (analysis['category_totals'].values / analysis['total_spent'] * 100).round(1)
                })
                st.dataframe(category_df, use_container_width=True)
            
            with col2:
                st.subheader("Monthly Breakdown")
                monthly_df = pd.DataFrame({
                    'Month': [str(m) for m in analysis['monthly_totals'].index],
                    'Amount': analysis['monthly_totals'].values
                })
                st.dataframe(monthly_df, use_container_width=True)
        
        with tab5:
            st.header("💷 Income vs Expenses Analysis")
            
            if st.session_state.income > 0:
                # Get tax information (calculate on annual basis for accuracy)
                tax_info = calculate_uk_tax(st.session_state.income * 12, 'annual')
                monthly_take_home = tax_info['take_home'] / 12
                
                # Create income vs expenses comparison
                col1, col2 = st.columns(2)
                
                with col1:
                    st.subheader("💰 Income Breakdown")
                     
                    # Income pie chart (show monthly amounts)
                    income_data = {
                        'Take-Home Pay': monthly_take_home,
                        'Income Tax': tax_info['income_tax'] / 12,
                        'National Insurance': tax_info['national_insurance'] / 12
                    }
                     
                    fig_income = px.pie(
                        values=list(income_data.values()),
                        names=list(income_data.keys()),
                        title="Where Your Money Goes (Tax)",
                        color_discrete_sequence=['#28a745', '#dc3545', '#ffc107']
                    )
                    fig_income.update_traces(textposition='inside', textinfo='percent+label')
                    st.plotly_chart(fig_income, use_container_width=True)
                    
                    # Income metrics
                    st.metric("Annual Gross Income", f"£{tax_info['gross_income']:,.0f}")
                    st.metric("Annual Take-Home", f"£{tax_info['take_home']:,.0f}")
                    st.metric("Monthly Take-Home", f"£{monthly_take_home:.2f}")
                    st.metric("Effective Tax Rate", f"{tax_info['effective_tax_rate']:.1f}%")
                 
                with col2:
                    st.subheader("📊 Financial Health Overview")
                     
                    if analysis:
                        financial_health = calculate_financial_health(
                            monthly_take_home,  # Use monthly take-home pay
                            analysis['total_spent'],
                            analysis['category_totals']
                        )
                        
                        if financial_health:
                            # Financial health gauge
                            health_percentage = financial_health['health_score']
                             
                            # Create a simple gauge chart
                            fig_gauge = go.Figure(go.Indicator(
                                mode="gauge+number+delta",
                                value=health_percentage,
                                domain={'x': [0, 1], 'y': [0, 1]},
                                title={'text': "Financial Health Score"},
                                delta={'reference': 50},
                                gauge={
                                    'axis': {'range': [None, 100]},
                                    'bar': {'color': "darkblue"},
                                    'steps': [
                                        {'range': [0, 25], 'color': "lightgray"},
                                        {'range': [25, 50], 'color': "yellow"},
                                        {'range': [50, 75], 'color': "lightgreen"},
                                        {'range': [75, 100], 'color': "green"}
                                    ],
                                    'threshold': {
                                        'line': {'color': "red", 'width': 4},
                                        'thickness': 0.75,
                                        'value': 90
                                    }
                                }
                            ))
                            
                            fig_gauge.update_layout(height=300)
                            st.plotly_chart(fig_gauge, use_container_width=True)
                            
                            # Financial health metrics
                            st.metric("Health Status", financial_health['health_status'])
                            st.metric("Savings Rate", f"{financial_health['savings_rate']:.1f}%")
                            st.metric("Remaining Balance", f"£{financial_health['remaining_balance']:.2f}")
                            
                            # Savings potential
                            if analysis['monthly_totals'].shape[0] >= 2:
                                prediction = predict_next_month(analysis['monthly_totals'])
                                if prediction:
                                    savings_potential = monthly_take_home - prediction['prediction']
                                    st.metric("Next Month Savings Potential", f"£{savings_potential:.2f}")
                 
                # Income vs Expenses Bar Chart
                st.subheader("📈 Income vs Expenses Comparison")
                
                if analysis:
                    comparison_data = {
                        'Category': ['Take-Home Income', 'Expenses', 'Savings'],
                        'Amount': [
                            monthly_take_home,
                            analysis['total_spent'],
                            financial_health['remaining_balance'] if financial_health else 0
                        ]
                    }
                    
                    fig_comparison = px.bar(
                        x=comparison_data['Category'],
                        y=comparison_data['Amount'],
                        title="Monthly Income vs Expenses",
                        color=comparison_data['Category'],
                        color_discrete_map={
                            'Take-Home Income': '#28a745',
                            'Expenses': '#dc3545',
                            'Savings': '#17a2b8'
                        }
                    )
                    fig_comparison.update_layout(height=400)
                    st.plotly_chart(fig_comparison, use_container_width=True)
            else:
                st.info("💡 Set your monthly income in the sidebar to see income analysis!")
    
    # Footer
    st.divider()
    st.markdown("""
    <div style='text-align: center; color: #666;'>
        <p>Add your expenses in the sidebar to start analyzing your spending patterns!</p>
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()
