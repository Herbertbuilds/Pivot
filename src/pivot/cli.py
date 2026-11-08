"""Terminal interface for Pivot: the menu, the input prompts, and app startup."""

import os

from pivot.core import (
    get_balance,
    initialize_csv,
    normalize_date,
    read_transactions,
    save_transaction,
    validate_date,
    validate_type,
)
from pivot.ui import (
    BANNER,
    CYAN,
    DIM,
    GREEN,
    RED,
    color,
    colors_enabled,
    format_ledger_line,
    render_ledger,
    signed_amount,
)

DATA_FILE_ENV = "PIVOT_DATA"


def get_data_path():
    """Resolve the ledger location: $PIVOT_DATA, else finance.csv in a fixed
    place (~/.pivot), so the same ledger is used no matter which directory
    the terminal is in."""
    return os.environ.get(
        DATA_FILE_ENV,
        os.path.expanduser("~/.pivot/finance.csv"),
    )


def show_banner(enabled):
    print(color(CYAN, BANNER, enabled))
    print()


def show_menu(enabled, ledger_path):
    print(f"\n{color(DIM, '--- Finance Tracker ---', enabled)}")
    padded = format_ledger_line(ledger_path)
    text = padded.lstrip()
    pad = len(padded) - len(text)
    print(" " * pad + color(DIM, text, enabled))
    for number, label in [("1", "Add Transaction"),
                          ("2", "View Balance"),
                          ("3", "Exit")]:
        print(f"{color(CYAN, '[', enabled)}{number}"
              f"{color(CYAN, ']', enabled)} {label}")


def prompt_date(enabled):
    """Keep asking until the user enters a valid date."""
    while True:
        date = input(f"Date (YYYY-MM-DD), e.g., {color(CYAN, '2026-01-31', enabled)}: ")
        if validate_date(date):
            return normalize_date(date)
        print(color(RED, "Invalid format.", enabled))


def prompt_description(enabled):
    return input("Description: ")


def prompt_amount(enabled):
    """Keep asking until the user enters a number."""
    while True:
        try:
            return float(input("Amount: "))
        except ValueError:
            print(color(RED, "Numbers only.", enabled))


def prompt_transaction_type(enabled):
    """Keep asking until the user enters Income or Expense."""
    while True:
        transaction_type = input("Type (Income/Expense): ").capitalize()
        if validate_type(transaction_type):
            return transaction_type


def add_transaction(path, enabled):
    date = prompt_date(enabled)
    description = prompt_description(enabled)
    amount = prompt_amount(enabled)
    transaction_type = prompt_transaction_type(enabled)
    save_transaction(path, date, description, amount, transaction_type)
    saved = (f"+ Saved: {date} | {description[:24]} | "
             f"{signed_amount(amount, transaction_type == 'Expense')} "
             f"({transaction_type})")
    print(color(GREEN, saved, enabled))


def show_balance(path, enabled):
    print(render_ledger(read_transactions(path),
                        get_balance(path), enabled=enabled))


def main():
    enabled = colors_enabled()
    data_path = get_data_path()
    initialize_csv(data_path)
    show_banner(enabled)

    while True:
        show_menu(enabled, data_path)
        choice = input(f"{color(CYAN, 'Choose an option', enabled)}: ")

        if choice == "1":
            add_transaction(data_path, enabled)
        elif choice == "2":
            show_balance(data_path, enabled)
        elif choice == "3":
            print(color(DIM, "Goodbye.", enabled))
            break


if __name__ == "__main__":
    main()
