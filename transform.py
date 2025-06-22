# etl/transform.py
import pandas as pd
import numpy as np

def _clean_and_coerce_to_numeric(series: pd.Series):
    return pd.to_numeric(series, errors='coerce')

def clean_customers(df: pd.DataFrame) -> pd.DataFrame:
    print("Cleaning customer data...")
    df.replace("", np.nan, inplace=True)
    df['customer_id'] = df['customer_id'].fillna(df['cust_id'].str.replace('CUST_', ''))
    df['name'] = df['full_name'].fillna(df['customer_name'])
    df['email'] = df['email'].fillna(df['email_address'])
    df['phone'] = df['phone'].fillna(df['phone_number'])
    df['postal_code'] = df['postal_code'].fillna(df['zip_code'])
    df['registration_date'] = df['reg_date'].fillna(df['registration_date'])
    df['status'] = df['customer_status'].fillna(df['status'])

    state_map = {'New York': 'NY', 'California': 'CA'}
    df['state'] = df['state'].replace(state_map)
    city_map = {'new_york': 'New York', 'nyc': 'New York', 'la': 'Los Angeles'}
    df['city'] = df['city'].str.lower().replace(city_map).str.title()
    df['status'] = df['status'].str.lower().fillna('unknown')

    df['customer_id'] = _clean_and_coerce_to_numeric(df['customer_id'])
    df['registration_date'] = pd.to_datetime(df['registration_date'], errors='coerce')

    final_df = df[['customer_id', 'name', 'email', 'phone', 'address', 'city', 'state', 'postal_code', 'registration_date', 'status']].copy()
    final_df.dropna(subset=['customer_id'], inplace=True)
    final_df['customer_id'] = final_df['customer_id'].astype(int)
    print("Customer data cleaned.")
    return final_df

def clean_products(df: pd.DataFrame) -> pd.DataFrame:
    print("Cleaning product data...")
    df.replace("", np.nan, inplace=True)
    df['name'] = df['product_name'].fillna(df['item_name'])
    df['category'] = df['product_category'].fillna(df['category']).str.title()
    df['brand'] = df['brand'].fillna(df['manufacturer']).str.title().str.replace('Brand-C', 'Brand C').str.replace('Brand_B', 'Brand B')
    df['stock_quantity'] = df['stock_quantity'].fillna(df['stock_level'])
    
    active_map = {'yes': True, 'no': False, 1: True, 0: False, True: True, False: False}
    df['is_active'] = df['is_active'].map(active_map).fillna(False).astype(bool)

    df['price'] = _clean_and_coerce_to_numeric(df['price'])
    df['rating'] = _clean_and_coerce_to_numeric(df['rating'])
    df['stock_quantity'] = _clean_and_coerce_to_numeric(df['stock_quantity'])

    final_df = df[['product_id', 'name', 'description', 'category', 'brand', 'price', 'stock_quantity', 'rating', 'is_active']].copy()
    final_df.dropna(subset=['product_id'], inplace=True)
    print("Product data cleaned.")
    return final_df

def clean_orders(df: pd.DataFrame) -> pd.DataFrame:
    print("Cleaning order data...")
    df.replace("", np.nan, inplace=True)
    df['order_id'] = df['order_id'].fillna(df['ord_id'])
    df['customer_id'] = df['customer_id'].fillna(df['cust_id'])
    df['product_id'] = df['product_id'].fillna(df['item_id'].apply(lambda x: f'PROD_{int(x):03d}' if pd.notnull(x) else x))
    df['quantity'] = df['quantity'].fillna(df['qty'])
    df['total_amount'] = df['total_amount'].fillna(df['order_total'])
    df['order_date'] = df['order_datetime'].fillna(df['order_date'])
    df['status'] = df['order_status'].fillna(df['status'])

    df['status'] = df['status'].str.lower().fillna('unknown')
    df['customer_id'] = df['customer_id'].astype(str).str.replace('CUST_', '', regex=False)
    
    df['order_date'] = pd.to_datetime(df['order_date'], errors='coerce')
    df['quantity'] = _clean_and_coerce_to_numeric(df['quantity'])
    df['total_amount'] = _clean_and_coerce_to_numeric(df['total_amount'])
    df['customer_id'] = _clean_and_coerce_to_numeric(df['customer_id'])

    final_df = df[['order_id', 'customer_id', 'product_id', 'order_date', 'quantity', 'total_amount', 'status']].copy()
    final_df.dropna(subset=['order_id', 'customer_id', 'product_id', 'order_date'], inplace=True)
    final_df['customer_id'] = final_df['customer_id'].astype(int)
    final_df['quantity'] = final_df['quantity'].astype(int)
    print("Order data cleaned.")
    return final_df