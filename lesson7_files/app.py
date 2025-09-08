"""
E-commerce Business Intelligence Streamlit Dashboard

A professional dashboard for analyzing e-commerce business metrics with configurable 
time periods, trend indicators, and interactive visualizations.
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import warnings

# Import custom modules
from data_loader import EcommerceDataLoader, categorize_delivery_speed
from business_metrics import BusinessMetricsCalculator

warnings.filterwarnings('ignore')

# Page configuration
st.set_page_config(
    page_title="E-commerce Business Intelligence",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Custom CSS for professional styling
st.markdown("""
<style>
    .main > div {
        padding-top: 2rem;
    }
    
    .metric-card {
        background-color: white;
        padding: 1rem;
        border-radius: 0.5rem;
        border: 1px solid #e0e0e0;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        height: 120px;
        display: flex;
        flex-direction: column;
        justify-content: center;
    }
    
    .metric-title {
        font-size: 0.9rem;
        color: #666;
        margin-bottom: 0.5rem;
        font-weight: 500;
    }
    
    .metric-value {
        font-size: 1.8rem;
        font-weight: bold;
        color: #333;
        margin-bottom: 0.3rem;
    }
    
    .metric-trend {
        font-size: 0.8rem;
        font-weight: 500;
    }
    
    .trend-positive {
        color: #28a745;
    }
    
    .trend-negative {
        color: #dc3545;
    }
    
    .chart-container {
        background-color: white;
        border-radius: 0.5rem;
        padding: 1rem;
        border: 1px solid #e0e0e0;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        height: 400px;
    }
    
    .bottom-card {
        background-color: white;
        padding: 1.5rem;
        border-radius: 0.5rem;
        border: 1px solid #e0e0e0;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        height: 150px;
        display: flex;
        flex-direction: column;
        justify-content: center;
        text-align: center;
    }
    
    .stars {
        color: #ffc107;
        font-size: 1.2rem;
        margin: 0.5rem 0;
    }
</style>
""", unsafe_allow_html=True)

@st.cache_data
def load_data():
    """Load and cache the e-commerce data."""
    try:
        loader = EcommerceDataLoader('ecommerce_data')
        datasets = loader.load_all_datasets()
        return loader, datasets
    except Exception as e:
        st.error(f"Error loading data: {str(e)}")
        return None, None

@st.cache_data
def get_business_metrics(_loader, year, comparison_year=None):
    """Get business metrics for the specified year."""
    try:
        # Create comprehensive dataset for all years needed
        if comparison_year:
            all_years_data = _loader.create_sales_dataset(target_year=None, include_canceled=False)
            all_years_with_customers = _loader.create_customer_sales_dataset(all_years_data)
            all_years_with_products = _loader.create_product_sales_dataset(all_years_with_customers)
            full_dataset = _loader.create_review_dataset(all_years_with_products)
        else:
            year_data = _loader.create_sales_dataset(target_year=year, include_canceled=False)
            year_with_customers = _loader.create_customer_sales_dataset(year_data)
            year_with_products = _loader.create_product_sales_dataset(year_with_customers)
            full_dataset = _loader.create_review_dataset(year_with_products)
        
        # Calculate metrics
        metrics_calc = BusinessMetricsCalculator(full_dataset)
        report = metrics_calc.generate_comprehensive_report(year, comparison_year)
        
        return report, full_dataset
    except Exception as e:
        st.error(f"Error calculating metrics: {str(e)}")
        return None, None

def format_currency(value):
    """Format currency values for display."""
    if value >= 1_000_000:
        return f"${value/1_000_000:.1f}M"
    elif value >= 1_000:
        return f"${value/1_000:.0f}K"
    else:
        return f"${value:,.0f}"

def create_trend_indicator(current_value, previous_value, is_percentage=True):
    """Create trend indicator with color and arrow."""
    if previous_value is None or previous_value == 0:
        return "N/A", "color: #666;"
    
    change = ((current_value - previous_value) / previous_value) * 100
    
    if change > 0:
        arrow = "↗"
        color_class = "trend-positive"
        sign = "+"
    elif change < 0:
        arrow = "↘"
        color_class = "trend-negative" 
        sign = ""
    else:
        arrow = "→"
        color_class = "color: #666;"
        sign = ""
    
    if is_percentage:
        return f"{arrow} {sign}{change:.2f}%", color_class
    else:
        return f"{arrow} {sign}{change:.2f}", color_class

def main():
    # Header with title and filter
    col1, col2 = st.columns([3, 1])
    
    with col1:
        st.title("E-commerce Business Intelligence Dashboard")
    
    with col2:
        # Load data to get available years
        loader, datasets = load_data()
        if loader is None:
            st.error("Failed to load data. Please check your data files.")
            return
        
        # Get available years from the data
        orders = datasets.get('orders')
        if orders is not None:
            orders['order_purchase_timestamp'] = pd.to_datetime(orders['order_purchase_timestamp'])
            available_years = sorted(orders['order_purchase_timestamp'].dt.year.unique(), reverse=True)
        else:
            available_years = [2023, 2022, 2021]
        
        # Set 2023 as default if available
        default_index = 0
        if 2023 in available_years:
            default_index = available_years.index(2023)
        
        selected_year = st.selectbox(
            "Analysis Year",
            options=available_years,
            index=default_index,
            key="year_filter"
        )
    
    # Determine comparison year
    comparison_year = selected_year - 1 if selected_year - 1 in available_years else None
    
    # Get business metrics
    report, full_dataset = get_business_metrics(loader, selected_year, comparison_year)
    if report is None:
        st.error("Failed to calculate business metrics.")
        return
    
    revenue_metrics = report['revenue_metrics']
    
    # KPI Row - 4 cards
    st.markdown("### Key Performance Indicators")
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        total_revenue = revenue_metrics['total_revenue']
        prev_revenue = revenue_metrics.get('previous_year_revenue')
        trend_text, trend_class = create_trend_indicator(total_revenue, prev_revenue)
        
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-title">Total Revenue</div>
            <div class="metric-value">{format_currency(total_revenue)}</div>
            <div class="metric-trend {trend_class}">{trend_text}</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        monthly_growth = report['monthly_trends']['revenue_growth'].mean()
        
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-title">Monthly Growth</div>
            <div class="metric-value">{monthly_growth:.2f}%</div>
            <div class="metric-trend" style="color: #666;">Average</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        aov = revenue_metrics['average_order_value']
        prev_aov = revenue_metrics.get('previous_year_aov')
        aov_trend_text, aov_trend_class = create_trend_indicator(aov, prev_aov)
        
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-title">Average Order Value</div>
            <div class="metric-value">{format_currency(aov)}</div>
            <div class="metric-trend {aov_trend_class}">{aov_trend_text}</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col4:
        total_orders = revenue_metrics['total_orders']
        prev_orders = revenue_metrics.get('previous_year_orders')
        orders_trend_text, orders_trend_class = create_trend_indicator(total_orders, prev_orders, is_percentage=True)
        
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-title">Total Orders</div>
            <div class="metric-value">{total_orders:,}</div>
            <div class="metric-trend {orders_trend_class}">{orders_trend_text}</div>
        </div>
        """, unsafe_allow_html=True)
    
    # Charts Grid - 2x2 layout
    st.markdown("### Performance Analytics")
    
    # First row of charts
    col1, col2 = st.columns(2)
    
    with col1:
        # Revenue trend line chart
        monthly_trends = report['monthly_trends']
        
        fig = go.Figure()
        
        # Current year line (solid)
        fig.add_trace(go.Scatter(
            x=monthly_trends['month'],
            y=monthly_trends['revenue'],
            mode='lines+markers',
            name=f'{selected_year}',
            line=dict(color='#1f77b4', width=3),
            marker=dict(size=8)
        ))
        
        # Previous year line (dashed) if available
        if comparison_year and full_dataset is not None:
            try:
                prev_year_data = full_dataset[full_dataset['purchase_year'] == comparison_year]
                prev_monthly = prev_year_data.groupby('purchase_month')['price'].sum().reset_index()
                prev_monthly.columns = ['month', 'revenue']
                
                fig.add_trace(go.Scatter(
                    x=prev_monthly['month'],
                    y=prev_monthly['revenue'],
                    mode='lines+markers',
                    name=f'{comparison_year}',
                    line=dict(color='#ff7f0e', width=2, dash='dash'),
                    marker=dict(size=6)
                ))
            except:
                pass
        
        fig.update_layout(
            title=f"Monthly Revenue Trend",
            xaxis_title="Month",
            yaxis_title="Revenue",
            showlegend=True,
            height=350,
            xaxis=dict(showgrid=True, gridcolor='#f0f0f0'),
            yaxis=dict(showgrid=True, gridcolor='#f0f0f0', tickformat='$,.0s'),
            plot_bgcolor='white',
            font=dict(size=12)
        )
        
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        # Top 10 categories bar chart
        if 'error' not in report['product_performance']:
            top_categories = report['product_performance']['top_categories'].head(10)
            
            # Create blue gradient colors
            max_revenue = top_categories['total_revenue'].max()
            colors = []
            for revenue in top_categories['total_revenue']:
                intensity = revenue / max_revenue
                # Create blue gradient from light to dark
                blue_intensity = 0.3 + (intensity * 0.7)
                colors.append(f'rgba(31, 119, 180, {blue_intensity})')
            
            fig = px.bar(
                top_categories,
                y='product_category_name',
                x='total_revenue',
                orientation='h',
                title="Top 10 Product Categories"
            )
            
            fig.update_traces(marker_color=colors)
            fig.update_layout(
                height=350,
                yaxis={'categoryorder': 'total ascending'},
                xaxis_title="Revenue",
                yaxis_title="Product Category",
                xaxis=dict(tickformat='$,.0s'),
                plot_bgcolor='white',
                font=dict(size=12)
            )
            
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("Product category data not available")
    
    # Second row of charts
    col1, col2 = st.columns(2)
    
    with col1:
        # Revenue by state choropleth map
        geo_data = report['geographic_performance']
        if 'error' not in geo_data.columns:
            fig = px.choropleth(
                geo_data,
                locations='state',
                color='revenue',
                locationmode='USA-states',
                scope='usa',
                title='Revenue by State',
                color_continuous_scale='Blues'
            )
            
            fig.update_layout(
                height=350,
                geo=dict(showframe=False, showcoastlines=True),
                font=dict(size=12)
            )
            
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("Geographic data not available")
    
    with col2:
        # Satisfaction vs delivery time bar chart
        if full_dataset is not None and 'delivery_days' in full_dataset.columns and 'review_score' in full_dataset.columns:
            delivery_satisfaction = full_dataset.drop_duplicates('order_id')
            delivery_satisfaction = delivery_satisfaction.dropna(subset=['delivery_days', 'review_score'])
            delivery_satisfaction['delivery_category'] = delivery_satisfaction['delivery_days'].apply(categorize_delivery_speed)
            
            satisfaction_by_delivery = delivery_satisfaction.groupby('delivery_category')['review_score'].mean().reset_index()
            satisfaction_by_delivery.columns = ['delivery_category', 'avg_review_score']
            
            # Order categories properly
            category_order = ['1-3 days', '4-7 days', '8+ days']
            satisfaction_by_delivery['delivery_category'] = pd.Categorical(
                satisfaction_by_delivery['delivery_category'], 
                categories=category_order, 
                ordered=True
            )
            satisfaction_by_delivery = satisfaction_by_delivery.sort_values('delivery_category')
            
            fig = px.bar(
                satisfaction_by_delivery,
                x='delivery_category',
                y='avg_review_score',
                title="Customer Satisfaction by Delivery Speed",
                color='avg_review_score',
                color_continuous_scale='Blues'
            )
            
            fig.update_layout(
                height=350,
                xaxis_title="Delivery Time",
                yaxis_title="Average Review Score",
                yaxis=dict(range=[0, 5]),
                plot_bgcolor='white',
                font=dict(size=12),
                showlegend=False
            )
            
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("Delivery and satisfaction data not available")
    
    # Bottom Row - 2 cards
    st.markdown("### Customer Experience Metrics")
    col1, col2 = st.columns(2)
    
    with col1:
        # Average delivery time with trend
        if 'error' not in report['delivery_performance']:
            delivery_metrics = report['delivery_performance']
            avg_delivery = delivery_metrics['avg_delivery_days']
            
            st.markdown(f"""
            <div class="bottom-card">
                <div class="metric-title">Average Delivery Time</div>
                <div class="metric-value">{avg_delivery:.1f} days</div>
                <div class="metric-trend" style="color: #666;">Operational Metric</div>
            </div>
            """, unsafe_allow_html=True)
        else:
            st.info("Delivery performance data not available")
    
    with col2:
        # Review Score with stars
        if 'error' not in report['customer_satisfaction']:
            satisfaction_metrics = report['customer_satisfaction']
            avg_score = satisfaction_metrics['avg_review_score']
            
            # Create star display
            full_stars = int(avg_score)
            has_half_star = (avg_score - full_stars) >= 0.5
            star_display = "★" * full_stars
            if has_half_star:
                star_display += "☆"
            remaining_stars = 5 - len(star_display)
            star_display += "☆" * remaining_stars
            
            st.markdown(f"""
            <div class="bottom-card">
                <div class="metric-value">{avg_score:.2f}</div>
                <div class="stars">{star_display}</div>
                <div class="metric-title">Average Review Score</div>
            </div>
            """, unsafe_allow_html=True)
        else:
            st.info("Customer satisfaction data not available")
    
    # Footer
    st.markdown("---")
    st.markdown(f"**Data Period:** {selected_year} | **Last Updated:** {pd.Timestamp.now().strftime('%Y-%m-%d %H:%M')}")

if __name__ == "__main__":
    main()