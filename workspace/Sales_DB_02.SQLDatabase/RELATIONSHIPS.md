# Sales_DB_02 — Table Relationships

This document describes the table structure and foreign-key relationships for the **Sales_DB_02** Fabric SQL database.

---

## Entity-Relationship Overview

```
Region
  │
  ├──< SalesRep (RegionID → Region.RegionID)
  │
  └──< Customer (RegionID → Region.RegionID)
           │
           └──< SalesOrder (CustomerID → Customer.CustomerID)
                    │
                    ├── SalesRep (SalesRepID → SalesRep.SalesRepID)
                    │
                    └──< SalesOrderItem (SalesOrderID → SalesOrder.SalesOrderID)
                               │
                               └── Product (ProductID → Product.ProductID)
```

---

## Tables

### `dbo.Region`

Lookup table of sales territories.

| Column        | Type          | Nullable | Description                    |
|---------------|---------------|----------|--------------------------------|
| RegionID      | INT (PK, AI)  | No       | Primary key                    |
| Name          | NVARCHAR(50)  | No       | Unique region name             |
| CountryCode   | NCHAR(2)      | No       | ISO 3166-1 alpha-2 code        |
| ModifiedDate  | DATETIME      | No       | Last modified timestamp        |

---

### `dbo.SalesRep`

Sales representatives assigned to a region.

| Column        | Type           | Nullable | Description                        |
|---------------|----------------|----------|------------------------------------|
| SalesRepID    | INT (PK, AI)   | No       | Primary key                        |
| FirstName     | NVARCHAR(50)   | No       | First name                         |
| LastName      | NVARCHAR(50)   | No       | Last name                          |
| Email         | NVARCHAR(100)  | No       | Unique email address               |
| RegionID      | INT (FK)       | No       | → `Region.RegionID`                |
| HireDate      | DATE           | No       | Date the rep joined                |
| IsActive      | BIT            | No       | `1` = active, `0` = inactive       |
| ModifiedDate  | DATETIME       | No       | Last modified timestamp            |

**Foreign keys**
- `FK_SalesRep_Region_RegionID` → `Region.RegionID`

---

### `dbo.Customer`

End customers who place sales orders.

| Column        | Type           | Nullable | Description                        |
|---------------|----------------|----------|------------------------------------|
| CustomerID    | INT (PK, AI)   | No       | Primary key                        |
| FirstName     | NVARCHAR(50)   | No       | First name                         |
| LastName      | NVARCHAR(50)   | No       | Last name                          |
| CompanyName   | NVARCHAR(128)  | Yes      | Employer / company                 |
| Email         | NVARCHAR(100)  | No       | Unique email address               |
| Phone         | NVARCHAR(25)   | Yes      | Contact phone number               |
| RegionID      | INT (FK)       | Yes      | → `Region.RegionID`                |
| ModifiedDate  | DATETIME       | No       | Last modified timestamp            |

**Foreign keys**
- `FK_Customer_Region_RegionID` → `Region.RegionID`

---

### `dbo.Product`

Product catalogue.

| Column        | Type           | Nullable | Description                        |
|---------------|----------------|----------|------------------------------------|
| ProductID     | INT (PK, AI)   | No       | Primary key                        |
| Name          | NVARCHAR(100)  | No       | Product name                       |
| SKU           | NVARCHAR(25)   | No       | Unique stock-keeping unit code     |
| Category      | NVARCHAR(50)   | Yes      | Product category label             |
| UnitPrice     | MONEY          | No       | Listed selling price (≥ 0)         |
| IsActive      | BIT            | No       | `1` = active in catalogue          |
| ModifiedDate  | DATETIME       | No       | Last modified timestamp            |

---

### `dbo.SalesOrder`

Order header — one row per customer order.

| Column        | Type           | Nullable | Description                               |
|---------------|----------------|----------|-------------------------------------------|
| SalesOrderID  | INT (PK, AI)   | No       | Primary key                               |
| CustomerID    | INT (FK)       | No       | → `Customer.CustomerID`                   |
| SalesRepID    | INT (FK)       | Yes      | → `SalesRep.SalesRepID` (nullable if direct) |
| OrderDate     | DATETIME       | No       | Date the order was placed                 |
| DueDate       | DATETIME       | No       | Promised delivery date (≥ OrderDate)      |
| ShipDate      | DATETIME       | Yes      | Actual ship date                          |
| Status        | TINYINT        | No       | 1=New 2=Processing … 5=Complete 8=Cancelled |
| SubTotal      | MONEY          | No       | Sum of line totals (≥ 0)                  |
| TaxAmt        | MONEY          | No       | Tax charged (≥ 0)                         |
| Freight       | MONEY          | No       | Shipping cost (≥ 0)                       |
| Comment       | NVARCHAR(MAX)  | Yes      | Free-text order notes                     |
| ModifiedDate  | DATETIME       | No       | Last modified timestamp                   |

**Computed total:** `SubTotal + TaxAmt + Freight`

**Foreign keys**
- `FK_SalesOrder_Customer_CustomerID` → `Customer.CustomerID`
- `FK_SalesOrder_SalesRep_SalesRepID` → `SalesRep.SalesRepID`

---

### `dbo.SalesOrderItem`

Order line items — one row per product per order.

| Column             | Type      | Nullable | Description                           |
|--------------------|-----------|----------|---------------------------------------|
| SalesOrderItemID   | INT (PK, AI) | No    | Primary key                           |
| SalesOrderID       | INT (FK)  | No       | → `SalesOrder.SalesOrderID` (cascade delete) |
| ProductID          | INT (FK)  | No       | → `Product.ProductID`                 |
| OrderQty           | SMALLINT  | No       | Quantity ordered (> 0)                |
| UnitPrice          | MONEY     | No       | Selling price at time of order (≥ 0)  |
| UnitPriceDiscount  | MONEY     | No       | Fractional discount (0.00–1.00)       |
| ModifiedDate       | DATETIME  | No       | Last modified timestamp               |

**Line total (computed):** `OrderQty × UnitPrice × (1 − UnitPriceDiscount)`

**Foreign keys**
- `FK_SalesOrderItem_SalesOrder_SalesOrderID` → `SalesOrder.SalesOrderID` (ON DELETE CASCADE)
- `FK_SalesOrderItem_Product_ProductID` → `Product.ProductID`

---

## Relationship Summary

| From table      | Column          | Relationship | To table        | Column        |
|-----------------|-----------------|--------------|-----------------|---------------|
| SalesRep        | RegionID        | Many → One   | Region          | RegionID      |
| Customer        | RegionID        | Many → One   | Region          | RegionID      |
| SalesOrder      | CustomerID      | Many → One   | Customer        | CustomerID    |
| SalesOrder      | SalesRepID      | Many → One   | SalesRep        | SalesRepID    |
| SalesOrderItem  | SalesOrderID    | Many → One   | SalesOrder      | SalesOrderID  |
| SalesOrderItem  | ProductID       | Many → One   | Product         | ProductID     |
