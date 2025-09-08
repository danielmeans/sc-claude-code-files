"""
Data loading and processing module for e-commerce analytics.

This module handles loading, cleaning, and preprocessing of e-commerce datasets
including orders, customers, products, reviews, and order items.
"""

import pandas as pd
import numpy as np
from typing import Dict, Tuple, Optional
import warnings

warnings.filterwarnings('ignore', category=pd.errors.SettingWithCopyWarning)


class EcommerceDataLoader:
    """
    Handles loading and preprocessing of e-commerce data files.
    
    Attributes:
        data_dir (str): Directory path containing the CSV files
        datasets (Dict[str, pd.DataFrame]): Dictionary of loaded datasets
    """
    
    def __init__(self, data_dir: str = 'ecommerce_data'):
        """
        Initialize the data loader.
        
        Args:
            data_dir (str): Directory containing the CSV files
        """
        self.data_dir = data_dir
        self.datasets = {}
        
    def load_all_datasets(self) -> Dict[str, pd.DataFrame]:
        """
        Load all e-commerce datasets from CSV files.
        
        Returns:
            Dict[str, pd.DataFrame]: Dictionary containing all loaded datasets
        """
        file_mapping = {
            'orders': 'orders_dataset.csv',
            'order_items': 'order_items_dataset.csv',
            'products': 'products_dataset.csv',
            'customers': 'customers_dataset.csv',
            'reviews': 'order_reviews_dataset.csv',
            'payments': 'order_payments_dataset.csv'
        }
        
        for dataset_name, filename in file_mapping.items():
            try:
                filepath = f"{self.data_dir}/{filename}"
                self.datasets[dataset_name] = pd.read_csv(filepath)
                print(f"Loaded {dataset_name}: {self.datasets[dataset_name].shape}")
            except FileNotFoundError:
                print(f"Warning: {filename} not found in {self.data_dir}")
                
        return self.datasets
    
    def preprocess_orders(self) -> pd.DataFrame:
        """
        Preprocess orders dataset with datetime conversion and feature extraction.
        
        Returns:
            pd.DataFrame: Processed orders dataframe
        """
        if 'orders' not in self.datasets:
            raise ValueError("Orders dataset not loaded")
            
        orders = self.datasets['orders'].copy()
        
        # Convert datetime columns
        datetime_cols = ['order_purchase_timestamp', 'order_approved_at', 
                        'order_delivered_carrier_date', 'order_delivered_customer_date',
                        'order_estimated_delivery_date']
        
        for col in datetime_cols:
            if col in orders.columns:
                orders[col] = pd.to_datetime(orders[col])
        
        # Extract date components
        orders['purchase_year'] = orders['order_purchase_timestamp'].dt.year
        orders['purchase_month'] = orders['order_purchase_timestamp'].dt.month
        orders['purchase_date'] = orders['order_purchase_timestamp'].dt.date
        
        return orders
    
    def create_sales_dataset(self, target_year: Optional[int] = None, 
                           target_month: Optional[int] = None,
                           include_canceled: bool = False) -> pd.DataFrame:
        """
        Create a comprehensive sales dataset by merging orders and order_items.
        
        Args:
            target_year (int, optional): Filter data for specific year
            target_month (int, optional): Filter data for specific month
            include_canceled (bool): Whether to include canceled orders
            
        Returns:
            pd.DataFrame: Merged sales dataset with date filtering applied
        """
        if 'orders' not in self.datasets or 'order_items' not in self.datasets:
            raise ValueError("Required datasets (orders, order_items) not loaded")
        
        # Process orders
        orders = self.preprocess_orders()
        order_items = self.datasets['order_items'].copy()
        
        # Merge datasets
        sales_data = pd.merge(
            left=order_items[['order_id', 'order_item_id', 'product_id', 'price', 'freight_value']],
            right=orders[['order_id', 'customer_id', 'order_status', 'order_purchase_timestamp', 
                         'order_delivered_customer_date', 'purchase_year', 'purchase_month']],
            on='order_id'
        )
        
        # Filter by order status
        if not include_canceled:
            sales_data = sales_data[sales_data['order_status'] == 'delivered']
        
        # Apply date filters
        if target_year is not None:
            sales_data = sales_data[sales_data['purchase_year'] == target_year]
            
        if target_month is not None:
            sales_data = sales_data[sales_data['purchase_month'] == target_month]
        
        return sales_data
    
    def create_customer_sales_dataset(self, sales_data: pd.DataFrame) -> pd.DataFrame:
        """
        Enhance sales dataset with customer information.
        
        Args:
            sales_data (pd.DataFrame): Base sales dataset
            
        Returns:
            pd.DataFrame: Sales dataset with customer information
        """
        if 'customers' not in self.datasets:
            raise ValueError("Customers dataset not loaded")
            
        customers = self.datasets['customers'].copy()
        
        return pd.merge(
            sales_data,
            customers[['customer_id', 'customer_state', 'customer_city', 'customer_zip_code_prefix']],
            on='customer_id'
        )
    
    def create_product_sales_dataset(self, sales_data: pd.DataFrame) -> pd.DataFrame:
        """
        Enhance sales dataset with product information.
        
        Args:
            sales_data (pd.DataFrame): Base sales dataset
            
        Returns:
            pd.DataFrame: Sales dataset with product information
        """
        if 'products' not in self.datasets:
            raise ValueError("Products dataset not loaded")
            
        products = self.datasets['products'].copy()
        
        return pd.merge(
            sales_data,
            products[['product_id', 'product_category_name', 'product_weight_g']],
            on='product_id'
        )
    
    def create_review_dataset(self, sales_data: pd.DataFrame) -> pd.DataFrame:
        """
        Create dataset combining sales and review information.
        
        Args:
            sales_data (pd.DataFrame): Base sales dataset
            
        Returns:
            pd.DataFrame: Dataset with sales and review information
        """
        if 'reviews' not in self.datasets:
            raise ValueError("Reviews dataset not loaded")
            
        reviews = self.datasets['reviews'].copy()
        
        # Merge with reviews
        sales_reviews = pd.merge(
            sales_data,
            reviews[['order_id', 'review_score', 'review_creation_date']],
            on='order_id'
        )
        
        # Calculate delivery speed (only for delivered orders with delivery dates)
        delivered_mask = (
            (sales_reviews['order_status'] == 'delivered') & 
            (sales_reviews['order_delivered_customer_date'].notna())
        )
        
        if delivered_mask.any():
            delivery_delta = (
                sales_reviews.loc[delivered_mask, 'order_delivered_customer_date'] - 
                sales_reviews.loc[delivered_mask, 'order_purchase_timestamp']
            )
            sales_reviews.loc[delivered_mask, 'delivery_days'] = delivery_delta.dt.days
        
        return sales_reviews
    
    def get_data_summary(self) -> Dict:
        """
        Get summary statistics of all loaded datasets.
        
        Returns:
            Dict: Summary information about each dataset
        """
        summary = {}
        
        for name, df in self.datasets.items():
            summary[name] = {
                'shape': df.shape,
                'columns': list(df.columns),
                'memory_usage_mb': df.memory_usage(deep=True).sum() / (1024 * 1024),
                'missing_values': df.isnull().sum().to_dict()
            }
            
        return summary


def categorize_delivery_speed(days: float) -> str:
    """
    Categorize delivery speed based on number of days.
    
    Args:
        days (float): Number of delivery days
    
    Returns:
        str: Delivery speed category
    """
    if pd.isna(days):
        return 'Unknown'
    elif days <= 3:
        return '1-3 days'
    elif days <= 7:
        return '4-7 days'
    else:
        return '8+ days'


def load_and_prepare_data(data_dir: str = 'ecommerce_data', 
                         target_year: Optional[int] = None,
                         target_month: Optional[int] = None) -> Tuple[pd.DataFrame, Dict[str, pd.DataFrame]]:
    """
    Convenience function to load and prepare all datasets.
    
    Args:
        data_dir (str): Directory containing CSV files
        target_year (int, optional): Filter data for specific year
        target_month (int, optional): Filter data for specific month
        
    Returns:
        Tuple containing:
            - Main sales dataset (pd.DataFrame)
            - Dictionary of all raw datasets (Dict[str, pd.DataFrame])
    """
    loader = EcommerceDataLoader(data_dir)
    datasets = loader.load_all_datasets()
    
    # Create main sales dataset
    sales_data = loader.create_sales_dataset(target_year, target_month)
    
    return sales_data, datasets