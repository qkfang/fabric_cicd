"""
tests/test_validate_repo.py
Unit tests for deploy/validate_repo.py and repository structure checks,
including validation of the new Sales_DB_02 database artefacts.
"""

from __future__ import annotations

import importlib.util
from pathlib import Path

import pytest

# ---------------------------------------------------------------------------
# Helpers — load validate_repo without running main()
# ---------------------------------------------------------------------------
REPO_ROOT = Path(__file__).parent.parent


def _load_validate_repo():
    spec = importlib.util.spec_from_file_location(
        "validate_repo", REPO_ROOT / "deploy" / "validate_repo.py"
    )
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


validate_repo = _load_validate_repo()


# ---------------------------------------------------------------------------
# check_workspace_dir
# ---------------------------------------------------------------------------


class TestCheckWorkspaceDir:
    def test_returns_true_when_workspace_exists(self, tmp_path):
        ws = tmp_path / "workspace"
        ws.mkdir()
        assert validate_repo.check_workspace_dir(tmp_path) is True

    def test_returns_false_when_workspace_missing(self, tmp_path):
        assert validate_repo.check_workspace_dir(tmp_path) is False

    def test_returns_true_for_empty_workspace(self, tmp_path):
        (tmp_path / "workspace").mkdir()
        # Empty workspace is a warning, not an error — should still return True
        assert validate_repo.check_workspace_dir(tmp_path) is True

    def test_counts_items_in_workspace(self, tmp_path):
        ws = tmp_path / "workspace"
        ws.mkdir()
        (ws / "ItemA.Notebook").mkdir()
        (ws / "ItemB.SQLDatabase").mkdir()
        assert validate_repo.check_workspace_dir(tmp_path) is True


# ---------------------------------------------------------------------------
# check_parameter_yml
# ---------------------------------------------------------------------------


class TestCheckParameterYml:
    def _write_param(self, path: Path, content: str) -> None:
        cfg = path / "config"
        cfg.mkdir(exist_ok=True)
        (cfg / "parameter.yml").write_text(content, encoding="utf-8")

    def test_returns_false_when_file_missing(self, tmp_path):
        assert validate_repo.check_parameter_yml(tmp_path) is False

    def test_valid_parameter_yml(self, tmp_path):
        self._write_param(
            tmp_path,
            "find_replace:\n  DEV: {}\n  QA: {}\n  PROD: {}\n",
        )
        assert validate_repo.check_parameter_yml(tmp_path) is True

    def test_invalid_yaml_returns_false(self, tmp_path):
        self._write_param(tmp_path, "find_replace: [\ninvalid yaml")
        assert validate_repo.check_parameter_yml(tmp_path) is False

    def test_missing_environments_still_returns_true(self, tmp_path):
        # Missing envs generate a warning but do not fail the check
        self._write_param(tmp_path, "find_replace:\n  DEV: {}\n")
        assert validate_repo.check_parameter_yml(tmp_path) is True


# ---------------------------------------------------------------------------
# check_platform_files
# ---------------------------------------------------------------------------


class TestCheckPlatformFiles:
    def test_returns_true_when_all_items_have_platform(self, tmp_path):
        ws = tmp_path / "workspace"
        ws.mkdir()
        item = ws / "MyNotebook.Notebook"
        item.mkdir()
        (item / ".platform").write_text("{}", encoding="utf-8")
        assert validate_repo.check_platform_files(tmp_path) is True

    def test_returns_true_even_when_platform_missing(self, tmp_path):
        # Missing .platform is a warning, not a hard failure
        ws = tmp_path / "workspace"
        ws.mkdir()
        (ws / "BrokenItem.Notebook").mkdir()
        assert validate_repo.check_platform_files(tmp_path) is True

    def test_returns_true_for_empty_workspace(self, tmp_path):
        (tmp_path / "workspace").mkdir()
        assert validate_repo.check_platform_files(tmp_path) is True


# ---------------------------------------------------------------------------
# Repository structure — Sales_DB_02
# ---------------------------------------------------------------------------


class TestSalesDB02Structure:
    """Verify the new Sales_DB_02 database artefacts are present and complete."""

    DB_DIR = REPO_ROOT / "workspace" / "Sales_DB_02.SQLDatabase"

    def test_platform_file_exists(self):
        assert (self.DB_DIR / ".platform").is_file()

    def test_sqlproj_exists(self):
        assert (self.DB_DIR / "Sales_DB_02.sqlproj").is_file()

    def test_relationships_md_exists(self):
        assert (self.DB_DIR / "RELATIONSHIPS.md").is_file()

    def test_seed_data_sql_exists(self):
        assert (self.DB_DIR / "dbo" / "SampleData" / "seed_data.sql").is_file()

    @pytest.mark.parametrize(
        "table",
        ["Region", "SalesRep", "Customer", "Product", "SalesOrder", "SalesOrderItem"],
    )
    def test_table_sql_exists(self, table):
        assert (self.DB_DIR / "dbo" / "Tables" / f"{table}.sql").is_file()

    def test_platform_file_contains_correct_type(self):
        import json

        content = json.loads((self.DB_DIR / ".platform").read_text(encoding="utf-8"))
        assert content["metadata"]["type"] == "SQLDatabase"
        assert content["metadata"]["displayName"] == "Sales_DB_02"

    def test_sqlproj_references_fabric_dsp(self):
        content = (self.DB_DIR / "Sales_DB_02.sqlproj").read_text(encoding="utf-8")
        assert "SqlDbFabricDatabaseSchemaProvider" in content

    def test_seed_data_contains_all_tables(self):
        content = (self.DB_DIR / "dbo" / "SampleData" / "seed_data.sql").read_text(
            encoding="utf-8"
        )
        for table in ("Region", "SalesRep", "Customer", "Product", "SalesOrder", "SalesOrderItem"):
            assert table in content, f"seed_data.sql is missing inserts for {table}"

    def test_relationships_md_contains_all_tables(self):
        content = (self.DB_DIR / "RELATIONSHIPS.md").read_text(encoding="utf-8")
        for table in ("Region", "SalesRep", "Customer", "Product", "SalesOrder", "SalesOrderItem"):
            assert table in content, f"RELATIONSHIPS.md does not mention {table}"


# ---------------------------------------------------------------------------
# Repository structure — Notebook_SalesDB2
# ---------------------------------------------------------------------------


class TestNotebookSalesDB2Structure:
    """Verify the new Notebook_SalesDB2 artefacts are present and complete."""

    NB_DIR = REPO_ROOT / "workspace" / "Notebook_SalesDB2.Notebook"

    def test_platform_file_exists(self):
        assert (self.NB_DIR / ".platform").is_file()

    def test_notebook_content_exists(self):
        assert (self.NB_DIR / "notebook-content.py").is_file()

    def test_platform_file_contains_correct_type(self):
        import json

        content = json.loads((self.NB_DIR / ".platform").read_text(encoding="utf-8"))
        assert content["metadata"]["type"] == "Notebook"
        assert content["metadata"]["displayName"] == "Notebook_SalesDB2"

    def test_notebook_content_references_sales_db_02(self):
        content = (self.NB_DIR / "notebook-content.py").read_text(encoding="utf-8")
        assert "Sales_DB_02" in content

    def test_notebook_content_has_pyspark_kernel(self):
        content = (self.NB_DIR / "notebook-content.py").read_text(encoding="utf-8")
        assert "synapse_pyspark" in content
