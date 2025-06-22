# app.py

# --- 1. Import necessary libraries ---
import streamlit as st
import pandas as pd
import sqlite3
import plotly.express as px

# --- 2. Define the path to your clean database ---
DB_PATH = 'techcorp_cleaned.db'


# --- 3. Function to load and prepare data (with caching) ---
# The @st.cache_data decorator is a powerful Streamlit feature.
# It tells Streamlit to run this function only once. If the user interacts with a widget,
# Streamlit will reuse the stored output instead of re-reading the database every time,
# making your app much faster.
# Find this function in your code
@st.cache_data(ttl=600)
def load_unified_data():
    """Connects to the SQLite DB, reads all tables, and merges them."""
    print("Loading data from database...")
    with sqlite3.connect(DB_PATH) as conn:
        orders = pd.read_sql_query("SELECT * FROM orders", conn, parse_dates=['order_date'])
        customers = pd.read_sql_query("SELECT * FROM customers", conn, parse_dates=['registration_date'])
        products = pd.read_sql_query("SELECT * FROM products", conn)
    
    # --- THIS IS THE FIX ---
    # Convert the timezone-aware 'order_date' column to a timezone-naive one.
    # .dt accessor lets us work with datetime properties.
    # .tz_localize(None) removes the timezone information.
    orders['order_date'] = orders['order_date'].dt.tz_localize(None)
    # -----------------------
    
    # Merge the tables into one large, easy-to-analyze DataFrame
    full_df = pd.merge(orders, customers, on='customer_id', how='left')
    full_df = pd.merge(full_df, products, on='product_id', how='left', suffixes=('_customer', '_product'))
    
    # Minor cleanup for display
    full_df['is_active'] = full_df['is_active'].apply(lambda x: 'Active' if x else 'Inactive')
    
    print("Data loading complete.")
    return full_df

# --- 4. Page Configuration ---
# This should be the first Streamlit command in your script.
st.set_page_config(
    page_title="TechCorp E-commerce Dashboard",
    page_icon="🛒",
    layout="wide"  # "wide" layout uses the full screen width
)

# --- 5. Load the data using the cached function ---
df = load_unified_data()

# --- 6. Main Dashboard Title ---
st.title("🛒 TechCorp Unified E-commerce Dashboard")
st.markdown("Explore sales, customer, and product data from our unified pipeline.")


# --- 7. Sidebar for Filters ---
st.sidebar.header("Dashboard Filters")

# Date Range Filter
min_date = df['order_date'].min().to_pydatetime()
max_date = df['order_date'].max().to_pydatetime()
date_range = st.sidebar.date_input(
    "Select Date Range",
    value=(min_date, max_date), # Default value is the full range
    min_value=min_date,
    max_value=max_date
)

# Handle the case where the user might only select one date
if len(date_range) == 2:
    start_date, end_date = date_range
else:
    start_date, end_date = min_date, max_date # Fallback to the full range

# Product Category Filter
all_categories = df['category'].dropna().unique()
selected_categories = st.sidebar.multiselect(
    "Select Product Category",
    options=all_categories,
    default=all_categories # Default to all categories selected
)

# --- 8. Apply the filters to the DataFrame ---
# This is the core of the interactivity.
filtered_df = df[
    (df['order_date'] >= pd.to_datetime(start_date)) & 
    (df['order_date'] <= pd.to_datetime(end_date)) &
    (df['category'].isin(selected_categories))
].copy()


# --- 9. Display Key Performance Indicators (KPIs) ---
st.header("Key Performance Indicators")
kpi1, kpi2, kpi3 = st.columns(3) # Create three columns for the KPIs

total_revenue = filtered_df['total_amount'].sum()
total_orders = filtered_df['order_id'].nunique()
unique_customers = filtered_df['customer_id'].nunique()

# Use st.metric to display KPIs in a nice format
kpi1.metric(label="Total Revenue", value=f"${total_revenue:,.2f}")
kpi2.metric(label="Total Orders", value=f"{total_orders:,}")
kpi3.metric(label="Unique Customers", value=f"{unique_customers:,}")


# --- 10. Visualizations ---
st.header("Visual Analytics")

# Create two columns for side-by-side charts
viz1, viz2 = st.columns(2)

# Chart 1: Sales Over Time
with viz1:
    # We need to group data by month to see the trend
    filtered_df['order_month'] = filtered_df['order_date'].dt.to_period('M').astype(str)
    sales_over_time = filtered_df.groupby('order_month')['total_amount'].sum().reset_index()
    fig_sales = px.line(sales_over_time, x='order_month', y='total_amount', 
                        title='Monthly Sales Revenue',
                        labels={'order_month': 'Month', 'total_amount': 'Revenue'})
    st.plotly_chart(fig_sales, use_container_width=True)

# Chart 2: Top 10 Product Categories by Revenue
with viz2:
    sales_by_category = filtered_df.groupby('category')['total_amount'].sum().nlargest(10).sort_values().reset_index()
    fig_cat_sales = px.bar(sales_by_category, y='category', x='total_amount', orientation='h', 
                           title='Top 10 Categories by Revenue',
                           labels={'category': 'Product Category', 'total_amount': 'Total Revenue'})
    st.plotly_chart(fig_cat_sales, use_container_width=True)


# --- 11. Data Explorer Table ---
st.header("Explore Cleaned & Unified Data")
st.dataframe(filtered_df.drop(columns=['order_month']).reset_index(drop=True))


# --- 12. Documentation Section ---
with st.expander("View Data Quality & Cleaning Summary"):
    st.subheader("Data Cleaning Process Overview")
    st.markdown("""
    The raw data from three separate acquisitions was heavily inconsistent. The following key steps were taken to create the unified dataset you see here:
    
    - **Column Coalescing:** Multiple columns representing the same information (e.g., `cust_id`, `customer_id`; `status`, `customer_status`) were merged into a single source-of-truth column.
    - **Data Type Correction:** Numeric fields stored as text (e.g., `total_spent`) and boolean fields with mixed representations (e.g., `is_active`) were converted to their proper types.
    - **Format Standardization:** Textual data like city names ('NYC', 'new_york'), state names ('California', 'CA'), and statuses ('ACTIVE', 'pending') were standardized to a consistent format.
    - **Foreign Key Validation:** Orders were cross-validated against the customer and product tables. Any order referencing a non-existent customer or product was removed to ensure relational integrity.
    
    This process ensures that all KPIs and analytics are accurate and reliable.
    """)