import matplotlib.pyplot as plt
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
import os

def create_charts(category_totals, monthly_totals):
    """Create both matplotlib and plotly charts"""
    
    # Create charts directory if it doesn't exist
    if not os.path.exists('charts'):
        os.makedirs('charts')
    
    # Create matplotlib charts
    create_matplotlib_charts(category_totals, monthly_totals)
    
    # Create plotly charts
    create_plotly_charts(category_totals, monthly_totals)
    
    print("✅ Charts created and saved in 'charts' directory")

def create_matplotlib_charts(category_totals, monthly_totals):
    """Create matplotlib charts"""
    
    # Set style
    plt.style.use('default')
    
    # Create figure with subplots
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 6))
    
    # Pie chart for categories
    colors = ['#FF6B6B', '#4ECDC4', '#45B7D1', '#96CEB4', '#FFEAA7']
    wedges, texts, autotexts = ax1.pie(
        category_totals.values, 
        labels=category_totals.index, 
        autopct='%1.1f%%',
        colors=colors[:len(category_totals)],
        startangle=90
    )
    ax1.set_title('Spending by Category', fontsize=14, fontweight='bold', pad=20)
    
    # Line chart for monthly spending
    months = [str(m) for m in monthly_totals.index]
    amounts = monthly_totals.values
    
    ax2.plot(months, amounts, marker='o', linewidth=2, markersize=8, color='#4ECDC4')
    ax2.fill_between(months, amounts, alpha=0.3, color='#4ECDC4')
    ax2.set_title('Monthly Spending Trend', fontsize=14, fontweight='bold', pad=20)
    ax2.set_xlabel('Month')
    ax2.set_ylabel('Amount (£)')
    ax2.grid(True, alpha=0.3)
    
    # Rotate x-axis labels for better readability
    ax2.tick_params(axis='x', rotation=45)
    
    # Add value labels on the line chart
    for i, (month, amount) in enumerate(zip(months, amounts)):
        ax2.annotate(f'£{amount:.0f}', (i, amount), textcoords="offset points", 
                     xytext=(0,10), ha='center', fontsize=10)
    
    plt.tight_layout()
    plt.savefig('charts/matplotlib_charts.png', dpi=300, bbox_inches='tight')
    plt.close()

def create_plotly_charts(category_totals, monthly_totals):
    """Create interactive plotly charts"""
    
    # Create subplot figure
    fig = make_subplots(
        rows=1, cols=2,
        subplot_titles=('Spending by Category', 'Monthly Spending Trend'),
        specs=[[{"type": "pie"}, {"type": "scatter"}]]
    )
    
    # Pie chart
    fig.add_trace(
        go.Pie(
            labels=category_totals.index,
            values=category_totals.values,
            hole=0.3,
            marker_colors=['#FF6B6B', '#4ECDC4', '#45B7D1', '#96CEB4', '#FFEAA7'],
            textinfo='label+percent',
            textposition='outside'
        ),
        row=1, col=1
    )
    
    # Line chart
    months = [str(m) for m in monthly_totals.index]
    amounts = monthly_totals.values
    
    fig.add_trace(
        go.Scatter(
            x=months,
            y=amounts,
            mode='lines+markers',
            line=dict(color='#4ECDC4', width=3),
            marker=dict(size=8, color='#4ECDC4'),
            fill='tonexty',
            fillcolor='rgba(78, 205, 196, 0.3)',
            name='Monthly Spending'
        ),
        row=1, col=2
    )
    
    # Update layout
    fig.update_layout(
        title_text="Budget & Expense Analysis Dashboard",
        title_x=0.5,
        title_font_size=20,
        showlegend=False,
        height=500
    )
    
    # Update axes
    fig.update_xaxes(title_text="Month", row=1, col=2)
    fig.update_yaxes(title_text="Amount (£)", row=1, col=2)
    
    # Save as HTML for interactive viewing
    fig.write_html('charts/plotly_dashboard.html')
    
    # Save as PNG for static viewing
    fig.write_image('charts/plotly_charts.png', width=1200, height=500)
