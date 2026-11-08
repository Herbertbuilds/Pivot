import pytest

from pivot.core import (
    get_balance,
    initialize_csv,
    normalize_date,
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


def test_ledger_line_right_aligned_and_shorthanded(monkeypatch):
    from pivot.ui import format_ledger_line
    monkeypatch.setenv("HOME", "/home/ub")
    line = format_ledger_line("/home/ub/.pivot/finance.csv", columns=40)
    assert line == " " * 11 + "ledger: ~/.pivot/finance.csv"


def test_ledger_line_narrow_terminal_lets_path_overflow():
    from pivot.ui import format_ledger_line
    long_path = "/home/user/very/deep/dirs/finance.csv"
    line = format_ledger_line(long_path, columns=20)
    assert line.lstrip().startswith("ledger:")


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
