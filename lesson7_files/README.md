# E-commerce Business Intelligence Analysis

A comprehensive, refactored e-commerce data analysis framework providing business insights through revenue analysis, product performance, geographic distribution, and customer experience metrics.

## Overview

This project transforms raw e-commerce data into actionable business intelligence through:
- **Configurable Analysis**: Easily adjust time periods and filters
- **Comprehensive Metrics**: Revenue, product, geographic, and customer insights
- **Clean Architecture**: Modular code with reusable components
- **Interactive Visualizations**: Charts, maps, and performance dashboards
- **Strategic Recommendations**: Data-driven business insights

## Project Structure

```
├── EDA_Refactored.ipynb      # Main analysis notebook
├── data_loader.py            # Data loading and preprocessing module
├── business_metrics.py       # Business metrics calculation module
├── requirements.txt          # Python dependencies
├── ecommerce_data/          # CSV data files
│   ├── orders_dataset.csv
│   ├── order_items_dataset.csv
│   ├── products_dataset.csv
│   ├── customers_dataset.csv
│   ├── order_reviews_dataset.csv
│   └── order_payments_dataset.csv
└── README.md                # This file
```

## Installation

1. **Clone or download** the project files to your local machine

2. **Install dependencies**:
```bash
pip install -r requirements.txt
```

3. **Verify data files** are present in the `ecommerce_data/` directory

4. **Launch the application**:

   **For Streamlit Dashboard**:
   ```bash
   streamlit run app.py
   ```

   **For Jupyter Notebook Analysis**:
   ```bash
   jupyter notebook EDA_Refactored.ipynb
   ```

## Quick Start

### Streamlit Dashboard

1. **Launch the dashboard**: 
   ```bash
   streamlit run app.py
   ```

2. **Use the interface**:
   - **Year Filter**: Select analysis year from dropdown (top-right)
   - **KPI Cards**: View key metrics with trend indicators
   - **Interactive Charts**: Explore visualizations in 2x2 grid
   - **Customer Metrics**: Monitor satisfaction and delivery performance

3. **Dashboard Features**:
   - **Real-time Filtering**: All charts update when year changes
   - **Trend Indicators**: Green/red arrows showing performance direction
   - **Professional Styling**: Business-ready interface with uniform card heights
   - **Interactive Maps**: Plotly choropleth for geographic insights

### Jupyter Notebook Analysis

1. **Open the notebook**: `EDA_Refactored.ipynb`
2. **Configure analysis parameters** in the first cell:
```python
ANALYSIS_YEAR = 2023          # Primary year for analysis
COMPARISON_YEAR = 2022        # Year for comparison metrics
ANALYSIS_MONTH = None         # Optional: specific month (1-12)
DATA_DIRECTORY = 'ecommerce_data'
```
3. **Run all cells** to generate the complete analysis

### Customizing the Analysis

#### Time Period Analysis
```python
# Analyze specific month
ANALYSIS_MONTH = 6  # June only
ANALYSIS_YEAR = 2023

# Year-over-year comparison
ANALYSIS_YEAR = 2023
COMPARISON_YEAR = 2022

# Single year analysis
COMPARISON_YEAR = None
```

#### Using the Modules Independently

**Data Loading**:
```python
from data_loader import EcommerceDataLoader

loader = EcommerceDataLoader('ecommerce_data')
datasets = loader.load_all_datasets()
sales_data = loader.create_sales_dataset(target_year=2023)
```

**Business Metrics**:
```python
from business_metrics import BusinessMetricsCalculator

calculator = BusinessMetricsCalculator(sales_data)
report = calculator.generate_comprehensive_report(2023, 2022)
```

**Visualizations**:
```python
from business_metrics import MetricsVisualizer

visualizer = MetricsVisualizer(report)
fig = visualizer.plot_revenue_trend()
```

## Features

### Data Processing
- **Automated Loading**: Handles all CSV files with error checking
- **Data Cleaning**: Fixes data types, handles missing values
- **Feature Engineering**: Creates derived metrics and categorizations
- **Flexible Filtering**: Time-based and status-based filtering

### Business Metrics
- **Revenue Analysis**: Total revenue, growth rates, trends
- **Order Metrics**: Order volume, average order value
- **Product Performance**: Category analysis, revenue distribution
- **Geographic Insights**: State-level performance analysis
- **Customer Experience**: Satisfaction scores, delivery performance

### Visualizations
- **Revenue Trends**: Month-over-month performance charts
- **Product Analysis**: Category performance bar charts
- **Geographic Maps**: Interactive state-level choropleth maps
- **Customer Metrics**: Satisfaction and delivery performance charts

## Dashboard Layout

### Header Section
- **Title**: E-commerce Business Intelligence Dashboard (left-aligned)
- **Year Filter**: Dropdown selector for analysis period (right-aligned)

### KPI Cards Row (4 Cards)
1. **Total Revenue**: Shows current year revenue with trend vs previous year
2. **Monthly Growth**: Average month-over-month revenue growth rate
3. **Average Order Value**: Revenue per order with trend indicator
4. **Total Orders**: Order volume with year-over-year comparison

### Charts Grid (2x2 Layout)

**Top Row**:
- **Revenue Trend**: Line chart comparing current vs previous year
  - Solid line for current period, dashed line for comparison
  - Grid lines and formatted Y-axis ($300K format)
- **Top 10 Categories**: Horizontal bar chart with blue gradient
  - Sorted descending by revenue
  - Values formatted as $300K, $2M

**Bottom Row**:
- **Revenue by State**: US choropleth map with blue color gradient
- **Satisfaction vs Delivery**: Bar chart showing review scores by delivery time buckets

### Customer Experience Cards (Bottom Row)
- **Average Delivery Time**: Shows delivery performance with trend
- **Review Score**: Large number display with star rating visualization

### Module Usage

#### Data Loading Module
```python
from data_loader import EcommerceDataLoader, load_and_process_data

# Quick start
loader, processed_data = load_and_process_data('ecommerce_data/')

# Advanced usage
loader = EcommerceDataLoader('ecommerce_data/')
loader.load_raw_data()
processed_data = loader.process_all_data()

# Create filtered dataset
sales_data = loader.create_sales_dataset(
    year_filter=2023,
    month_filter=None,
    status_filter='delivered'
)
```

#### Business Metrics Module
```python
from business_metrics import BusinessMetricsCalculator, MetricsVisualizer

# Calculate metrics
metrics_calc = BusinessMetricsCalculator(sales_data)
report = metrics_calc.generate_comprehensive_report(
    current_year=2023,
    previous_year=2022
)

# Create visualizations
visualizer = MetricsVisualizer(report)
revenue_fig = visualizer.plot_revenue_trend()
category_fig = visualizer.plot_category_performance()
```

## Key Business Metrics

### Revenue Metrics
- **Total Revenue**: Sum of all delivered order item prices
- **Revenue Growth Rate**: Year-over-year percentage change
- **Average Order Value (AOV)**: Average total value per order
- **Monthly Growth Trends**: Month-over-month performance

### Product Performance
- **Category Revenue**: Revenue by product category
- **Market Share**: Percentage of total revenue by category
- **Category Diversity**: Distribution across product lines

### Geographic Analysis
- **State Performance**: Revenue and order count by state
- **Market Penetration**: Number of active markets
- **Regional AOV**: Average order value by geographic region

### Customer Experience
- **Review Scores**: Average satisfaction rating (1-5 scale)
- **Satisfaction Distribution**: Percentage of high/low ratings
- **Delivery Performance**: Average delivery time and speed metrics

## Output Examples

### Console Output
```
BUSINESS METRICS SUMMARY - 2023
============================================================

REVENUE PERFORMANCE:
  Total Revenue: $3,360,294.74
  Total Orders: 4,635
  Average Order Value: $724.98
  Revenue Growth: -2.5%

CUSTOMER SATISFACTION:
  Average Review Score: 4.10/5.0
  High Satisfaction (4+): 84.2%

DELIVERY PERFORMANCE:
  Average Delivery Time: 8.0 days
  Fast Delivery (≤3 days): 28.5%
```

### Generated Visualizations
- Monthly revenue trend line charts
- Top product category horizontal bar charts
- Interactive US state choropleth maps
- Customer satisfaction distribution charts

## Customization Options

### Adding New Metrics
1. Extend the `BusinessMetricsCalculator` class in `business_metrics.py`
2. Add visualization methods to `MetricsVisualizer` class
3. Update the notebook to display new metrics

### Custom Visualizations
```python
# Example: Custom visualization
def plot_custom_metric(self, data):
    fig, ax = plt.subplots(figsize=(12, 6))
    # Your visualization code
    return fig
```

### Data Source Modifications
- Modify `data_loader.py` to handle different CSV structures
- Update column mappings in the `EcommerceDataLoader` class
- Add new data validation rules

## Troubleshooting

### Common Issues

1. **Module Import Errors**:
   - Ensure all files are in the same directory
   - Check Python path configuration

2. **Missing Data Files**:
   - Verify CSV files are in the `ecommerce_data/` directory
   - Check file naming matches expected patterns

3. **Empty Results**:
   - Verify date filters match available data
   - Check order status filtering

4. **Visualization Issues**:
   - Ensure all required packages are installed
   - Check Plotly version compatibility for interactive maps

### Performance Optimization
- For large datasets, consider chunked processing
- Use data sampling for initial exploration
- Implement caching for repeated analysis

## Dashboard Features

### Layout Structure
- **Header**: Title with year selection filter (applies globally)
- **KPI Row**: 4 metric cards with trend indicators
  - Total Revenue, Monthly Growth, Average Order Value, Total Orders
  - Color-coded trends (green for positive, red for negative)
- **Charts Grid**: 2x2 interactive visualization layout
  - Revenue trend (current vs previous year)
  - Top 10 product categories bar chart
  - US state choropleth map
  - Customer satisfaction vs delivery time analysis
- **Bottom Row**: Customer experience metrics
  - Average delivery time with trend
  - Review score with star rating

### Technical Features
- **Real-time Filtering**: All visualizations update automatically
- **Professional Styling**: Business-ready interface with uniform card heights
- **Plotly Charts**: Interactive, publication-quality visualizations
- **Responsive Design**: Adapts to different screen sizes
- **Error Handling**: Graceful handling of missing data

## Future Enhancements

### Planned Features
- Real-time data connections
- Predictive analytics and forecasting
- Customer segmentation analysis
- A/B testing framework
- Automated report scheduling
- Export functionality (PDF reports)

### Extension Ideas
- Integration with business intelligence tools
- API endpoints for metrics access
- Machine learning model integration
- Advanced statistical analysis
- Mobile-responsive improvements

## Contributing

To extend this analysis framework:

1. Follow the existing code structure and documentation patterns
2. Add comprehensive docstrings to new functions
3. Include unit tests for new business logic
4. Update this README with new features

## License

This project is provided as-is for educational and business analysis purposes.

---

**Note**: This framework is designed to be easily maintained and extended for ongoing business intelligence needs. The modular architecture ensures that updates to data sources or metric calculations can be made without affecting the overall analysis structure.