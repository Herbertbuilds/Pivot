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
* **Language:** Python 3.x
* **Storage:** CSV (Comma Separated Values)
* **Testing:** Pytest (Unit tests for core logic)NB! not required to run the program just used it for testing reasons
* **Environment:** Optimized for **Low end devices**.

## 🌍 Running From Anywhere
To run Pivot as a global command, install it as a package:

```bash
pip install git+https://github.com/Herbertbuilds/Pivot.git
pivot
```

### My Setup (MX Linux + Fish Shell)
Using the **Fish shell**, without installing anything system-wide:
1. `alias Pivot="env PYTHONPATH=~/Code/Pivot/src python3 -m pivot"`
2. `funcsave Pivot`

### For Bash/Zsh Users
Add the following to your `.bashrc` or `.zshrc`:
```bash
alias pivot='cd /absolute/path/to/Pivot && python3 -m pivot'
```
All thats left is to restart your terminal and your all set up.

### Project Structure
```
Pivot/
├── docs/              # README media (demo GIF)
├── src/pivot/         # the app (core logic + terminal interface)
└── tests/             # pytest suite
```
