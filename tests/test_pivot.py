import pytest

from pivot.core import (
    get_balance,
    initialize_csv,
    monthly_summary,
    normalize_date,
    read_config,
    read_transactions,
    save_transaction,
    validate_date,
    validate_type,
)


def test_validate_date():
    assert validate_date("2026-01-31") is True
    assert validate_date("31-01-2026") is False
    assert validate_date("2026/01/31") is False


def test_validate_date_allows_short_month_day():
    # the regex permits 1-2 digit months/days; normalize_date pads them after
    assert validate_date("2026-1-1") is True
    assert validate_date("yesterday") is False


def test_validate_type():
    assert validate_type("Income") is True
    assert validate_type("Expense") is True
    assert validate_type("Cat") is False


def test_normalize_date():
    assert normalize_date("2026-01-31") == "2026-01-31"
    assert normalize_date("2026-01-05") == "2026-01-05"


def test_initialize_csv_creates_header(tmp_path):
    path = tmp_path / "ledger.csv"
    initialize_csv(path)
    assert path.read_text().strip() == "Date,Description,Amount,Type"


def test_initialize_csv_keeps_existing_data(tmp_path):
    path = tmp_path / "ledger.csv"
    initialize_csv(path)
    save_transaction(path, "2026-01-31", "food", 200.0, "Expense")
    initialize_csv(path)  # must not clobber the extra row
    assert path.read_text().count("\n") == 2


def test_balance_round_trip(tmp_path):
    path = tmp_path / "ledger.csv"
    initialize_csv(path)
    save_transaction(path, "2026-01-01", "salary", 1000.0, "Income")
    save_transaction(path, "2026-01-02", "food", 200.0, "Expense")
    save_transaction(path, "2026-01-03", "gift", 50.0, "Income")
    assert get_balance(path) == pytest.approx(850.0)


def test_read_transactions(tmp_path):
    path = tmp_path / "ledger.csv"
    initialize_csv(path)
    save_transaction(path, "2026-01-01", "salary", 1000.0, "Income")
    transaction_rows = read_transactions(path)
    assert transaction_rows == [
        {"Date": "2026-01-01", "Description": "salary",
         "Amount": 1000.0, "Type": "Income"}
    ]


def test_initialize_csv_creates_missing_parent_dirs(tmp_path):
    path = tmp_path / "pivot" / "ledger.csv"
    initialize_csv(path)
    assert path.read_text().strip() == "Date,Description,Amount,Type"


def test_get_data_path_defaults_to_home(monkeypatch, tmp_path):
    from pivot.cli import get_data_path
    monkeypatch.delenv("PIVOT_DATA", raising=False)
    monkeypatch.setenv("HOME", str(tmp_path))
    assert get_data_path() == str(tmp_path / ".pivot" / "finance.csv")


def test_get_data_path_honors_pivot_data(monkeypatch):
    from pivot.cli import get_data_path
    monkeypatch.setenv("PIVOT_DATA", "/tmp/my-ledger.csv")
    assert get_data_path() == "/tmp/my-ledger.csv"



def test_monthly_summary_groups_by_month(tmp_path):
    path = tmp_path / "ledger.csv"
    initialize_csv(path)
    save_transaction(path, "2026-01-05", "salary", 1000.0, "Income")
    save_transaction(path, "2026-01-20", "food", 200.0, "Expense")
    save_transaction(path, "2026-02-14", "bus", 20.0, "Expense")
    summary = monthly_summary(path)
    assert summary == [
        {"Month": "2026-01", "Income": 1000.0, "Expense": 200.0, "Net": 800.0},
        {"Month": "2026-02", "Income": 0.0, "Expense": 20.0, "Net": -20.0},
    ]


def test_monthly_summary_empty_ledger(tmp_path):
    path = tmp_path / "ledger.csv"
    initialize_csv(path)
    assert monthly_summary(path) == []


def test_render_monthly_monochrome():
    from pivot.ui import render_monthly
    rows = [{"Month": "2026-01", "Income": 1000.0,
             "Expense": 200.0, "Net": 800.0},
            {"Month": "2026-02", "Income": 0.0,
             "Expense": 20.0, "Net": -20.0}]
    out = render_monthly(rows)
    assert "\x1b[" not in out
    assert "2026-01" in out and "2026-02" in out
    assert "Total" in out
    lines = out.splitlines()
    assert lines[0].strip().startswith("Month")
    assert lines[1].startswith("  ----")


def test_render_monthly_empty():
    from pivot.ui import render_monthly
    assert render_monthly([], enabled=False) == "No transactions yet."


def test_read_config_reads_data_key(tmp_path):
    path = tmp_path / "config"
    path.write_text("data = /tmp/my-ledger.csv\n")
    assert read_config(path) == {"data": "/tmp/my-ledger.csv"}


def test_read_config_skips_comments_and_blanks(tmp_path):
    path = tmp_path / "config"
    path.write_text("# my pivot config\n\ndata = /tmp/my-ledger.csv\n")
    assert read_config(path) == {"data": "/tmp/my-ledger.csv"}


def test_read_config_missing_file(tmp_path):
    assert read_config(tmp_path / "nope") == {}


def test_get_data_path_prefers_env_then_config(monkeypatch, tmp_path):
    from pivot.cli import get_data_path
    pivot_dir = tmp_path / ".pivot"
    pivot_dir.mkdir()
    config = pivot_dir / "config"
    config.write_text("data = /tmp/from-config.csv\n")
    monkeypatch.setenv("HOME", str(tmp_path))  # ~/.pivot/config -> tmp_path
    monkeypatch.delenv("PIVOT_DATA", raising=False)
    assert get_data_path() == "/tmp/from-config.csv"
    monkeypatch.setenv("PIVOT_DATA", "/tmp/from-env.csv")
    assert get_data_path() == "/tmp/from-env.csv"


def test_color_disabled():
    from pivot.ui import color, CYAN
    assert color(CYAN, "hi", enabled=False) == "hi"


def test_color_enabled():
    from pivot.ui import color, CYAN
    assert color(CYAN, "hi", enabled=True) == "\x1b[96mhi\x1b[0m"


def test_colors_enabled_no_color_env(monkeypatch):
    from pivot.ui import colors_enabled
    monkeypatch.setenv("NO_COLOR", "1")
    assert colors_enabled() is False


def test_signed_amount():
    from pivot.ui import signed_amount
    assert signed_amount(200.0, True) == "-200.00"
    assert signed_amount(1000.0, False) == "+1000.00"


def test_render_ledger_monochrome():
    from pivot.ui import render_ledger
    rows = [{"Date": "2026-01-01", "Description": "salary",
             "Amount": 1000.0, "Type": "Income"},
            {"Date": "2026-01-02", "Description": "food",
             "Amount": 200.0, "Type": "Expense"}]
    out = render_ledger(rows, 850.0)
    assert "\x1b[" not in out
    assert out == (
        "  Date       Description              Type          Amount\n"
        "  -------------------------------------------------------\n"
        "  2026-01-01 salary                   Income      +1000.00\n"
        "  2026-01-02 food                     Expense      -200.00\n"
        "  -------------------------------------------------------\n"
        "                                         Balance   +850.00"
    )


def test_render_ledger_empty():
    from pivot.ui import render_ledger
    assert render_ledger([], 0.0, enabled=False) == "No transactions yet."
    assert render_ledger([], 0.0, enabled=True) == "\x1b[2mNo transactions yet.\x1b[0m"
