# 🚀 TechCorp Unified E-commerce Data Pipeline



### An End-to-End Data Engineering Solution for the Take-Home Challenge

This repository contains a complete, production-style data engineering project built to solve the TechCorp take-home challenge. The objective was to ingest, clean, and analyze messy data from three disparate e-commerce platforms. This solution demonstrates a robust ETL pipeline, a user-friendly interactive dashboard, and an advanced AI-powered module for automated schema reconciliation.

---

## 📊 Interactive Dashboard Demo

The final output of the pipeline is an interactive Streamlit dashboard designed for business analysts. It provides at-a-glance KPIs and visualizations to track performance and explore the unified dataset.



*(This is a sample GIF. You can replace it with a recording of your own running dashboard!)*

---

## 🏛️ Project Architecture

The project follows a modern, modular data engineering workflow, separating concerns for maintainability and scalability.



1.  **Extract:** Raw data files (JSON, CSV) are ingested from their source locations.
2.  **Transform:** A series of robust Python scripts, organized by function, systematically clean, standardize, de-duplicate, and validate the data using the **Pandas** library.
3.  **Load:** The cleaned and validated data is loaded into a normalized **SQLite** database, with a clear schema, foreign keys, and indexes for query performance.
4.  **Analyze & Visualize:**
    *   The primary analytics layer is an interactive **Streamlit** web application (`app.py`) that queries the clean database.
    *   A bonus module uses the **Google Gemini AI** to automate the mapping of new, unknown data schemas.

---

## 🎯 Key Challenges & Solutions

This project successfully tackled numerous real-world data quality issues.

| Category | Challenge | Solution Implemented |
| :--- | :--- | :--- |
| 🔀 **Structural Chaos** | **Extreme Column Redundancy:** Fields like `cust_id`/`customer_id` and `order_status`/`status` existed for the same concept. | Implemented a **coalescing strategy** using `.fillna()` to merge data into a single, canonical column before dropping the redundant ones. |
| 🔢 **Data Type Issues** | **Inconsistent Data Types:** Numbers stored as text, dates in multiple formats, and booleans represented as strings (`'yes'`), integers (`1`), and booleans (`True`). | Created robust cleaning functions using `pd.to_datetime(errors='coerce')` and `pd.to_numeric` to standardize all data into proper `datetime`, `int`, `float`, and `boolean` types. |
| ✍️ **Formatting Errors** | **Inconsistent Categorical Data:** City names (`NYC`, `new_york`), states (`CA`, `California`), and statuses (`ACTIVE`, `pending`) lacked a standard format. | Used a combination of string methods (`.lower()`, `.title()`) and explicit mapping dictionaries to standardize all categorical data. |
| 🔗 **Relational Integrity** | **Orphan Records:** Orders existed that referenced `customer_id`s or `product_id`s not present in the master tables. | Implemented a **validation step** before the final load to cross-reference foreign keys, ensuring that only orders with valid customer and product references were loaded into the database. |

---

## 🤖 AI-Powered Schema Reconciliation (Bonus)

A key feature of this project is the use of a Large Language Model (LLM) to automate a traditionally manual data engineering task.

**Problem:** How do you efficiently ingest data from a new source when its column names don't match your database schema?

**Solution:**
1.  **Prompt Engineering:** A detailed prompt was crafted to instruct the Google Gemini AI to act as a "data mapping assistant."
2.  **API Integration:** The script sends the target schema and the new source columns to the Gemini API.
3.  **Automated Transformation:** The AI returns a structured JSON mapping. This JSON is programmatically used to automatically rename the columns of the new DataFrame, preparing it for the cleaning and loading process.

This demonstrates a powerful, scalable approach to reducing development time and onboarding new data sources with minimal friction.

---

## 🏃‍♀️ How to Run This Project Locally

Follow these steps to set up and run the entire pipeline and dashboard.

#### **1. Prerequisites**
*   Python 3.9+ installed on your system.

#### **2. Clone & Setup**
```bash
# Clone this repository to your local machine
git clone https://github.com/your-username/TechCorp-Data-Pipeline-Challenge.git

# Navigate into the project directory
cd TechCorp-Data-Pipeline-Challenge

# Install all required packages from the list
pip3 install -r requirements.txt
```
*(Replace `your-username` with your actual GitHub username)*

#### **3. Run the Full ETL Pipeline**
This command executes the entire data processing workflow. It will read the files from the `/data` directory and create a clean database named `techcorp_cleaned.db` in the root folder.
```bash
python3 etl/main.py
```

#### **4. Launch the Interactive Dashboard**
This command starts the Streamlit web server and will automatically open the dashboard in your default browser.
```bash
streamlit run app.py
```
You can now interact with the filters on the sidebar to explore the data!
