"""Terminal interface for Pivot: the menu, the input prompts, and app startup."""

import os

from pivot.core import (
    get_balance,
    initialize_csv,
    normalize_date,
    save_transaction,
    validate_date,
    validate_type,
)

DATA_FILE_ENV = "PIVOT_DATA"


def get_data_path():
    """Resolve the ledger location: $PIVOT_DATA, else finance.csv in the
    directory the terminal is currently in."""
    return os.environ.get(DATA_FILE_ENV, "finance.csv")


def prompt_date():
    """Keep asking until the user enters a valid date."""
    while True:
        date = input("Date (YYYY-MM-DD), e.g., 2026-01-31: ")
        if validate_date(date):
            return normalize_date(date)
        print("Invalid format.")


def prompt_description():
    return input("Description: ")


def prompt_amount():
    """Keep asking until the user enters a number."""
    while True:
        try:
            return float(input("Amount: "))
        except ValueError:
            print("Numbers only.")


def prompt_transaction_type():
    """Keep asking until the user enters Income or Expense."""
    while True:
        transaction_type = input("Type (Income/Expense): ").capitalize()
        if validate_type(transaction_type):
            return transaction_type


def add_transaction(path):
    date = prompt_date()
    description = prompt_description()
    amount = prompt_amount()
    transaction_type = prompt_transaction_type()
    save_transaction(path, date, description, amount, transaction_type)


def main():
    data_path = get_data_path()
    initialize_csv(data_path)

    while True:
        print("\n--- Finance Tracker ---")
        print("1. Add Transaction")
        print("2. View Balance")
        print("3. Exit")
        choice = input("Choose an option: ")

        if choice == "1":
            add_transaction(data_path)
        elif choice == "2":
            print(f"Current Balance: ${get_balance(data_path):.2f}")
        elif choice == "3":
            break


if __name__ == "__main__":
    main()
