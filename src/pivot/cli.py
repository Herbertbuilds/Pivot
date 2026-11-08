"""Terminal interface for Pivot: the menu, the input prompts, and app startup."""

import os

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
from pivot.ui import (
    BANNER,
    CYAN,
    DIM,
    GREEN,
    RED,
    color,
    colors_enabled,
    render_ledger,
    render_monthly,
    signed_amount,
)

DATA_FILE_ENV = "PIVOT_DATA"
CONFIG_FILE = ".pivot/config"
DEFAULT_DATA_FILE = ".pivot/finance.csv"

MENU_ITEMS = [
    ("1", "Add Transaction"),
    ("2", "View Balance"),
    ("3", "View All Transactions"),
    ("4", "Monthly Summary"),
    ("5", "Exit"),
]


def get_data_path():
    """Resolve the ledger location: $PIVOT_DATA, then the `data` setting in
    ~/.pivot/config, then finance.csv in ~/.pivot — so the same ledger is
    used no matter which directory the terminal is in."""
    env_path = os.environ.get(DATA_FILE_ENV)
    if env_path:
        return env_path
    configured = read_config(os.path.expanduser(f"~/{CONFIG_FILE}")).get("data")
    if configured:
        return configured
    return os.path.expanduser(f"~/{DEFAULT_DATA_FILE}")


def show_banner(enabled):
    print(color(CYAN, BANNER, enabled))
    print()


def show_menu(enabled):
    print(f"\n{color(DIM, '--- Finance Tracker ---', enabled)}")
    for number, label in MENU_ITEMS:
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
    balance = get_balance(path)
    tone = GREEN if balance >= 0 else RED
    print(color(tone, f"Current Balance: {signed_amount(balance, balance < 0)}",
                enabled))


def show_all_transactions(path, enabled):
    print(render_ledger(read_transactions(path),
                        get_balance(path), enabled=enabled))


def show_monthly_summary(path, enabled):
    print(render_monthly(monthly_summary(path), enabled=enabled))


def main():
    enabled = colors_enabled()
    data_path = get_data_path()
    initialize_csv(data_path)
    show_banner(enabled)

    while True:
        show_menu(enabled)
        choice = input(f"{color(CYAN, 'Choose an option', enabled)}: ")

        if choice == "1":
            add_transaction(data_path, enabled)
        elif choice == "2":
            show_balance(data_path, enabled)
        elif choice == "3":
            show_all_transactions(data_path, enabled)
        elif choice == "4":
            show_monthly_summary(data_path, enabled)
        elif choice == "5":
            print(color(DIM, "Goodbye.", enabled))
            break
        else:
            print(color(RED, "Choose 1-5.", enabled))


if __name__ == "__main__":
    main()
