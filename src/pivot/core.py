"""Core logic for Pivot: input validation and the CSV-backed ledger.

Everything here is independent of the terminal, which makes it easy to
unit-test: every function takes its file path as an argument.
"""

import csv
import os
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
    parent = os.path.dirname(os.path.abspath(path))
    os.makedirs(parent, exist_ok=True)
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


def monthly_summary(path):
    """Group the ledger by month: one dict per month with Income, Expense
    and Net totals, oldest first. Reuses read_transactions."""
    buckets = {}
    for row in read_transactions(path):
        month = row["Date"][:7]  # YYYY-MM-DD -> YYYY-MM
        if month not in buckets:
            buckets[month] = {"Month": month, "Income": 0.0,
                              "Expense": 0.0, "Net": 0.0}
        bucket = buckets[month]
        amount = row["Amount"]
        if row["Type"].lower() == "expense":
            bucket["Expense"] += amount
            bucket["Net"] -= amount
        else:
            bucket["Income"] += amount
            bucket["Net"] += amount
    return [buckets[month] for month in sorted(buckets)]


def read_config(path):
    """Read a simple config file: `key = value` lines, # comments, blanks
    ignored. Empty dict when the file doesn't exist."""
    settings = {}
    try:
        with open(path, "r") as file:
            lines = file.read().splitlines()
    except FileNotFoundError:
        return {}
    for line in lines:
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        key, _, value = line.partition("=")
        key, value = key.strip(), value.strip()
        if key and value:
            settings[key.lower()] = value
    return settings
