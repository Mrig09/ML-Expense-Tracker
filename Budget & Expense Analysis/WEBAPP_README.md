# 🌐 Budget & Expense Analysis Web App

A modern, interactive web application built with Streamlit that allows users to input expenses directly and see real-time visualizations, including pie charts, line charts, and spending predictions.

## 🚀 Features

### 📝 **Input & Management**
- **Add Expenses**: Input date, category, and amount directly in the web interface
- **Custom Categories**: Create your own expense categories
- **Delete Expenses**: Remove expenses with one click
- **Real-time Updates**: See changes immediately as you add/remove expenses

### 📊 **Visualizations**
- **Pie Chart**: Spending distribution by category with percentages
- **Bar Chart**: Category spending comparison
- **Line Chart**: Monthly spending trends over time
- **Interactive Charts**: Hover over charts for detailed information

### 🔮 **Analytics & Predictions**
- **Real-time Statistics**: Total spent, monthly average, transaction count
- **Category Breakdown**: Detailed analysis with percentages
- **Monthly Trends**: Track spending patterns month by month
- **ML Predictions**: Linear regression to forecast next month's spending
- **Trend Analysis**: Identify increasing/decreasing spending patterns

### 📤 **Data Management**
- **Export to CSV**: Download your expense data
- **Session Persistence**: Data stays while the app is running
- **Responsive Design**: Works on desktop and mobile devices

## 🛠️ Installation & Setup

### Prerequisites
- Python 3.7+
- pip package manager

### Quick Start

1. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

2. **Launch the Web App**:
   ```bash
   # Option 1: Use the launcher script
   python run_webapp.py
   
   # Option 2: Direct Streamlit command
   streamlit run web_app.py
   ```

3. **Open Your Browser**:
   - The app will automatically open at `http://localhost:8501`
   - If it doesn't open automatically, manually navigate to the URL

## 📱 How to Use

### 1. **Adding Expenses**
- Use the sidebar on the left
- Select a date (defaults to today)
- Choose a category from the dropdown
- Enter the amount
- Click "➕ Add Expense"

### 2. **Managing Categories**
- Add new categories in the sidebar
- Categories are automatically saved for the session
- Default categories: Food, Transport, Entertainment, Shopping, Bills, Other

### 3. **Viewing Analytics**
- **Charts Tab**: Interactive pie charts and bar charts
- **Trends Tab**: Monthly spending line charts
- **Predictions Tab**: ML-based spending forecasts
- **Details Tab**: Detailed breakdown tables

### 4. **Exporting Data**
- Click "📥 Download CSV" in the sidebar
- File will be named with current date: `expenses_YYYYMMDD.csv`

## 🎨 Interface Overview

```
┌─────────────────────────────────────────────────────────────┐
│                    💰 Budget & Expense Analysis             │
├─────────────────────────────────────────────────────────────┤
│ 📝 Add New Expense │ 📊 Expense Overview │ 📈 Quick Stats   │
│ Date: [____]       │ [Expense List]      │ Total: £XXX.XX   │
│ Category: [Food ▼] │                     │ Monthly: £XX.XX  │
│ Amount: [£__.__]   │                     │ Transactions: X  │
│ [➕ Add Expense]   │                     │ Biggest: Food    │
├─────────────────────────────────────────────────────────────┤
│ 🏷️ Manage Categories │ 📤 Export Data    │ [Charts] [Trends] │
│ [New Category]      │ [📥 Download CSV]  │ [Predictions]    │
│ [Add Category]      │                     │ [Details]        │
└─────────────────────────────────────────────────────────────┘
```

## 🔧 Technical Details

### **Built With**
- **Streamlit**: Web framework for data apps
- **Pandas**: Data manipulation and analysis
- **Plotly**: Interactive visualizations
- **Scikit-learn**: Machine learning for predictions
- **NumPy**: Numerical computations

### **Architecture**
- **Frontend**: Streamlit components with custom CSS
- **Backend**: Python with session state management
- **Data Processing**: Pandas for analysis and grouping
- **Visualizations**: Plotly for interactive charts
- **ML**: Linear regression for spending predictions

### **Data Flow**
1. User inputs expense → Session state
2. Data processed with Pandas → Analysis results
3. Results visualized with Plotly → Interactive charts
4. ML model trained on monthly data → Predictions

## 🚀 Running the App

### **Development Mode**
```bash
streamlit run web_app.py
```

### **Production Mode**
```bash
streamlit run web_app.py --server.port 8501 --server.address 0.0.0.0
```

### **Custom Port**
```bash
streamlit run web_app.py --server.port 8080
```

## 📊 Sample Data

To test the app with sample data, you can:

1. **Add Sample Expenses**:
   - Food: £25.50 (Today)
   - Transport: £12.80 (Yesterday)
   - Entertainment: £45.00 (2 days ago)

2. **View Results**:
   - Check the Charts tab for pie chart
   - See Trends tab for monthly patterns
   - Explore Predictions tab for ML forecasts

## 🎯 Key Benefits

### **User Experience**
- ✅ **No CSV Uploads**: Input expenses directly
- ✅ **Real-time Updates**: See changes immediately
- ✅ **Interactive Charts**: Hover and explore data
- ✅ **Mobile Friendly**: Responsive design
- ✅ **No Database Setup**: Session-based storage

### **Analytics**
- ✅ **Instant Insights**: Real-time calculations
- ✅ **Visual Learning**: Charts and graphs
- ✅ **Predictive Power**: ML-based forecasting
- ✅ **Trend Analysis**: Identify patterns
- ✅ **Category Management**: Flexible organization

## 🔮 Future Enhancements

- **Data Persistence**: Save data to database/files
- **User Accounts**: Multi-user support
- **Budget Tracking**: Set and monitor limits
- **Advanced ML**: More sophisticated prediction models
- **Mobile App**: Native mobile application
- **API Integration**: Connect with banking apps
- **Notifications**: Spending alerts and reminders

## 🐛 Troubleshooting

### **Common Issues**

1. **Port Already in Use**:
   ```bash
   streamlit run web_app.py --server.port 8502
   ```

2. **Dependencies Missing**:
   ```bash
   pip install -r requirements.txt
   ```

3. **App Not Loading**:
   - Check if Streamlit is installed: `pip show streamlit`
   - Verify Python version: `python --version`

4. **Charts Not Displaying**:
   - Ensure Plotly is installed: `pip show plotly`
   - Check browser console for JavaScript errors

### **Performance Tips**
- Close other browser tabs
- Use smaller datasets for testing
- Restart the app if it becomes slow

## 📞 Support

- **Documentation**: Check this README and the main project README
- **Issues**: Report bugs or feature requests
- **Contributions**: Pull requests welcome!

---

**🎉 Ready to start tracking your expenses? Launch the web app and begin your financial journey!**
