# Workspace Items

This directory contains Microsoft Fabric workspace items managed through Git integration.
Each subfolder represents one Fabric item and must contain a `.platform` file plus its definition files.

---

## Directory Structure

```
workspace/
  FSI_DB_01.SQLDatabase/          # Fabric SQL Database (schema source of truth)
  Sales_Report.SemanticModel/     # Power BI Semantic Model (connects to SQL Database)
  Sales_Report.Report/            # Power BI Report (references the Semantic Model)
  Notebook_Sales.Notebook/        # Sample Fabric notebook
```

---

## Fabric SQL Database (`FSI_DB_01.SQLDatabase`)

The SQL Database defines the `SalesLT` schema with the following tables used by the semantic model:

| Table | Key columns |
|---|---|
| `SalesLT.Customer` | CustomerID (PK), FirstName, LastName, CompanyName, EmailAddress |
| `SalesLT.Product` | ProductID (PK), Name, ProductNumber, Color, ListPrice, ProductCategoryID |
| `SalesLT.ProductCategory` | ProductCategoryID (PK), ParentProductCategoryID, Name |
| `SalesLT.SalesOrderHeader` | SalesOrderID (PK), OrderDate, CustomerID (FK), SubTotal, TaxAmt, Freight |
| `SalesLT.SalesOrderDetail` | SalesOrderDetailID (PK), SalesOrderID (FK), ProductID (FK), OrderQty, UnitPrice |

**Does the SQL server need to be created manually?**
Yes. Before deploying the semantic model, create a Fabric SQL Database item named `FSI_DB_01`
in each Fabric workspace (DEV, QA, PROD). Then apply the SQL schema using the `.sqlproj`
in `FSI_DB_01.SQLDatabase/`.

---

## Semantic Model (`Sales_Report.SemanticModel`)

The semantic model (`model.bim`) connects to the Fabric SQL Database using Power Query M:

```m
let
    Source = Sql.Database("dev-sql-server.database.windows.net", "FSI_DB_01"),
    SalesLT_Customer = Source{[Schema="SalesLT",Item="Customer"]}[Data]
in
    SalesLT_Customer
```

The server name `dev-sql-server.database.windows.net` is a placeholder that is replaced
per-environment by the `find_replace` rules in `config/parameter.yml`. The replacement
applies to **all occurrences** in `model.bim` — both the `dataSources` connection details
and the `Sql.Database()` M expressions in each partition.

### How the SQL Server Endpoint is Configured

1. Open `config/parameter.yml`.
2. Replace the placeholder server names with your actual Fabric SQL Database SQL Analytics
   Endpoint URLs. Find your endpoint in the Fabric portal:
   **Workspace → SQL Database item → Settings → Connection strings → Server**

```yaml
find_replace:
  DEV:
    "dev-sql-server.database.windows.net": "<your-dev-endpoint>.database.windows.net"
  QA:
    "dev-sql-server.database.windows.net": "<your-qa-endpoint>.database.windows.net"
  PROD:
    "dev-sql-server.database.windows.net": "<your-prod-endpoint>.database.windows.net"
```

3. When `deploy_workspace.py` runs, `fabric-cicd` applies these replacements to all
   definition files before publishing to the target workspace — including the `dataSources`
   connection details and the `Sql.Database()` M expressions in `model.bim`. The semantic
   model deployed to QA will automatically point to the QA SQL Database, and so on.

### After Deployment — Configure Credentials

After the semantic model is published to a Fabric workspace, you must configure
the SQL connection credentials in the Fabric portal:

1. Open the workspace → select the **Sales_Report** semantic model.
2. Go to **Settings → Data source credentials**.
3. Select the SQL data source entry and authenticate (OAuth2 / Service Principal).

---

## Power BI Report (`Sales_Report.Report`)

The report references the semantic model using a **relative path** in `definition.pbir`:

```json
{
  "version": "4.0",
  "datasetReference": {
    "byPath": {
      "path": "../Sales_Report.SemanticModel"
    },
    "byConnection": null
  }
}
```

`fabric-cicd` resolves this relative path at deploy time, so both items must be in the
same workspace. The `byPath` reference means **no hard-coded IDs** are needed — the report
automatically binds to the co-deployed semantic model.

### Report Pages

| Page | Visuals |
|---|---|
| **Sales Overview** | Title, KPI cards (# Orders, Total Revenue, # Customers, # Products), Revenue by Order Date column chart, Sales by Product table |

---

## Required `.platform` File

Every item folder must contain a `.platform` file describing the item type and display name:

```json
{
  "$schema": "https://developer.microsoft.com/json-schemas/fabric/gitIntegration/platformProperties/2.0.0/schema.json",
  "metadata": {
    "type": "SemanticModel",
    "displayName": "Sales_Report"
  },
  "config": {
    "version": "2.0",
    "logicalId": "<unique-guid>"
  }
}
```

Supported `type` values: `Notebook`, `SemanticModel`, `Report`, `Environment`, `SQLDatabase`, etc.

