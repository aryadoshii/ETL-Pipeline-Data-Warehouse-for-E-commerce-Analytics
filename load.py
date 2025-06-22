# etl/load.py
import sqlite3
import pandas as pd

DB_PATH = 'techcorp_cleaned.db'

def create_database_schema():
    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.cursor()
        cursor.execute("DROP TABLE IF EXISTS orders;")
        cursor.execute("DROP TABLE IF EXISTS customers;")
        cursor.execute("DROP TABLE IF EXISTS products;")

        cursor.execute("""
        CREATE TABLE customers (
            customer_id INTEGER PRIMARY KEY, name TEXT, email TEXT, phone TEXT,
            address TEXT, city TEXT, state TEXT, postal_code TEXT,
            registration_date DATETIME, status TEXT
        );
        """)

        cursor.execute("""
        CREATE TABLE products (
            product_id TEXT PRIMARY KEY, name TEXT, description TEXT, category TEXT,
            brand TEXT, price REAL, stock_quantity INTEGER, rating REAL, is_active BOOLEAN
        );
        """)

        cursor.execute("""
        CREATE TABLE orders (
            order_id TEXT PRIMARY KEY, customer_id INTEGER, product_id TEXT,
            order_date DATETIME, quantity INTEGER, total_amount REAL, status TEXT,
            FOREIGN KEY (customer_id) REFERENCES customers(customer_id),
            FOREIGN KEY (product_id) REFERENCES products(product_id)
        );
        """)
        print(f"Database '{DB_PATH}' created/reset with target schema.")

def load_data_to_db(df: pd.DataFrame, table_name: str):
    with sqlite3.connect(DB_PATH) as conn:
        df.to_sql(table_name, conn, if_exists='append', index=False)
        print(f"Data successfully loaded into table '{table_name}'.")