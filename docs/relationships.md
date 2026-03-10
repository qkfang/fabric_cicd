# FSI_DB_02 — Sales Schema: Table Relationships

This document describes the database schema for **FSI_DB_02**, the v2 Sales
database deployed to Microsoft Fabric.  It covers every table in the `Sales`
schema, lists all columns, and maps the primary-key / foreign-key relationships.

---

## Entity-Relationship Overview

```
Region ──────────────────────────────────────────────┐
  PK: RegionID                                        │
                                                      │ FK: RegionID
Customer ───────────────────────────────────────────>─┘
  PK: CustomerID
      │
      │ FK: CustomerID
      ▼
  SalesOrder
  PK: SalesOrderID
      │
      │ FK: SalesOrderID (CASCADE DELETE)
      ▼
  SalesOrderLine ──────────────────────────────────>─┐
  PK: SalesOrderID + SalesOrderLineID                │ FK: ProductID
                                                      │
ProductCategory ──────────────────────────────────┐  │
  PK: ProductCategoryID                            │  │
  FK: ParentProductCategoryID → self               │  │
                                                   │  │
Product ──────────────────────────────────────>───┘  │
  PK: ProductID                                       │
  FK: ProductCategoryID → ProductCategory.ProductCategoryID
  <────────────────────────────────────────────────────┘
```

---

## Tables

### `Sales.Region`

Lookup table for geographic sales regions.

| Column        | Type              | Nullable | Notes                          |
|---------------|-------------------|----------|--------------------------------|
| RegionID      | INT IDENTITY      | NOT NULL | **Primary Key**                |
| RegionCode    | NVARCHAR(10)      | NOT NULL | Unique — e.g. `NA-NW`         |
| RegionName    | NVARCHAR(100)     | NOT NULL | Human-readable label           |
| Country       | NVARCHAR(60)      | NOT NULL |                                |
| rowguid       | UNIQUEIDENTIFIER  | NOT NULL | Unique; default `newid()`      |
| ModifiedDate  | DATETIME          | NOT NULL | Default `getdate()`            |

**Constraints**
- `PK_Region_RegionID` — primary key on `RegionID`
- `AK_Region_RegionCode` — unique non-clustered index on `RegionCode`
- `AK_Region_rowguid` — unique non-clustered index on `rowguid`

---

### `Sales.Customer`

Stores customer master data including a link to their sales region.

| Column        | Type              | Nullable | Notes                          |
|---------------|-------------------|----------|--------------------------------|
| CustomerID    | INT IDENTITY      | NOT NULL | **Primary Key**                |
| FirstName     | NVARCHAR(50)      | NOT NULL |                                |
| LastName      | NVARCHAR(50)      | NOT NULL |                                |
| CompanyName   | NVARCHAR(128)     | NULL     |                                |
| EmailAddress  | NVARCHAR(100)     | NULL     | Indexed                        |
| Phone         | NVARCHAR(25)      | NULL     |                                |
| RegionID      | INT               | NULL     | **FK → Region.RegionID**       |
| rowguid       | UNIQUEIDENTIFIER  | NOT NULL | Unique; default `newid()`      |
| ModifiedDate  | DATETIME          | NOT NULL | Default `getdate()`            |

**Constraints & Indexes**
- `PK_Customer_CustomerID` — primary key
- `FK_Customer_Region_RegionID` → `Sales.Region(RegionID)`
- `AK_Customer_rowguid` — unique non-clustered
- `IX_Customer_EmailAddress` — non-clustered index
- `IX_Customer_RegionID` — non-clustered index

---

### `Sales.ProductCategory`

Hierarchical product category tree (self-referencing).

| Column                  | Type              | Nullable | Notes                                |
|-------------------------|-------------------|----------|--------------------------------------|
| ProductCategoryID       | INT IDENTITY      | NOT NULL | **Primary Key**                      |
| ParentProductCategoryID | INT               | NULL     | **FK → ProductCategory (self-join)** |
| Name                    | NVARCHAR(50)      | NOT NULL | Unique                               |
| rowguid                 | UNIQUEIDENTIFIER  | NOT NULL | Unique; default `newid()`            |
| ModifiedDate            | DATETIME          | NOT NULL | Default `getdate()`                  |

**Constraints**
- `PK_ProductCategory_ProductCategoryID` — primary key
- `FK_ProductCategory_ProductCategory_Parent` → self on `ParentProductCategoryID`
- `AK_ProductCategory_Name` — unique non-clustered
- `AK_ProductCategory_rowguid` — unique non-clustered

---

### `Sales.Product`

Product catalogue with pricing, stock quantity, and category link.

| Column             | Type              | Nullable | Notes                                   |
|--------------------|-------------------|----------|-----------------------------------------|
| ProductID          | INT IDENTITY      | NOT NULL | **Primary Key**                         |
| ProductNumber      | NVARCHAR(25)      | NOT NULL | Unique business key                     |
| Name               | NVARCHAR(100)     | NOT NULL |                                         |
| ProductCategoryID  | INT               | NULL     | **FK → ProductCategory.ProductCategoryID** |
| Color              | NVARCHAR(15)      | NULL     |                                         |
| Size               | NVARCHAR(5)       | NULL     |                                         |
| StandardCost       | MONEY             | NOT NULL | CHECK ≥ 0; default 0.00                 |
| ListPrice          | MONEY             | NOT NULL | CHECK ≥ 0; default 0.00                 |
| StockQty           | INT               | NOT NULL | CHECK ≥ 0; default 0                   |
| rowguid            | UNIQUEIDENTIFIER  | NOT NULL | Unique; default `newid()`               |
| ModifiedDate       | DATETIME          | NOT NULL | Default `getdate()`                     |

**Constraints**
- `PK_Product_ProductID` — primary key
- `FK_Product_ProductCategory_ProductCategoryID` → `Sales.ProductCategory`
- `AK_Product_ProductNumber` — unique non-clustered on `ProductNumber`
- `AK_Product_rowguid` — unique non-clustered
- `CK_Product_ListPrice`, `CK_Product_StandardCost`, `CK_Product_StockQty` — range checks

---

### `Sales.SalesOrder`

Order header; one row per customer order.  `SalesOrderID` is generated from the
`Sales.OrderNumber` sequence.

| Column        | Type              | Nullable | Notes                                   |
|---------------|-------------------|----------|-----------------------------------------|
| SalesOrderID  | INT               | NOT NULL | **Primary Key**; default from sequence  |
| OrderDate     | DATETIME          | NOT NULL | Default `getdate()`                     |
| DueDate       | DATETIME          | NOT NULL | CHECK ≥ `OrderDate`                     |
| ShipDate      | DATETIME          | NULL     | CHECK ≥ `OrderDate` OR NULL             |
| Status        | TINYINT           | NOT NULL | CHECK 0–8; default 1                    |
| CustomerID    | INT               | NOT NULL | **FK → Customer.CustomerID**            |
| ShipMethod    | NVARCHAR(50)      | NOT NULL |                                         |
| SubTotal      | MONEY             | NOT NULL | CHECK ≥ 0; default 0.00                 |
| TaxAmt        | MONEY             | NOT NULL | CHECK ≥ 0; default 0.00                 |
| Freight       | MONEY             | NOT NULL | CHECK ≥ 0; default 0.00                 |
| Comment       | NVARCHAR(MAX)     | NULL     |                                         |
| rowguid       | UNIQUEIDENTIFIER  | NOT NULL | Unique; default `newid()`               |
| ModifiedDate  | DATETIME          | NOT NULL | Default `getdate()`                     |

**Constraints & Indexes**
- `PK_SalesOrder_SalesOrderID` — primary key
- `FK_SalesOrder_Customer_CustomerID` → `Sales.Customer(CustomerID)`
- `AK_SalesOrder_rowguid` — unique non-clustered
- `IX_SalesOrder_CustomerID` — non-clustered index
- `CK_SalesOrder_DueDate`, `CK_SalesOrder_ShipDate`, `CK_SalesOrder_Status`,
  `CK_SalesOrder_SubTotal`, `CK_SalesOrder_TaxAmt`, `CK_SalesOrder_Freight`

---

### `Sales.SalesOrderLine`

Order line items; child of `SalesOrder` with a cascade-delete relationship.

| Column             | Type              | Nullable | Notes                                    |
|--------------------|-------------------|----------|------------------------------------------|
| SalesOrderID       | INT               | NOT NULL | **PK (part 1)**; FK → SalesOrder         |
| SalesOrderLineID   | INT IDENTITY      | NOT NULL | **PK (part 2)**                          |
| ProductID          | INT               | NOT NULL | **FK → Product.ProductID**               |
| OrderQty           | SMALLINT          | NOT NULL | CHECK > 0; default 1                     |
| UnitPrice          | MONEY             | NOT NULL | CHECK ≥ 0                                |
| UnitPriceDiscount  | MONEY             | NOT NULL | CHECK ≥ 0; default 0.00                  |
| rowguid            | UNIQUEIDENTIFIER  | NOT NULL | Unique; default `newid()`                |
| ModifiedDate       | DATETIME          | NOT NULL | Default `getdate()`                      |

**Constraints & Indexes**
- `PK_SalesOrderLine_SalesOrderID_SalesOrderLineID` — composite primary key
- `FK_SalesOrderLine_SalesOrder_SalesOrderID` → `Sales.SalesOrder(SalesOrderID)` **ON DELETE CASCADE**
- `FK_SalesOrderLine_Product_ProductID` → `Sales.Product(ProductID)`
- `AK_SalesOrderLine_rowguid` — unique non-clustered
- `IX_SalesOrderLine_ProductID` — non-clustered index
- `CK_SalesOrderLine_OrderQty`, `CK_SalesOrderLine_UnitPrice`, `CK_SalesOrderLine_UnitPriceDiscount`

---

## Views

### `Sales.vTopCustomers`

Aggregates total orders and revenue per customer, joined to region.
Useful for top-N customer reports.

**Columns:** `CustomerID`, `CustomerName`, `CompanyName`, `RegionName`,
`TotalOrders`, `TotalRevenue`

**Base tables:** `Sales.Customer`, `Sales.SalesOrder`, `Sales.Region`

---

### `Sales.vSalesByCategory`

Aggregates units sold and net revenue (after discount) per product category.

**Columns:** `Category`, `TotalOrders`, `UnitsSold`, `NetRevenue`

**Base tables:** `Sales.ProductCategory`, `Sales.Product`, `Sales.SalesOrderLine`

---

## Sequence

### `Sales.OrderNumber`

Integer sequence (start 1, increment 1) that seeds the default value for
`Sales.SalesOrder.SalesOrderID`.

---

## Relationship Summary

| Child Table        | Child Column           | Parent Table            | Parent Column       | On Delete |
|--------------------|------------------------|-------------------------|---------------------|-----------|
| Customer           | RegionID               | Region                  | RegionID            | —         |
| ProductCategory    | ParentProductCategoryID| ProductCategory (self)  | ProductCategoryID   | —         |
| Product            | ProductCategoryID      | ProductCategory         | ProductCategoryID   | —         |
| SalesOrder         | CustomerID             | Customer                | CustomerID          | —         |
| SalesOrderLine     | SalesOrderID           | SalesOrder              | SalesOrderID        | CASCADE   |
| SalesOrderLine     | ProductID              | Product                 | ProductID           | —         |
