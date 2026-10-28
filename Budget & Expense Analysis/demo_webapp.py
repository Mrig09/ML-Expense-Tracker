#!/usr/bin/env python3
"""
Demo script for the Budget & Expense Analysis Web App
This script shows how to use the web application features
"""

import streamlit as st
import pandas as pd
from datetime import date, timedelta

def demo_webapp():
    """Demonstrate the web app features"""
    
    st.title("🎯 Budget & Expense Analysis - Demo Mode")
    st.markdown("---")
    
    st.header("📱 How to Use the Web App")
    
    # Demo instructions
    st.subheader("🚀 Getting Started")
    st.markdown("""
    1. **Launch the Web App**: Run `python run_webapp.py` or `streamlit run web_app.py`
    2. **Open Your Browser**: Navigate to `http://localhost:8501`
    3. **Start Adding Expenses**: Use the sidebar to input your expenses
    """)
    
    # Demo features
    st.subheader("✨ Key Features")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        **📝 Input & Management**
        - Add expenses with date, category, amount
        - Create custom categories
        - Delete expenses with one click
        - Real-time updates
        """)
        
        st.markdown("""
        **📊 Visualizations**
        - Interactive pie charts
        - Bar charts for comparison
        - Line charts for trends
        - Hover for details
        """)
    
    with col2:
        st.markdown("""
        **🔮 Analytics & ML**
        - Real-time statistics
        - Category breakdowns
        - Monthly trends
        - Spending predictions
        - Trend analysis
        """)
        
        st.markdown("""
        **📤 Data Management**
        - Export to CSV
        - Session persistence
        - Responsive design
        - Mobile friendly
        """)
    
    # Sample data demonstration
    st.subheader("📊 Sample Data Demo")
    
    # Create sample expenses
    sample_expenses = [
        {'Date': date.today(), 'Category': 'Food', 'Amount': 25.50},
        {'Date': date.today() - timedelta(days=1), 'Category': 'Transport', 'Amount': 12.80},
        {'Date': date.today() - timedelta(days=2), 'Category': 'Entertainment', 'Amount': 45.00},
        {'Date': date.today() - timedelta(days=3), 'Category': 'Food', 'Amount': 18.75},
        {'Date': date.today() - timedelta(days=4), 'Category': 'Shopping', 'Amount': 32.40},
        {'Date': date.today() - timedelta(days=5), 'Category': 'Transport', 'Amount': 8.50},
        {'Date': date.today() - timedelta(days=6), 'Category': 'Food', 'Amount': 22.30},
        {'Date': date.today() - timedelta(days=7), 'Category': 'Entertainment', 'Amount': 28.00},
    ]
    
    # Display sample data
    df = pd.DataFrame(sample_expenses)
    st.dataframe(df, use_container_width=True)
    
    # Show what the analysis would look like
    st.subheader("📈 What You'll See in the App")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("**Quick Stats**")
        total = df['Amount'].sum()
        avg_daily = df['Amount'].mean()
        categories = df['Category'].nunique()
        
        st.metric("Total Spent", f"£{total:.2f}")
        st.metric("Daily Average", f"£{avg_daily:.2f}")
        st.metric("Categories", categories)
    
    with col2:
        st.markdown("**Category Breakdown**")
        category_totals = df.groupby('Category')['Amount'].sum().sort_values(ascending=False)
        for category, amount in category_totals.items():
            percentage = (amount / total) * 100
            st.write(f"**{category}**: £{amount:.2f} ({percentage:.1f}%)")
    
    # Demo workflow
    st.subheader("🔄 Demo Workflow")
    
    st.markdown("""
    1. **Add Sample Expenses**:
       - Food: £25.50 (Today)
       - Transport: £12.80 (Yesterday)
       - Entertainment: £45.00 (2 days ago)
    
    2. **View Results**:
       - Check Charts tab for pie chart
       - See Trends tab for patterns
       - Explore Predictions tab for ML forecasts
    
    3. **Try Features**:
       - Add new categories
       - Delete expenses
       - Export data to CSV
    """)
    
    # Launch instructions
    st.subheader("🚀 Ready to Launch?")
    
    st.code("""
# Option 1: Use the launcher script
python run_webapp.py

# Option 2: Direct Streamlit command
streamlit run web_app.py

# Option 3: Custom port
streamlit run web_app.py --server.port 8080
    """, language="bash")
    
    st.success("🎉 The web app will open automatically in your browser!")
    
    # Tips and tricks
    st.subheader("💡 Tips & Tricks")
    
    st.markdown("""
    - **Real-time Updates**: Changes appear immediately
    - **Mobile Friendly**: Works great on phones and tablets
    - **Keyboard Shortcuts**: Use Tab to navigate between fields
    - **Data Persistence**: Data stays while the app is running
    - **Export Anytime**: Download your data as CSV
    """)
    
    # Footer
    st.markdown("---")
    st.markdown("""
    <div style='text-align: center; color: #666;'>
        <p>💰 <strong>Budget & Expense Analysis Web App</strong></p>
        <p>Built with Streamlit, Pandas, and Plotly</p>
        <p>Start tracking your expenses today!</p>
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    demo_webapp()
