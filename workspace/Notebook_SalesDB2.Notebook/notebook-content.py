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
# Cell 1 – Connect to Sales_DB_02 using AAD token
# ─────────────────────────────────────────────
import os
import struct

import pandas as pd
import pyodbc
from IPython.display import display
from notebookutils import mssparkutils

# Fabric SQL endpoint — these must be set to match your Fabric workspace.
# Note: FABRIC_SQL_SERVER has no usable default; set it as an environment variable.
FABRIC_SERVER   = os.environ["FABRIC_SQL_SERVER"]
FABRIC_DATABASE = os.environ.get("FABRIC_SQL_DATABASE", "Sales_DB_02")

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
# Cell 2 – Top 10 Customers by Total Revenue
# ─────────────────────────────────────────────
sql_top_customers = """
SELECT TOP 10
    c.CustomerID,
    c.FirstName + ' ' + c.LastName  AS CustomerName,
    c.CompanyName,
    COUNT(DISTINCT so.SalesOrderID)  AS TotalOrders,
    ROUND(SUM(so.SubTotal), 2)       AS TotalRevenue
FROM dbo.Customer       c
JOIN dbo.SalesOrder     so ON c.CustomerID = so.CustomerID
GROUP BY c.CustomerID, c.FirstName, c.LastName, c.CompanyName
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
# Cell 3 – Monthly Sales Trend
# ─────────────────────────────────────────────
sql_monthly_sales = """
SELECT
    YEAR(OrderDate)            AS OrderYear,
    MONTH(OrderDate)           AS OrderMonth,
    COUNT(*)                   AS TotalOrders,
    ROUND(SUM(SubTotal), 2)    AS SubTotal,
    ROUND(SUM(TaxAmt),   2)    AS TaxAmount,
    ROUND(SUM(Freight),  2)    AS Freight,
    ROUND(SUM(SubTotal + TaxAmt + Freight), 2) AS TotalRevenue
FROM dbo.SalesOrder
GROUP BY YEAR(OrderDate), MONTH(OrderDate)
ORDER BY OrderYear, OrderMonth;
"""

df_monthly = pd.read_sql(sql_monthly_sales, conn)
print("=== Monthly Sales Trend ===")
display(df_monthly)

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# CELL ********************

# ─────────────────────────────────────────────
# Cell 4 – Revenue by Product Category
# ─────────────────────────────────────────────
sql_category_revenue = """
SELECT
    p.Category,
    COUNT(DISTINCT soi.SalesOrderID)   AS TotalOrders,
    SUM(soi.OrderQty)                  AS UnitsSold,
    ROUND(SUM(soi.OrderQty * soi.UnitPrice * (1 - soi.UnitPriceDiscount)), 2) AS CategoryRevenue
FROM dbo.Product         p
JOIN dbo.SalesOrderItem  soi ON p.ProductID = soi.ProductID
GROUP BY p.Category
ORDER BY CategoryRevenue DESC;
"""

df_categories = pd.read_sql(sql_category_revenue, conn)
print("=== Revenue by Product Category ===")
display(df_categories)

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# CELL ********************

# ─────────────────────────────────────────────
# Cell 5 – Top 10 Best-Selling Products
# ─────────────────────────────────────────────
sql_best_sellers = """
SELECT TOP 10
    p.ProductID,
    p.Name                          AS ProductName,
    p.SKU,
    p.Category,
    p.UnitPrice,
    SUM(soi.OrderQty)               AS TotalUnitsSold,
    ROUND(SUM(soi.OrderQty * soi.UnitPrice * (1 - soi.UnitPriceDiscount)), 2) AS TotalRevenue
FROM dbo.Product         p
JOIN dbo.SalesOrderItem  soi ON p.ProductID = soi.ProductID
GROUP BY p.ProductID, p.Name, p.SKU, p.Category, p.UnitPrice
ORDER BY TotalUnitsSold DESC;
"""

df_best_sellers = pd.read_sql(sql_best_sellers, conn)
print("=== Top 10 Best-Selling Products ===")
display(df_best_sellers)

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# CELL ********************

# ─────────────────────────────────────────────
# Cell 6 – Sales Rep Performance
# ─────────────────────────────────────────────
sql_rep_performance = """
SELECT
    sr.SalesRepID,
    sr.FirstName + ' ' + sr.LastName   AS SalesRepName,
    r.Name                             AS Region,
    COUNT(DISTINCT so.SalesOrderID)    AS TotalOrders,
    COUNT(DISTINCT so.CustomerID)      AS UniqueCustomers,
    ROUND(SUM(so.SubTotal), 2)         AS TotalRevenue
FROM dbo.SalesRep    sr
JOIN dbo.Region      r  ON sr.RegionID   = r.RegionID
JOIN dbo.SalesOrder  so ON sr.SalesRepID = so.SalesRepID
GROUP BY sr.SalesRepID, sr.FirstName, sr.LastName, r.Name
ORDER BY TotalRevenue DESC;
"""

df_reps = pd.read_sql(sql_rep_performance, conn)
print("=== Sales Rep Performance ===")
display(df_reps)

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# CELL ********************

# ─────────────────────────────────────────────
# Cell 7 – Revenue by Region
# ─────────────────────────────────────────────
sql_region_revenue = """
SELECT
    r.RegionID,
    r.Name                             AS RegionName,
    r.CountryCode,
    COUNT(DISTINCT so.SalesOrderID)    AS TotalOrders,
    COUNT(DISTINCT so.CustomerID)      AS UniqueCustomers,
    ROUND(SUM(so.SubTotal), 2)         AS TotalRevenue
FROM dbo.Region      r
JOIN dbo.Customer    c  ON r.RegionID = c.RegionID
JOIN dbo.SalesOrder  so ON c.CustomerID = so.CustomerID
GROUP BY r.RegionID, r.Name, r.CountryCode
ORDER BY TotalRevenue DESC;
"""

df_regions = pd.read_sql(sql_region_revenue, conn)
print("=== Revenue by Region ===")
display(df_regions)

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# CELL ********************

# ─────────────────────────────────────────────
# Cell 8 – INSERT: Add a demo customer
# ─────────────────────────────────────────────
sql_insert_customer = """
INSERT INTO dbo.Customer (FirstName, LastName, CompanyName, Email, Phone, RegionID)
VALUES ('Jane', 'Demo', 'Contoso Ltd', 'jane.demo@contoso.com', '425-555-0199', 1);
"""

cursor.execute(sql_insert_customer)
conn.commit()

cursor.execute(
    "SELECT CustomerID, FirstName, LastName, CompanyName, Email "
    "FROM dbo.Customer WHERE Email = 'jane.demo@contoso.com'"
)
row = cursor.fetchone()
print("=== Inserted Customer ===")
print(f"CustomerID={row.CustomerID}  Name={row.FirstName} {row.LastName}  Company={row.CompanyName}")
demo_customer_id = row.CustomerID

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# CELL ********************

# ─────────────────────────────────────────────
# Cell 9 – UPDATE: Change the demo customer's phone
# ─────────────────────────────────────────────
cursor.execute(
    "UPDATE dbo.Customer SET Phone = '206-555-0101', ModifiedDate = GETDATE() WHERE CustomerID = ?;",
    demo_customer_id,
)
conn.commit()
print(f"Updated CustomerID {demo_customer_id} – Phone changed to 206-555-0101")

cursor.execute("SELECT CustomerID, Phone FROM dbo.Customer WHERE CustomerID = ?", demo_customer_id)
row = cursor.fetchone()
print(f"Verified Phone: {row.Phone}")

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# CELL ********************

# ─────────────────────────────────────────────
# Cell 10 – DELETE: Remove the demo customer
# ─────────────────────────────────────────────
cursor.execute("DELETE FROM dbo.Customer WHERE CustomerID = ?;", demo_customer_id)
conn.commit()
print(f"Deleted demo CustomerID {demo_customer_id} – cleanup complete")

cursor.execute("SELECT COUNT(*) FROM dbo.Customer WHERE CustomerID = ?", demo_customer_id)
count = cursor.fetchone()[0]
print(f"Rows remaining for CustomerID {demo_customer_id}: {count}")

# Close connection
cursor.close()
conn.close()
print("\nConnection closed.")

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }
