"""
Task 3: Data Analysis with Pandas
===================================
Demonstrates:
- Creating and loading DataFrames
- Cleaning data (nulls, duplicates, types)
- Aggregations, groupby, filtering
- Descriptive statistics
- Exporting results to CSV
"""

import pandas as pd
import os


# ──────────────────────────────────────────
# 1. Create Sample Dataset
# ──────────────────────────────────────────
def create_sales_data():
    data = {
        "OrderID":    [101, 102, 103, 104, 105, 106, 107, 108, 109, 110],
        "Product":    ["Laptop", "Phone", "Tablet", "Laptop", "Phone",
                       "Tablet", "Laptop", "Phone", None, "Tablet"],
        "Category":   ["Electronics"] * 10,
        "Quantity":   [2, 5, 3, 1, 4, 6, 2, 3, 1, 5],
        "UnitPrice":  [800, 300, 450, 800, 300, 450, 800, 300, 300, 450],
        "Region":     ["North", "South", "East", "West", "North",
                       "South", "East", "West", "North", "South"],
        "SaleDate":   pd.to_datetime([
            "2024-01-05","2024-01-10","2024-01-15","2024-02-01","2024-02-14",
            "2024-02-20","2024-03-03","2024-03-15","2024-03-22","2024-03-30"
        ]),
        "Discount":   [0.05, 0.10, 0.0, 0.05, 0.10, 0.0, 0.05, 0.10, 0.0, 0.15],
    }
    df = pd.DataFrame(data)
    # Add revenue column
    df["Revenue"] = df["Quantity"] * df["UnitPrice"] * (1 - df["Discount"])
    return df


# ──────────────────────────────────────────
# 2. Data Cleaning
# ──────────────────────────────────────────
def clean_data(df):
    print("\n=== Data Cleaning ===")
    print(f"  Rows before cleaning : {len(df)}")
    print(f"  Missing values:\n{df.isnull().sum()[df.isnull().sum() > 0]}")

    # Fill missing Product with 'Unknown'
    df["Product"] = df["Product"].fillna("Unknown")

    # Remove duplicates
    df = df.drop_duplicates()

    print(f"  Rows after cleaning  : {len(df)}")
    print(f"  Dtypes:\n{df.dtypes}")
    return df


# ──────────────────────────────────────────
# 3. Descriptive Statistics
# ──────────────────────────────────────────
def describe_data(df):
    print("\n=== Descriptive Statistics ===")
    print(df[["Quantity", "UnitPrice", "Revenue"]].describe().round(2))


# ──────────────────────────────────────────
# 4. GroupBy Analysis
# ──────────────────────────────────────────
def groupby_analysis(df):
    print("\n=== Revenue by Product ===")
    product_summary = df.groupby("Product").agg(
        Total_Revenue=("Revenue", "sum"),
        Total_Quantity=("Quantity", "sum"),
        Avg_Price=("UnitPrice", "mean"),
        Order_Count=("OrderID", "count")
    ).reset_index().sort_values("Total_Revenue", ascending=False)
    print(product_summary.to_string(index=False))

    print("\n=== Revenue by Region ===")
    region_summary = df.groupby("Region")["Revenue"].sum().reset_index()
    region_summary.columns = ["Region", "Total_Revenue"]
    print(region_summary.to_string(index=False))

    return product_summary, region_summary


# ──────────────────────────────────────────
# 5. Filtering
# ──────────────────────────────────────────
def filter_data(df):
    print("\n=== Orders with Revenue > 1000 ===")
    high_value = df[df["Revenue"] > 1000][["OrderID", "Product", "Revenue", "Region"]]
    print(high_value.to_string(index=False))

    print("\n=== Orders in Q1 2024 (Jan–Mar) ===")
    q1 = df[(df["SaleDate"].dt.month >= 1) & (df["SaleDate"].dt.month <= 3)]
    print(f"  Q1 Orders: {len(q1)} | Total Q1 Revenue: ₹{q1['Revenue'].sum():,.2f}")


# ──────────────────────────────────────────
# 6. Monthly Trend
# ──────────────────────────────────────────
def monthly_trend(df):
    print("\n=== Monthly Revenue Trend ===")
    df["Month"] = df["SaleDate"].dt.to_period("M")
    monthly = df.groupby("Month")["Revenue"].sum().reset_index()
    monthly.columns = ["Month", "Revenue"]
    for _, row in monthly.iterrows():
        bar = "█" * int(row["Revenue"] // 500)
        print(f"  {row['Month']}  ${row['Revenue']:>8,.2f}  {bar}")


# ──────────────────────────────────────────
# 7. Export
# ──────────────────────────────────────────
def export_results(df, product_summary, region_summary, output_dir):
    os.makedirs(output_dir, exist_ok=True)
    df.to_csv(f"{output_dir}/cleaned_sales.csv", index=False)
    product_summary.to_csv(f"{output_dir}/product_summary.csv", index=False)
    region_summary.to_csv(f"{output_dir}/region_summary.csv", index=False)
    print(f"\n[OK] Exported 3 CSV files to '{output_dir}/'")


# ──────────────────────────────────────────
# MAIN DEMO
# ──────────────────────────────────────────
if __name__ == "__main__":
    print("=" * 50)
    print("  Task 3: Data Analysis with Pandas")
    print("=" * 50)

    df = create_sales_data()
    print(f"\n[OK] Dataset created: {df.shape[0]} rows, {df.shape[1]} columns")
    print("\nFirst 5 rows:")
    print(df.head().to_string(index=False))

    df = clean_data(df)
    describe_data(df)
    product_summary, region_summary = groupby_analysis(df)
    filter_data(df)
    monthly_trend(df)
    export_results(df, product_summary, region_summary, "pandas_output")

    print("\n✅ Task 3 Complete!")
