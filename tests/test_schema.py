"""
tests/test_schema.py — Unit tests for the FSI_DB_02 Sales database schema.

Validates that all expected SQL object definition files exist, follow
consistent naming conventions, and contain the correct DDL keywords.

Run with:
    python -m pytest tests/test_schema.py -v
or:
    python tests/test_schema.py
"""

from __future__ import annotations

import unittest
from pathlib import Path

# Repository root is one level above the tests/ directory
REPO_ROOT = Path(__file__).resolve().parent.parent
DB_ROOT = REPO_ROOT / "workspace" / "FSI_DB_02.SQLDatabase"
DATA_DIR = REPO_ROOT / "data"


class TestFSIDB02Structure(unittest.TestCase):
    """Verify the FSI_DB_02.SQLDatabase folder structure."""

    def test_platform_file_exists(self):
        platform = DB_ROOT / ".platform"
        self.assertTrue(platform.is_file(), f".platform not found at {platform}")

    def test_sqlproj_file_exists(self):
        sqlproj = DB_ROOT / "FSI_DB_02.sqlproj"
        self.assertTrue(sqlproj.is_file(), f"FSI_DB_02.sqlproj not found at {sqlproj}")

    def test_schema_security_file_exists(self):
        schema_file = DB_ROOT / "Security" / "Sales.sql"
        self.assertTrue(schema_file.is_file(), f"Security/Sales.sql not found at {schema_file}")

    def test_sequence_file_exists(self):
        seq_file = DB_ROOT / "Sales" / "Sequences" / "OrderNumber.sql"
        self.assertTrue(seq_file.is_file(), f"Sequences/OrderNumber.sql not found at {seq_file}")


class TestFSIDB02Tables(unittest.TestCase):
    """Verify all expected Sales schema table files exist and contain valid DDL."""

    EXPECTED_TABLES = [
        "Region",
        "Customer",
        "ProductCategory",
        "Product",
        "SalesOrder",
        "SalesOrderLine",
    ]

    def _table_path(self, name: str) -> Path:
        return DB_ROOT / "Sales" / "Tables" / f"{name}.sql"

    def test_all_table_files_exist(self):
        for table in self.EXPECTED_TABLES:
            with self.subTest(table=table):
                path = self._table_path(table)
                self.assertTrue(path.is_file(), f"Table file not found: {path}")

    def test_table_files_contain_create_table(self):
        for table in self.EXPECTED_TABLES:
            with self.subTest(table=table):
                path = self._table_path(table)
                content = path.read_text(encoding="utf-8").upper()
                self.assertIn("CREATE TABLE", content, f"CREATE TABLE missing in {path.name}")

    def test_table_files_contain_primary_key(self):
        for table in self.EXPECTED_TABLES:
            with self.subTest(table=table):
                path = self._table_path(table)
                content = path.read_text(encoding="utf-8").upper()
                self.assertIn("PRIMARY KEY", content, f"PRIMARY KEY missing in {path.name}")

    def test_region_has_unique_region_code(self):
        path = self._table_path("Region")
        content = path.read_text(encoding="utf-8").upper()
        self.assertIn("REGIONCODE", content, "RegionCode column missing in Region.sql")
        self.assertIn("UNIQUE", content, "UNIQUE constraint missing in Region.sql")

    def test_customer_has_region_foreign_key(self):
        path = self._table_path("Customer")
        content = path.read_text(encoding="utf-8").upper()
        self.assertIn("REGIONID", content, "RegionID column missing in Customer.sql")
        self.assertIn("FOREIGN KEY", content, "FOREIGN KEY missing in Customer.sql")

    def test_product_has_category_foreign_key(self):
        path = self._table_path("Product")
        content = path.read_text(encoding="utf-8").upper()
        self.assertIn("PRODUCTCATEGORYID", content, "ProductCategoryID missing in Product.sql")
        self.assertIn("FOREIGN KEY", content, "FOREIGN KEY missing in Product.sql")

    def test_product_has_list_price_check_constraint(self):
        path = self._table_path("Product")
        content = path.read_text(encoding="utf-8").upper()
        self.assertIn("CK_PRODUCT_LISTPRICE", content, "ListPrice CHECK constraint missing in Product.sql")

    def test_sales_order_has_customer_foreign_key(self):
        path = self._table_path("SalesOrder")
        content = path.read_text(encoding="utf-8").upper()
        self.assertIn("CUSTOMERID", content, "CustomerID column missing in SalesOrder.sql")
        self.assertIn("FOREIGN KEY", content, "FOREIGN KEY missing in SalesOrder.sql")

    def test_sales_order_has_due_date_check(self):
        path = self._table_path("SalesOrder")
        content = path.read_text(encoding="utf-8").upper()
        self.assertIn("DUEDATE", content, "DueDate column missing in SalesOrder.sql")
        self.assertIn("CHECK", content, "CHECK constraint missing in SalesOrder.sql")

    def test_sales_order_line_cascades_on_delete(self):
        path = self._table_path("SalesOrderLine")
        content = path.read_text(encoding="utf-8").upper()
        self.assertIn("ON DELETE CASCADE", content, "ON DELETE CASCADE missing in SalesOrderLine.sql")

    def test_tables_use_rowguid(self):
        """Every table should have a rowguid uniqueidentifier column."""
        for table in self.EXPECTED_TABLES:
            with self.subTest(table=table):
                path = self._table_path(table)
                content = path.read_text(encoding="utf-8").upper()
                self.assertIn("ROWGUID", content, f"rowguid missing in {path.name}")

    def test_tables_use_modified_date(self):
        """Every table should have a ModifiedDate column."""
        for table in self.EXPECTED_TABLES:
            with self.subTest(table=table):
                path = self._table_path(table)
                content = path.read_text(encoding="utf-8").upper()
                self.assertIn("MODIFIEDDATE", content, f"ModifiedDate missing in {path.name}")

    def test_no_redundant_indexes_on_unique_columns(self):
        """
        Unique constraints already create indexes — do not add a separate
        non-clustered index on the same column (per repo convention).
        """
        for table in self.EXPECTED_TABLES:
            with self.subTest(table=table):
                path = self._table_path(table)
                content = path.read_text(encoding="utf-8")
                upper = content.upper()
                # rowguid always has a unique constraint; there must be no
                # separate CREATE NONCLUSTERED INDEX … ON …([rowguid])
                if "AK_" in upper and "ROWGUID" in upper:
                    self.assertNotIn(
                        "IX_" + table.upper() + "_ROWGUID",
                        upper,
                        f"Redundant index on rowguid detected in {path.name}",
                    )


class TestFSIDB02Views(unittest.TestCase):
    """Verify view files exist and contain correct DDL."""

    EXPECTED_VIEWS = ["vTopCustomers", "vSalesByCategory"]

    def _view_path(self, name: str) -> Path:
        return DB_ROOT / "Sales" / "Views" / f"{name}.sql"

    def test_all_view_files_exist(self):
        for view in self.EXPECTED_VIEWS:
            with self.subTest(view=view):
                path = self._view_path(view)
                self.assertTrue(path.is_file(), f"View file not found: {path}")

    def test_view_files_contain_create_view(self):
        for view in self.EXPECTED_VIEWS:
            with self.subTest(view=view):
                path = self._view_path(view)
                content = path.read_text(encoding="utf-8").upper()
                self.assertIn("CREATE VIEW", content, f"CREATE VIEW missing in {path.name}")

    def test_views_use_schemabinding(self):
        for view in self.EXPECTED_VIEWS:
            with self.subTest(view=view):
                path = self._view_path(view)
                content = path.read_text(encoding="utf-8").upper()
                self.assertIn("WITH SCHEMABINDING", content, f"SCHEMABINDING missing in {path.name}")

    def test_v_top_customers_references_sales_order(self):
        path = self._view_path("vTopCustomers")
        content = path.read_text(encoding="utf-8").upper()
        self.assertIn("SALES].[SALESORDER]", content, "vTopCustomers must reference Sales.SalesOrder")

    def test_v_sales_by_category_references_sales_order_line(self):
        path = self._view_path("vSalesByCategory")
        content = path.read_text(encoding="utf-8").upper()
        self.assertIn("SALES].[SALESORDERLINE]", content, "vSalesByCategory must reference Sales.SalesOrderLine")


class TestSampleData(unittest.TestCase):
    """Verify sample CSV data files exist and contain expected columns."""

    def _csv_headers(self, filename: str) -> list[str]:
        import csv
        with open(DATA_DIR / filename, newline="", encoding="utf-8") as fh:
            reader = csv.DictReader(fh)
            return reader.fieldnames or []

    def test_region_csv_exists(self):
        self.assertTrue((DATA_DIR / "Region.csv").is_file())

    def test_region_csv_columns(self):
        headers = self._csv_headers("Region.csv")
        self.assertIn("RegionCode", headers)
        self.assertIn("RegionName", headers)
        self.assertIn("Country", headers)

    def test_region_csv_has_data(self):
        import csv
        with open(DATA_DIR / "Region.csv", newline="", encoding="utf-8") as fh:
            rows = list(csv.DictReader(fh))
        self.assertGreater(len(rows), 0, "Region.csv must have at least one data row")

    def test_product_category_csv_exists(self):
        self.assertTrue((DATA_DIR / "ProductCategory.csv").is_file())

    def test_product_category_csv_columns(self):
        headers = self._csv_headers("ProductCategory.csv")
        self.assertIn("Name", headers)

    def test_product_csv_exists(self):
        self.assertTrue((DATA_DIR / "Product.csv").is_file())

    def test_product_csv_columns(self):
        headers = self._csv_headers("Product.csv")
        for col in ("ProductNumber", "Name", "CategoryName", "StandardCost", "ListPrice", "StockQty"):
            self.assertIn(col, headers, f"Column {col!r} missing from Product.csv")

    def test_product_csv_prices_are_positive(self):
        import csv
        with open(DATA_DIR / "Product.csv", newline="", encoding="utf-8") as fh:
            for row in csv.DictReader(fh):
                with self.subTest(product=row["ProductNumber"]):
                    self.assertGreaterEqual(float(row["ListPrice"]), 0, "ListPrice must be >= 0")
                    self.assertGreaterEqual(float(row["StandardCost"]), 0, "StandardCost must be >= 0")

    def test_customer_csv_exists(self):
        self.assertTrue((DATA_DIR / "Customer.csv").is_file())

    def test_customer_csv_columns(self):
        headers = self._csv_headers("Customer.csv")
        for col in ("FirstName", "LastName", "EmailAddress", "RegionCode"):
            self.assertIn(col, headers, f"Column {col!r} missing from Customer.csv")

    def test_customer_csv_email_addresses_unique(self):
        import csv
        with open(DATA_DIR / "Customer.csv", newline="", encoding="utf-8") as fh:
            emails = [row["EmailAddress"] for row in csv.DictReader(fh) if row["EmailAddress"]]
        self.assertEqual(len(emails), len(set(emails)), "Customer email addresses must be unique")

    def test_customer_region_codes_exist_in_region_csv(self):
        import csv
        with open(DATA_DIR / "Region.csv", newline="", encoding="utf-8") as fh:
            region_codes = {row["RegionCode"] for row in csv.DictReader(fh)}
        with open(DATA_DIR / "Customer.csv", newline="", encoding="utf-8") as fh:
            for row in csv.DictReader(fh):
                if row["RegionCode"]:
                    self.assertIn(
                        row["RegionCode"],
                        region_codes,
                        f"Customer {row['EmailAddress']} references unknown RegionCode {row['RegionCode']!r}",
                    )


class TestNotebookV2(unittest.TestCase):
    """Verify the Notebook_Sales_v2.Notebook folder and content."""

    NB_ROOT = REPO_ROOT / "workspace" / "Notebook_Sales_v2.Notebook"

    def test_platform_file_exists(self):
        self.assertTrue((self.NB_ROOT / ".platform").is_file())

    def test_notebook_content_exists(self):
        self.assertTrue((self.NB_ROOT / "notebook-content.py").is_file())

    def test_platform_type_is_notebook(self):
        import json
        with open(self.NB_ROOT / ".platform", encoding="utf-8") as fh:
            data = json.load(fh)
        self.assertEqual(data["metadata"]["type"], "Notebook")

    def test_notebook_connects_to_fsi_db_02(self):
        content = (self.NB_ROOT / "notebook-content.py").read_text(encoding="utf-8")
        self.assertIn("FSI_DB_02", content, "Notebook must reference FSI_DB_02")

    def test_notebook_contains_cleanup_cell(self):
        content = (self.NB_ROOT / "notebook-content.py").read_text(encoding="utf-8")
        self.assertIn("cleanup", content.lower(), "Notebook should contain a cleanup cell")


if __name__ == "__main__":
    unittest.main(verbosity=2)
