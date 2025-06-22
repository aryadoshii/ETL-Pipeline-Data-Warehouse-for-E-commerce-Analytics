# etl/main.py

# --- THIS IS THE FIX for ModuleNotFoundError ---
# It tells the script to look for modules in the parent directory (Data_Project)
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
# ---------------------------------------------

from etl import extract, transform, load

def main():
    print("--- Starting TechCorp ETL Pipeline ---")

    load.create_database_schema()

    raw_customers = extract.extract_from_json('data/customers_messy_data.json')
    raw_products = extract.extract_from_json('data/products_inconsistent_data.json')
    raw_orders = extract.extract_from_csv('data/orders_unstructured_data.csv')

    cleaned_customers = transform.clean_customers(raw_customers)
    cleaned_products = transform.clean_products(raw_products)
    cleaned_orders = transform.clean_orders(raw_orders)
    
    valid_customer_ids = set(cleaned_customers['customer_id'])
    valid_product_ids = set(cleaned_products['product_id'])
    
    original_order_count = len(cleaned_orders)
    cleaned_orders = cleaned_orders[cleaned_orders['customer_id'].isin(valid_customer_ids)]
    cleaned_orders = cleaned_orders[cleaned_orders['product_id'].isin(valid_product_ids)]
    final_order_count = len(cleaned_orders)
    
    print(f"Validation: Removed {original_order_count - final_order_count} orders with invalid foreign keys.")

    load.load_data_to_db(cleaned_customers, 'customers')
    load.load_data_to_db(cleaned_products, 'products')
    load.load_data_to_db(cleaned_orders, 'orders')
    
    print("--- ETL Pipeline Completed Successfully ---")

if __name__ == "__main__":
    main()