# Fabric notebook source

# METADATA ********************

# META {
# META   "kernel_info": {
# META     "name": "synapse_pyspark"
# META   },
# META   "dependencies": {}
# META }

# CELL ********************

# ─────────────────────────────────────────────
# Cell 1 – Connect to FSI_DB_02 using AAD token
# ─────────────────────────────────────────────
import csv
import os
import struct

import pandas as pd
import pyodbc
from IPython.display import display
from notebookutils import mssparkutils

# Fabric SQL endpoint — update these to match your workspace
FABRIC_SERVER   = os.environ.get("FABRIC_SQL_SERVER",   "zylcdhpgv7uezc6dy7d3ngcwyi-kmmmko2hhaeunmdplvelcbfeyu.database.fabric.microsoft.com")
FABRIC_DATABASE = os.environ.get("FABRIC_SQL_DATABASE", "FSI_DB_02")

# Acquire an AAD token scoped to Azure SQL / Fabric SQL
token        = mssparkutils.credentials.getToken("https://database.windows.net/")
token_bytes  = token.encode("UTF-16-LE")
token_struct = struct.pack(f"<I{len(token_bytes)}s", len(token_bytes), token_bytes)

conn = pyodbc.connect(
    f"Driver={{ODBC Driver 18 for SQL Server}};"
    f"Server={FABRIC_SERVER};"
    f"Database={FABRIC_DATABASE};",
    attrs_before={1256: token_struct},
)
cursor = conn.cursor()
print(f"Connected to {FABRIC_DATABASE} on {FABRIC_SERVER} ✓")

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# CELL ********************

# ─────────────────────────────────────────────
# Cell 2 – Load sample data from CSV files
# Reads CSV files from the data/ folder and inserts
# seed rows into the Sales schema for testing.
# ─────────────────────────────────────────────

DATA_DIR = os.environ.get("DATA_DIR", "./data")

# ── Regions ────────────────────────────────────────────────────────────
region_ids: dict[str, int] = {}
with open(f"{DATA_DIR}/Region.csv", newline="", encoding="utf-8") as fh:
    reader = csv.DictReader(fh)
    for row in reader:
        cursor.execute(
            """
            INSERT INTO Sales.Region (RegionCode, RegionName, Country)
            OUTPUT INSERTED.RegionID
            VALUES (?, ?, ?)
            """,
            row["RegionCode"], row["RegionName"], row["Country"],
        )
        region_ids[row["RegionCode"]] = int(cursor.fetchone()[0])
conn.commit()
print(f"Inserted {len(region_ids)} regions: {list(region_ids.keys())}")

# ── Product categories ─────────────────────────────────────────────────
category_ids: dict[str, int] = {}
with open(f"{DATA_DIR}/ProductCategory.csv", newline="", encoding="utf-8") as fh:
    reader = csv.DictReader(fh)
    for row in reader:
        cursor.execute(
            """
            INSERT INTO Sales.ProductCategory (Name)
            OUTPUT INSERTED.ProductCategoryID
            VALUES (?)
            """,
            row["Name"],
        )
        category_ids[row["Name"]] = int(cursor.fetchone()[0])
conn.commit()
print(f"Inserted {len(category_ids)} product categories")

# ── Products ───────────────────────────────────────────────────────────
product_ids: dict[str, int] = {}
with open(f"{DATA_DIR}/Product.csv", newline="", encoding="utf-8") as fh:
    reader = csv.DictReader(fh)
    for row in reader:
        cat_id = category_ids.get(row["CategoryName"])
        cursor.execute(
            """
            INSERT INTO Sales.Product
                (ProductNumber, Name, ProductCategoryID, Color, Size, StandardCost, ListPrice, StockQty)
            OUTPUT INSERTED.ProductID
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """,
            row["ProductNumber"], row["Name"], cat_id,
            row["Color"] or None, row["Size"] or None,
            float(row["StandardCost"]), float(row["ListPrice"]), int(row["StockQty"]),
        )
        product_ids[row["ProductNumber"]] = int(cursor.fetchone()[0])
conn.commit()
print(f"Inserted {len(product_ids)} products")

# ── Customers ──────────────────────────────────────────────────────────
customer_ids: dict[str, int] = {}
with open(f"{DATA_DIR}/Customer.csv", newline="", encoding="utf-8") as fh:
    reader = csv.DictReader(fh)
    for row in reader:
        reg_id = region_ids.get(row["RegionCode"])
        cursor.execute(
            """
            INSERT INTO Sales.Customer
                (FirstName, LastName, CompanyName, EmailAddress, Phone, RegionID)
            OUTPUT INSERTED.CustomerID
            VALUES (?, ?, ?, ?, ?, ?)
            """,
            row["FirstName"], row["LastName"], row["CompanyName"] or None,
            row["EmailAddress"] or None, row["Phone"] or None, reg_id,
        )
        customer_ids[row["EmailAddress"] or row["FirstName"] + " " + row["LastName"]] = int(cursor.fetchone()[0])
conn.commit()
print(f"Inserted {len(customer_ids)} customers")

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# CELL ********************

# ─────────────────────────────────────────────
# Cell 3 – Top 10 Customers by Total Revenue
# Uses the vTopCustomers view.
# ─────────────────────────────────────────────
sql_top_customers = """
SELECT TOP 10
    CustomerName,
    CompanyName,
    RegionName,
    TotalOrders,
    ROUND(TotalRevenue, 2) AS TotalRevenue
FROM Sales.vTopCustomers
ORDER BY TotalRevenue DESC;
"""

df_top_customers = pd.read_sql(sql_top_customers, conn)
print("=== Top 10 Customers by Revenue ===")
display(df_top_customers)

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# CELL ********************

# ─────────────────────────────────────────────
# Cell 4 – Sales by Product Category
# Uses the vSalesByCategory view.
# ─────────────────────────────────────────────
sql_category_sales = """
SELECT
    Category,
    TotalOrders,
    UnitsSold,
    ROUND(NetRevenue, 2) AS NetRevenue
FROM Sales.vSalesByCategory
ORDER BY NetRevenue DESC;
"""

df_category_sales = pd.read_sql(sql_category_sales, conn)
print("=== Sales by Product Category ===")
display(df_category_sales)

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# CELL ********************

# ─────────────────────────────────────────────
# Cell 5 – Monthly Sales Trend
# ─────────────────────────────────────────────
sql_monthly_trend = """
SELECT
    YEAR(OrderDate)  AS OrderYear,
    MONTH(OrderDate) AS OrderMonth,
    COUNT(*)                        AS TotalOrders,
    ROUND(SUM(SubTotal), 2)         AS SubTotal,
    ROUND(SUM(TaxAmt),   2)         AS TaxAmount,
    ROUND(SUM(SubTotal + TaxAmt + Freight), 2) AS TotalDue
FROM Sales.SalesOrder
GROUP BY YEAR(OrderDate), MONTH(OrderDate)
ORDER BY OrderYear, OrderMonth;
"""

df_monthly = pd.read_sql(sql_monthly_trend, conn)
print("=== Monthly Sales Trend ===")
display(df_monthly)

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# CELL ********************

# ─────────────────────────────────────────────
# Cell 6 – Revenue by Region
# ─────────────────────────────────────────────
sql_region_revenue = """
SELECT
    r.RegionName,
    r.Country,
    COUNT(DISTINCT so.SalesOrderID) AS TotalOrders,
    COUNT(DISTINCT so.CustomerID)   AS UniqueCustomers,
    ROUND(SUM(so.SubTotal), 2)      AS TotalRevenue
FROM Sales.Region r
JOIN Sales.Customer  c  ON r.RegionID   = c.RegionID
JOIN Sales.SalesOrder so ON c.CustomerID = so.CustomerID
GROUP BY r.RegionName, r.Country
ORDER BY TotalRevenue DESC;
"""

df_region = pd.read_sql(sql_region_revenue, conn)
print("=== Revenue by Region ===")
display(df_region)

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# CELL ********************

# ─────────────────────────────────────────────
# Cell 7 – Low Stock Products (StockQty < 10)
# ─────────────────────────────────────────────
sql_low_stock = """
SELECT
    p.ProductNumber,
    p.Name         AS ProductName,
    pc.Name        AS Category,
    p.ListPrice,
    p.StockQty
FROM Sales.Product         p
LEFT JOIN Sales.ProductCategory pc ON p.ProductCategoryID = pc.ProductCategoryID
WHERE p.StockQty < 10
ORDER BY p.StockQty ASC, p.ListPrice DESC;
"""

df_low_stock = pd.read_sql(sql_low_stock, conn)
print(f"=== Low Stock Products ({len(df_low_stock)} rows) ===")
display(df_low_stock)

# Close connection
cursor.close()
conn.close()
print("\nConnection closed.")

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# CELL ********************

# ─────────────────────────────────────────────
# Cell 8 – Cleanup: Remove seed data
# Deletes all rows inserted by Cell 2.
# Run after verifying the analytics queries.
# NOTE: Requires FABRIC_SERVER and FABRIC_DATABASE from Cell 1 to be set.
# ─────────────────────────────────────────────

# Re-open connection for cleanup (Cell 7 closes it)
token2        = mssparkutils.credentials.getToken("https://database.windows.net/")
token2_bytes  = token2.encode("UTF-16-LE")
token2_struct = struct.pack(f"<I{len(token2_bytes)}s", len(token2_bytes), token2_bytes)

conn2   = pyodbc.connect(
    f"Driver={{ODBC Driver 18 for SQL Server}};"
    f"Server={FABRIC_SERVER};"
    f"Database={FABRIC_DATABASE};",
    attrs_before={1256: token2_struct},
)
cursor2 = conn2.cursor()

cursor2.execute("DELETE FROM Sales.SalesOrderLine")
print(f"Deleted {cursor2.rowcount} sales order lines.")

cursor2.execute("DELETE FROM Sales.SalesOrder")
print(f"Deleted {cursor2.rowcount} sales orders.")

cursor2.execute("DELETE FROM Sales.Customer")
print(f"Deleted {cursor2.rowcount} customers.")

cursor2.execute("DELETE FROM Sales.Product")
print(f"Deleted {cursor2.rowcount} products.")

cursor2.execute("DELETE FROM Sales.ProductCategory")
print(f"Deleted {cursor2.rowcount} product categories.")

cursor2.execute("DELETE FROM Sales.Region")
print(f"Deleted {cursor2.rowcount} regions.")

conn2.commit()
cursor2.close()
conn2.close()
print("Seed data cleanup complete.")

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }
