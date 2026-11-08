"""Presentation for Pivot: banner, colors, and the ledger table renderer.

Pure presentation, no ledger logic. Colors encode meaning:
cyan = structure, green = positive/income, red = negative/expense,
dim = rules and meta text.
"""

import os
import sys

BANNER = """\
██████╗ ██╗██╗   ██╗ ██████╗ ████████╗
██╔══██╗██║██║   ██║██╔═══██╗╚══██╔══╝
██████╔╝██║██║   ██║██║   ██║   ██║
██╔═══╝ ██║╚██╗ ██╔╝██║   ██║   ██║
██║     ██║ ╚████╔╝ ╚██████╔╝   ██║
╚═╝     ╚═╝  ╚═══╝   ╚═════╝    ╚═╝
 ▁▂▃▅▆▇  terminal finance tracker  ▇▆▅▃▂▁"""

CYAN = "\x1b[96m"
GREEN = "\x1b[92m"
RED = "\x1b[91m"
DIM = "\x1b[2m"
RESET = "\x1b[0m"


def colors_enabled():
    """Colors only when output is a real terminal and NO_COLOR is unset."""
    if not sys.stdout.isatty():
        return False
    return not os.environ.get("NO_COLOR")


def color(code, text, enabled):
    """Wrap `text` in the ANSI `code`; stays plain when disabled."""
    if not enabled:
        return text
    return f"{code}{text}{RESET}"


def signed_amount(amount, is_expense):
    """Two decimals with an always-visible sign, e.g. +1000.00 / -200.00."""
    if is_expense:
        return f"-{abs(amount):.2f}"
    return f"+{amount:.2f}"


def render_ledger(transactions, balance, enabled=False):
    """The balance view: an aligned table of the ledger plus the total."""
    if not transactions:
        return color(DIM, "No transactions yet.", enabled)

    lines = [
        f"  {'Date':<10} {'Description':<24} {'Type':<10} {'Amount':>9}",
        "  " + "-" * 55,
    ]
    for row in transactions:
        is_expense = row["Type"].upper() == "EXPENSE"
        signed = signed_amount(float(row["Amount"]), is_expense)
        line = (
            f"  {row['Date']:<10} {row['Description'][:24]:<24} "
            f"{row['Type']:<10} {signed:>9}"
        )
        tone = DIM if is_expense else GREEN
        lines.append(color(tone, line, enabled))

    lines.append("  " + "-" * 55)
    total = signed_amount(balance, balance < 0)
    total_text = "Balance".rjust(46) + " " + f"{total:>9}"
    tone = GREEN if balance >= 0 else RED
    lines.append(color(tone, "  " + total_text, enabled))
    return "\n".join(lines)


def render_monthly(summary, enabled=False):
    """Per-month table: Month, Income, Expense, Net, plus a Total row."""
    if not summary:
        return color(DIM, "No transactions yet.", enabled)

    lines = [
        f"  {'Month':<8} {'Income':>10} {'Expense':>10} {'Net':>11}",
        "  " + "-" * 43,
    ]
    totals = {"Income": 0.0, "Expense": 0.0, "Net": 0.0}
    for row in summary:
        for key in totals:
            totals[key] += row[key]
        net = signed_amount(row["Net"], row["Net"] < 0)
        line = (
            f"  {row['Month']:<8} "
            f"{signed_amount(row['Income'], False):>10} "
            f"{signed_amount(row['Expense'], True):>10} "
            f"{net:>11}"
        )
        tone = RED if row["Net"] < 0 else GREEN
        lines.append(color(tone, line, enabled))

    lines.append("  " + "-" * 43)
    net = signed_amount(totals["Net"], totals["Net"] < 0)
    total_line = (
        f"  {'Total':<8} "
        f"{signed_amount(totals['Income'], False):>10} "
        f"{signed_amount(totals['Expense'], True):>10} "
        f"{net:>11}"
    )
    lines.append(color(GREEN if totals["Net"] >= 0 else RED, total_line, enabled))
    return "\n".join(lines)
