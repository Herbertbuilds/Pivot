![Python Version](https://img.shields.io/badge/python-3.9%2B-blue.svg) ![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg) ![CS50P](https://img.shields.io/badge/CS50P-Completed-green.svg)

# 💰 Pivot
> A lightweight **CLI** financial management tool built for speed and efficiency.

![Project Demo](docs/output_demo.gif)

## 🎯 Overview
Why I built Pivot, was for the final **CS50P** final project, then I realised I have a great idea that I can built on, having a **lightweight**, easy to set up CLI finance tracking program,
no need to download huge aplications just a simple terminal program that allows you to record your daily expenses/income and calculates your balance from any location in the terminal 

### Key Features:
* **Instant Logging:** Quickly add transactions with Descriptions CLI.
* **Data Persistence:** Automatically saves to a local CSV file.
* **Summary Reports:** Easily calculate your real time balance.
* **Validation:** Robust error handling for dates and currency inputs.

## 🛠️ Technical Implementation
* **Language:** Python 3.9+
* **Storage:** CSV (Comma Separated Values)
* **Testing:** Pytest (Unit tests for core logic)NB! not required to run the program just used it for testing reasons
* **Environment:** Optimized for **Low end devices**.

## 🌍 Running From Anywhere

### Install
```bash
pip install git+https://github.com/Herbertbuilds/Pivot.git
pivot
```

Or with [`pipx`](https://pipx.pypa.io/) - recommended for CLI tools, keeps
Pivot in its own isolated environment and puts the command on your PATH:

```bash
pipx install git+https://github.com/Herbertbuilds/Pivot.git
```

### Update
```bash
pipx install --force git+https://github.com/Herbertbuilds/Pivot.git
```
(For plain `pip` installs: `pip install -U git+https://...`.)

### Uninstall
```bash
pipx uninstall pivot-finance
```
Uninstalling never touches your data - the ledger stays put (see below).

### Run without installing
Pivot's ledger follows you everywhere, but if you'd rather run straight from
a clone than install, an alias works fine:

```fish
# Fish
alias Pivot="env PYTHONPATH=~/Code/Pivot/src python3 -m pivot"
funcsave Pivot
```
```bash
# Bash/Zsh - add to your .bashrc or .zshrc
alias pivot='cd /path/to/Pivot && PYTHONPATH=src python3 -m pivot'
```

### The Menu
```
[1] Add Transaction        log an income or expense with validation
[2] View Balance           the running total
[3] View All Transactions  every entry in an aligned table
[4] Monthly Summary        income/expense/net grouped by month
[5] Exit
```

### The Ledger Location
Pivot keeps its ledger at `~/.pivot/finance.csv` - the same file no matter
which directory you run it from, so your balance never resets just because
you `cd`'d somewhere else. Precedence:

1. `$PIVOT_DATA` environment variable
2. `~/.pivot/config` file - a line like `data = /path/to/your.csv`
3. the default `~/.pivot/finance.csv`

> 💡 The menu header always shows which ledger you're talking to.

### Project Structure
```
Pivot/
├── docs/              # README media (demo GIF)
├── src/pivot/         # the app (core logic + terminal interface)
└── tests/             # pytest suite
```
