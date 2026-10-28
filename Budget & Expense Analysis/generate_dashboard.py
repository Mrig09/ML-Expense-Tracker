#!/usr/bin/env python3
"""
Generate HTML dashboard dynamically from analysis results
"""

import pandas as pd
from datetime import datetime
import os

def load_analysis_data():
    """Load the analysis data from CSV"""
    try:
        df = pd.read_csv("sample_expenses.csv")
        df['Date'] = pd.to_datetime(df['Date'])
        df['Month'] = df['Date'].dt.to_period('M')
        
        # Calculate statistics
        total_spent = df['Amount'].sum()
        avg_monthly = df.groupby('Month')['Amount'].sum().mean()
        transaction_count = len(df)
        
        # Category analysis
        category_totals = df.groupby('Category')['Amount'].sum().sort_values(ascending=False)
        biggest_category = category_totals.index[0]
        biggest_amount = category_totals.iloc[0]
        
        # Monthly analysis
        monthly_totals = df.groupby('Month')['Amount'].sum()
        
        return {
            'total_spent': total_spent,
            'avg_monthly': avg_monthly,
            'transaction_count': transaction_count,
            'biggest_category': biggest_category,
            'biggest_amount': biggest_amount,
            'category_totals': category_totals,
            'monthly_totals': monthly_totals
        }
    except Exception as e:
        print(f"Error loading data: {e}")
        return None

def generate_html_dashboard(data):
    """Generate HTML dashboard with real data"""   
    
    # Calculate percentages for categories
    category_percentages = {}
    for category, amount in data['category_totals'].items():
        percentage = (amount / data['total_spent']) * 100
        category_percentages[category] = percentage
    
    html_template = f"""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>💰 Budget & Expense Analysis Dashboard</title>
    <style>
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}

        body {{
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            color: #333;
        }}

        .container {{
            max-width: 1200px;
            margin: 0 auto;
            padding: 20px;
        }}

        .header {{
            text-align: center;
            margin-bottom: 40px;
            color: white;
        }}

        .header h1 {{
            font-size: 3rem;
            margin-bottom: 10px;
            text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
        }}

        .header p {{
            font-size: 1.2rem;
            opacity: 0.9;
        }}

        .stats-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
            gap: 20px;
            margin-bottom: 40px;
        }}

        .stat-card {{
            background: white;
            padding: 25px;
            border-radius: 15px;
            box-shadow: 0 10px 30px rgba(0,0,0,0.1);
            text-align: center;
            transition: transform 0.3s ease, box-shadow 0.3s ease;
        }}

        .stat-card:hover {{
            transform: translateY(-5px);
            box-shadow: 0 15px 40px rgba(0,0,0,0.15);
        }}

        .stat-card h3 {{
            color: #667eea;
            margin-bottom: 10px;
            font-size: 1.1rem;
        }}

        .stat-card .value {{
            font-size: 2.5rem;
            font-weight: bold;
            color: #333;
            margin-bottom: 5px;
        }}

        .stat-card .label {{
            color: #666;
            font-size: 0.9rem;
        }}

        .charts-section {{
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 30px;
            margin-bottom: 40px;
        }}

        .chart-container {{
            background: white;
            padding: 25px;
            border-radius: 15px;
            box-shadow: 0 10px 30px rgba(0,0,0,0.1);
        }}

        .chart-container h3 {{
            color: #667eea;
            margin-bottom: 20px;
            text-align: center;
            font-size: 1.3rem;
        }}

        .chart-info {{
            background: #f8f9fa;
            border-radius: 10px;
            padding: 30px 20px;
            text-align: center;
            color: #6c757d;
        }}

        .chart-info .amount {{
            font-size: 2.5rem;
            font-weight: bold;
            color: #667eea;
            margin-bottom: 10px;
        }}

        .chart-info .description {{
            font-size: 1.1rem;
            margin-bottom: 15px;
        }}

        .chart-info .note {{
            font-size: 0.9rem;
            opacity: 0.7;
        }}

        .prediction-section {{
            background: white;
            padding: 30px;
            border-radius: 15px;
            box-shadow: 0 10px 30px rgba(0,0,0,0.1);
            margin-bottom: 40px;
        }}

        .prediction-section h3 {{
            color: #667eea;
            margin-bottom: 20px;
            text-align: center;
            font-size: 1.5rem;
        }}

        .prediction-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 20px;
        }}

        .prediction-item {{
            text-align: center;
            padding: 20px;
            background: #f8f9fa;
            border-radius: 10px;
            border-left: 4px solid #667eea;
        }}

        .prediction-item .label {{
            font-size: 0.9rem;
            color: #666;
            margin-bottom: 5px;
        }}

        .prediction-item .value {{
            font-size: 1.5rem;
            font-weight: bold;
            color: #333;
        }}

        .category-breakdown {{
            background: white;
            padding: 30px;
            border-radius: 15px;
            box-shadow: 0 10px 30px rgba(0,0,0,0.1);
            margin-bottom: 40px;
        }}

        .category-breakdown h3 {{
            color: #667eea;
            margin-bottom: 20px;
            text-align: center;
            font-size: 1.5rem;
        }}

        .category-item {{
            display: flex;
            justify-content: space-between;
            align-items: center;
            padding: 15px 0;
            border-bottom: 1px solid #eee;
        }}

        .category-item:last-child {{
            border-bottom: none;
        }}

        .category-name {{
            font-weight: 500;
            color: #333;
        }}

        .category-amount {{
            font-weight: bold;
            color: #667eea;
        }}

        .category-percentage {{
            color: #666;
            font-size: 0.9rem;
        }}

        .footer {{
            text-align: center;
            color: white;
            opacity: 0.8;
            margin-top: 40px;
        }}

        .monthly-trend {{
            background: white;
            padding: 30px;
            border-radius: 15px;
            box-shadow: 0 10px 30px rgba(0,0,0,0.1);
            margin-bottom: 40px;
        }}

        .monthly-trend h3 {{
            color: #667eea;
            margin-bottom: 20px;
            text-align: center;
            font-size: 1.5rem;
        }}

        .monthly-item {{
            display: flex;
            justify-content: space-between;
            align-items: center;
            padding: 12px 0;
            border-bottom: 1px solid #eee;
        }}

        .monthly-item:last-child {{
            border-bottom: none;
        }}

        .month-name {{
            font-weight: 500;
            color: #333;
        }}

        .month-amount {{
            font-weight: bold;
            color: #667eea;
        }}

        @media (max-width: 768px) {{
            .charts-section {{
                grid-template-columns: 1fr;
            }}
            
            .header h1 {{
                font-size: 2rem;
            }}
            
            .stat-card .value {{
                font-size: 2rem;
            }}
        }}

        .loading {{
            text-align: center;
            padding: 40px;
            color: #666;
        }}

        .loading .spinner {{
            border: 4px solid #f3f3f3;
            border-top: 4px solid #667eea;
            border-radius: 50%;
            width: 40px;
            height: 40px;
            animation: spin 1s linear infinite;
            margin: 0 auto 20px;
        }}

        @keyframes spin {{
            0% {{ transform: rotate(0deg); }}
            100% {{ transform: rotate(360deg); }}
        }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>💰 Budget & Expense Analysis</h1>
            <p>Your Personal Financial Dashboard</p>
            <small>Generated on {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</small>
        </div>

        <div class="stats-grid">
            <div class="stat-card">
                <h3>Total Spent</h3>
                <div class="value">£{data['total_spent']:.2f}</div>
                <div class="label">Overall spending</div>
            </div>
            <div class="stat-card">
                <h3>Monthly Average</h3>
                <div class="value">£{data['avg_monthly']:.2f}</div>
                <div class="label">Per month</div>
            </div>
            <div class="stat-card">
                <h3>Transactions</h3>
                <div class="value">{data['transaction_count']}</div>
                <div class="label">Total count</div>
            </div>
            <div class="stat-card">
                <h3>Biggest Category</h3>
                <div class="value">{data['biggest_category']}</div>
                <div class="label">£{data['biggest_amount']:.2f} ({category_percentages[data['biggest_category']]:.1f}%)</div>
            </div>
        </div>

        <div class="charts-section">
            <div class="chart-container">
                <h3>📊 Spending by Category</h3>
                <div class="chart-info">
                    <div class="amount">£{data['category_totals'].iloc[0]:.2f}</div>
                    <div class="description">Highest spending category</div>
                    <div class="note">Check 'charts' directory for actual pie chart</div>
                </div>
            </div>
            <div class="chart-container">
                <h3>📈 Monthly Spending Trend</h3>
                <div class="chart-info">
                    <div class="amount">£{data['monthly_totals'].max():.2f}</div>
                    <div class="description">Highest monthly spend</div>
                    <div class="note">Check 'charts' directory for actual line chart</div>
                </div>
            </div>
        </div>

        <div class="monthly-trend">
            <h3>📅 Monthly Spending Breakdown</h3>
            {''.join([f'''
            <div class="monthly-item">
                <div class="month-name">{month}</div>
                <div class="month-amount">£{amount:.2f}</div>
            </div>''' for month, amount in data['monthly_totals'].items()])}
        </div>

        <div class="category-breakdown">
            <h3>🏷️ Spending by Category</h3>
            {''.join([f'''
            <div class="category-item">
                <div class="category-name">{category}</div>
                <div class="category-amount">£{amount:.2f}</div>
                <div class="category-percentage">{category_percentages[category]:.1f}%</div>
            </div>''' for category, amount in data['category_totals'].items()])}
        </div>

        <div class="footer">
            <p>Built with ❤️ using Python, Pandas, and Machine Learning</p>
            <p>Check the 'charts' directory for generated visualizations</p>
            <p><a href="charts/plotly_dashboard.html" style="color: white;">📊 View Interactive Dashboard</a></p>
        </div>
    </div>

    <script>
        // Add some interactivity
        document.addEventListener('DOMContentLoaded', function() {{
            // Animate stat cards on scroll
            const observerOptions = {{
                threshold: 0.1,
                rootMargin: '0px 0px -50px 0px'
            }};

            const observer = new IntersectionObserver((entries) => {{
                entries.forEach(entry => {{
                    if (entry.isIntersecting) {{
                        entry.target.style.opacity = '1';
                        entry.target.style.transform = 'translateY(0)';
                    }}
                }});
            }}, observerOptions);

            // Observe all stat cards
            document.querySelectorAll('.stat-card').forEach(card => {{
                card.style.opacity = '0';
                card.style.transform = 'translateY(20px)';
                card.style.transition = 'opacity 0.6s ease, transform 0.6s ease';
                observer.observe(card);
            }});
        }});
    </script>
</body>
</html>
"""
    
    return html_template

def main():
    """Main function to generate the dashboard"""
    print("🚀 Generating HTML Dashboard...")
    
    # Load analysis data
    data = load_analysis_data()
    if data is None:
        print("❌ Failed to load data")
        return
    
    # Generate HTML
    html_content = generate_html_dashboard(data)
    
    # Save to file
    output_file = "dynamic_dashboard.html"
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(html_content)
    
    print(f"✅ Dashboard generated successfully: {output_file}")
    print(f"📊 Open {output_file} in your web browser to view the dashboard")
    print(f"🔗 You can also view the interactive Plotly dashboard: charts/plotly_dashboard.html")

if __name__ == "__main__":
    main()
