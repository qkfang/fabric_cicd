# Test Suite — `tests/test_validate_repo.py`

30 pytest unit tests across 5 classes covering the `validate_repo.py` deployment helper and the structural integrity of the `Sales_DB_02` database artefacts and the `Notebook_SalesDB2` notebook.

---

## Quick start

```bash
# Install dependencies (once)
pip install -r requirements.txt

# Run the full suite
pytest tests/ -v

# Run a single class
pytest tests/test_validate_repo.py::TestSalesDB02Structure -v

# Run a single test
pytest tests/test_validate_repo.py::TestCheckWorkspaceDir::test_returns_false_when_workspace_missing -v
```

Expected output (all passing):

```
tests/test_validate_repo.py::TestCheckWorkspaceDir::test_returns_true_when_workspace_exists       PASSED
tests/test_validate_repo.py::TestCheckWorkspaceDir::test_returns_false_when_workspace_missing     PASSED
tests/test_validate_repo.py::TestCheckWorkspaceDir::test_returns_true_for_empty_workspace         PASSED
tests/test_validate_repo.py::TestCheckWorkspaceDir::test_counts_items_in_workspace                PASSED
tests/test_validate_repo.py::TestCheckParameterYml::test_returns_false_when_file_missing          PASSED
tests/test_validate_repo.py::TestCheckParameterYml::test_valid_parameter_yml                      PASSED
tests/test_validate_repo.py::TestCheckParameterYml::test_invalid_yaml_returns_false               PASSED
tests/test_validate_repo.py::TestCheckParameterYml::test_missing_environments_still_returns_true  PASSED
tests/test_validate_repo.py::TestCheckPlatformFiles::test_returns_true_when_all_items_have_platform PASSED
tests/test_validate_repo.py::TestCheckPlatformFiles::test_returns_true_even_when_platform_missing  PASSED
tests/test_validate_repo.py::TestCheckPlatformFiles::test_returns_true_for_empty_workspace         PASSED
tests/test_validate_repo.py::TestSalesDB02Structure::test_platform_file_exists                     PASSED
tests/test_validate_repo.py::TestSalesDB02Structure::test_sqlproj_exists                           PASSED
tests/test_validate_repo.py::TestSalesDB02Structure::test_relationships_md_exists                  PASSED
tests/test_validate_repo.py::TestSalesDB02Structure::test_seed_data_sql_exists                     PASSED
tests/test_validate_repo.py::TestSalesDB02Structure::test_table_sql_exists[Region]                 PASSED
tests/test_validate_repo.py::TestSalesDB02Structure::test_table_sql_exists[SalesRep]               PASSED
tests/test_validate_repo.py::TestSalesDB02Structure::test_table_sql_exists[Customer]               PASSED
tests/test_validate_repo.py::TestSalesDB02Structure::test_table_sql_exists[Product]                PASSED
tests/test_validate_repo.py::TestSalesDB02Structure::test_table_sql_exists[SalesOrder]             PASSED
tests/test_validate_repo.py::TestSalesDB02Structure::test_table_sql_exists[SalesOrderItem]         PASSED
tests/test_validate_repo.py::TestSalesDB02Structure::test_platform_file_contains_correct_type      PASSED
tests/test_validate_repo.py::TestSalesDB02Structure::test_sqlproj_references_fabric_dsp            PASSED
tests/test_validate_repo.py::TestSalesDB02Structure::test_seed_data_contains_all_tables            PASSED
tests/test_validate_repo.py::TestSalesDB02Structure::test_relationships_md_contains_all_tables     PASSED
tests/test_validate_repo.py::TestNotebookSalesDB2Structure::test_platform_file_exists              PASSED
tests/test_validate_repo.py::TestNotebookSalesDB2Structure::test_notebook_content_exists           PASSED
tests/test_validate_repo.py::TestNotebookSalesDB2Structure::test_platform_file_contains_correct_type PASSED
tests/test_validate_repo.py::TestNotebookSalesDB2Structure::test_notebook_content_references_sales_db_02 PASSED
tests/test_validate_repo.py::TestNotebookSalesDB2Structure::test_notebook_content_has_pyspark_kernel PASSED

30 passed in 0.08s
```

---

## Test classes

### Class 1 — `TestCheckWorkspaceDir` (4 tests)

Covers `deploy/validate_repo.py → check_workspace_dir(repo_root)`.

| # | Test | What it asserts |
|---|------|-----------------|
| 1 | `test_returns_true_when_workspace_exists` | Returns `True` when `workspace/` directory is present |
| 2 | `test_returns_false_when_workspace_missing` | Returns `False` when `workspace/` directory does not exist |
| 3 | `test_returns_true_for_empty_workspace` | Empty `workspace/` is a warning, not a failure — returns `True` |
| 4 | `test_counts_items_in_workspace` | Returns `True` when `workspace/` contains one or more item folders |

All four tests use pytest's `tmp_path` fixture so they never touch the real repository.

---

### Class 2 — `TestCheckParameterYml` (4 tests)

Covers `deploy/validate_repo.py → check_parameter_yml(repo_root)`.

| # | Test | What it asserts |
|---|------|-----------------|
| 5 | `test_returns_false_when_file_missing` | Returns `False` when `config/parameter.yml` is absent |
| 6 | `test_valid_parameter_yml` | Returns `True` for a well-formed YAML file with DEV / QA / PROD sections |
| 7 | `test_invalid_yaml_returns_false` | Returns `False` when the file contains unparseable YAML |
| 8 | `test_missing_environments_still_returns_true` | Missing environment keys are warnings, not errors — returns `True` |

---

### Class 3 — `TestCheckPlatformFiles` (3 tests)

Covers `deploy/validate_repo.py → check_platform_files(repo_root)`.

| # | Test | What it asserts |
|---|------|-----------------|
| 9  | `test_returns_true_when_all_items_have_platform` | Returns `True` when every item folder contains a `.platform` file |
| 10 | `test_returns_true_even_when_platform_missing` | Missing `.platform` is a warning, not a hard failure — returns `True` |
| 11 | `test_returns_true_for_empty_workspace` | Returns `True` for an empty `workspace/` (nothing to check) |

---

### Class 4 — `TestSalesDB02Structure` (13 tests)

Verifies the structural integrity of `workspace/Sales_DB_02.SQLDatabase/` directly in the repository checkout. These tests catch accidental deletion or renaming of database artefacts.

| # | Test | What it asserts |
|---|------|-----------------|
| 12 | `test_platform_file_exists` | `.platform` is present at the database root |
| 13 | `test_sqlproj_exists` | `Sales_DB_02.sqlproj` is present |
| 14 | `test_relationships_md_exists` | `RELATIONSHIPS.md` is present |
| 15 | `test_seed_data_sql_exists` | `dbo/SampleData/seed_data.sql` is present |
| 16 | `test_table_sql_exists[Region]` | `dbo/Tables/Region.sql` is present |
| 17 | `test_table_sql_exists[SalesRep]` | `dbo/Tables/SalesRep.sql` is present |
| 18 | `test_table_sql_exists[Customer]` | `dbo/Tables/Customer.sql` is present |
| 19 | `test_table_sql_exists[Product]` | `dbo/Tables/Product.sql` is present |
| 20 | `test_table_sql_exists[SalesOrder]` | `dbo/Tables/SalesOrder.sql` is present |
| 21 | `test_table_sql_exists[SalesOrderItem]` | `dbo/Tables/SalesOrderItem.sql` is present |
| 22 | `test_platform_file_contains_correct_type` | `.platform` JSON has `type = "SQLDatabase"` and `displayName = "Sales_DB_02"` |
| 23 | `test_sqlproj_references_fabric_dsp` | `.sqlproj` references the `SqlDbFabricDatabaseSchemaProvider` DSP |
| 24 | `test_seed_data_contains_all_tables` | `seed_data.sql` contains `INSERT` blocks for all 6 tables |
| 25 | `test_relationships_md_contains_all_tables` | `RELATIONSHIPS.md` mentions all 6 table names |

Tests 16–21 are generated with `@pytest.mark.parametrize` over the six table names, so adding a new table only requires updating the parameter list.

---

### Class 5 — `TestNotebookSalesDB2Structure` (5 tests)

Verifies the structural integrity of `workspace/Notebook_SalesDB2.Notebook/`.

| # | Test | What it asserts |
|---|------|-----------------|
| 26 | `test_platform_file_exists` | `.platform` is present in the notebook folder |
| 27 | `test_notebook_content_exists` | `notebook-content.py` is present |
| 28 | `test_platform_file_contains_correct_type` | `.platform` JSON has `type = "Notebook"` and `displayName = "Notebook_SalesDB2"` |
| 29 | `test_notebook_content_references_sales_db_02` | Notebook source references `"Sales_DB_02"` (database name) |
| 30 | `test_notebook_content_has_pyspark_kernel` | Notebook source specifies the `synapse_pyspark` kernel |

---

## Coverage summary

| Class | Target | Tests | Uses `tmp_path` |
|-------|--------|------:|:---:|
| `TestCheckWorkspaceDir` | `check_workspace_dir()` | 4 | ✅ |
| `TestCheckParameterYml` | `check_parameter_yml()` | 4 | ✅ |
| `TestCheckPlatformFiles` | `check_platform_files()` | 3 | ✅ |
| `TestSalesDB02Structure` | `Sales_DB_02.SQLDatabase/` artefacts | 13 | ❌ (real files) |
| `TestNotebookSalesDB2Structure` | `Notebook_SalesDB2.Notebook/` artefacts | 5 | ❌ (real files) |
| **Total** | | **30** | |

---

## Adding new tests

- **New `validate_repo` function** → add a new class `TestCheck<FunctionName>` following the same `tmp_path`-based pattern.
- **New workspace item** → add a new class `Test<ItemName>Structure` that pins `DB_DIR` / `NB_DIR` to the item folder and mirrors the checks in `TestSalesDB02Structure` or `TestNotebookSalesDB2Structure`.
- **New table in Sales_DB_02** → add the table name to the `@pytest.mark.parametrize` list in `TestSalesDB02Structure.test_table_sql_exists`.
