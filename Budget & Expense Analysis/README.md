# 💸 Budget & Expense Analysis - MVP

A Python-based budget and expense analysis tool that provides insights into spending patterns, generates visualizations, and predicts future expenses using machine learning.

## 🚀 Features

- **CSV Data Processing**: Load and analyze expense data from CSV files
- **Category Analysis**: Group expenses by category with totals and percentages
- **Monthly Trends**: Track spending patterns over time
- **Data Visualization**: Generate pie charts and line charts using matplotlib and plotly
- **Predictive Analytics**: Use linear regression to forecast next month's spending
- **Interactive Dashboard**: View charts in an interactive HTML format

## 📁 Project Structure

```
Budget & Expense Analysis/
├── analysis.py              # Main analysis script
├── visualize.py             # Chart generation module
├── predict.py               # ML prediction module
├── test_analysis.py         # Testing script
├── sample_expenses.csv      # Sample data file
├── requirements.txt         # Python dependencies
├── README.md               # This file
└── charts/                 # Generated charts (created automatically)
```

## 🛠️ Installation

1. **Clone or download** this project to your local machine

2. **Install Python dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Verify installation**:
   ```bash
   python test_analysis.py
   ```

## 📊 Usage

### Quick Start

1. **Run the analysis**:
   ```bash
   python analysis.py
   ```

2. **View results**:
   - Check the terminal for text summaries
   - View generated charts in the `charts/` directory
   - Open `charts/plotly_dashboard.html` for interactive charts

### Using Your Own Data

1. **Prepare your CSV file** with these columns:
   ```csv
   Date,Category,Amount
   2025-01-01,Food,12.50
   2025-01-02,Transport,4.20
   ```

2. **Update the file path** in `analysis.py`:
   ```python
   csv_file = "your_expenses.csv"  # Change this line
   ```

3. **Run the analysis** as above

## 📈 Sample Output

The tool generates comprehensive summaries including:

- **Overall Statistics**: Total spent, average monthly spend, transaction count
- **Current Month**: Spending for the current month
- **Category Breakdown**: Spending by category with percentages
- **Monthly Trends**: Month-over-month spending patterns
- **Predictions**: Forecast for next month's spending with confidence intervals

## 🎨 Generated Charts

- **Pie Chart**: Spending distribution by category
- **Line Chart**: Monthly spending trends over time
- **Interactive Dashboard**: Plotly-based interactive visualizations

## 🔮 Prediction Features

- **Linear Regression**: Predicts next month's spending based on historical data
- **Confidence Intervals**: Provides 95% confidence ranges for predictions
- **Trend Analysis**: Identifies increasing/decreasing spending patterns
- **Model Performance**: R² score and mean absolute error metrics

## 🧪 Testing

Run the test suite to verify everything works:

```bash
python test_analysis.py
```

This will check:
- ✅ Module imports
- ✅ CSV file loading
- ✅ Custom module functionality

## 📋 Requirements

- Python 3.7+
- pandas >= 1.5.0
- matplotlib >= 3.6.0
- scikit-learn >= 1.1.0
- plotly >= 5.10.0

## 🚧 Future Enhancements

- **Interactive Dashboard**: Streamlit-based web interface
- **Auto-categorization**: Smart expense categorization
- **Advanced ML**: ARIMA, Prophet, or other time series models
- **User Input Forms**: Web-based data entry instead of CSV
- **Budget Tracking**: Set and monitor budget limits
- **Export Features**: Generate reports in various formats

## 🤝 Contributing

Feel free to:
- Report bugs
- Suggest new features
- Submit pull requests
- Improve documentation

## 📄 License

This project is open source and available under the MIT License.

---

**Happy Budgeting! 💰📊**
