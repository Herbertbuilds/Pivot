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
