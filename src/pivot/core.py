"""Core logic for Pivot: input validation and the CSV-backed ledger.

Everything here is independent of the terminal, which makes it easy to
unit-test: every function takes its file path as an argument.
"""

import csv
import re
from datetime import datetime

CSV_HEADER = ["Date", "Description", "Amount", "Type"]


def validate_date(string):
    """Return True if `string` looks like a YYYY-MM-DD date."""
    if re.search(r"^\d{4}-\d{1,2}-\d{1,2}$", string):
        return True
    return False


def validate_type(string):
    """Return True if `string` is a recognised transaction type."""
    if string in ["Income", "Expense"]:
        return True
    return False


def normalize_date(string):
    """Format a validated date string consistently, e.g. 2026-1-5 -> 2026-01-05."""
    date_obj = datetime.strptime(string, "%Y-%m-%d")
    return date_obj.strftime("%Y-%m-%d")


def initialize_csv(path):
    """Create the ledger file with its header row if it doesn't exist yet."""
    try:
        with open(path, "r") as file:
            return
    except FileNotFoundError:
        with open(path, "w", newline="") as file:
            writer = csv.writer(file)
            writer.writerow(CSV_HEADER)


def save_transaction(path, date, description, amount, transaction_type):
    """Append one transaction to the ledger at `path`."""
    with open(path, "a", newline="") as file:
        writer = csv.writer(file)
        writer.writerow([date, description, amount, transaction_type])


def get_balance(path):
    """Read the whole ledger and return the running balance."""
    total = 0.0
    with open(path, "r") as file:
        reader = csv.DictReader(file)
        for row in reader:
            amount = float(row["Amount"])
            if row["Type"].lower() == "expense":
                total -= amount
            else:
                total += amount
    return total


def read_transactions(path):
    """Read the whole ledger as dicts, Amount cast to float, in file order."""
    transactions = []
    with open(path, "r") as file:
        reader = csv.DictReader(file)
        for row in reader:
            transactions.append({
                "Date": row["Date"],
                "Description": row["Description"],
                "Amount": float(row["Amount"]),
                "Type": row["Type"],
            })
    return transactions
