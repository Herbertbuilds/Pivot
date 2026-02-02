import csv
import re
import os
from datetime import datetime

BASE_DIR = os.path.dirname(os.path.realpath(__file__))
FILE_PATH = os.path.join(BASE_DIR, "finance.csv")

def main():
    print(f"DEBUG: Using database file at: {FILE_PATH}")
    
    initialize_csv(FILE_PATH)
    
    while True:
        print("\n--- Finance Tracker ---")
        print("1. Add Transaction")
        print("2. View Balance")
        print("3. Exit")
        choice = input("Choose an option: ")

        if choice == "1":
            while True:
                d = input("Date (YYYY-MM-DD), e.g., 2026-01-31: ")
                if validate_date(d):
                    date_obj = datetime.strptime(d, "%Y-%m-%d")
                    d = date_obj.strftime("%Y-%m-%d")
                    break
                print("Invalid format.")
            
            desc = input("Description: ")
            
            while True:
                try:
                    amt = float(input("Amount: "))
                    break
                except ValueError:
                    print("Numbers only.")
            
            while True:
                t = input("Type (Income/Expense): ").capitalize()
                if validate_type(t):
                    break
            
            save_transaction(FILE_PATH, d, desc, amt, t)
        
        elif choice == "2":
            print(f"Current Balance: ${get_balance(FILE_PATH):.2f}")
        elif choice == "3":
            break

def initialize_csv(path):
    try:
        with open(path, "r") as file:
            return
    except FileNotFoundError:
        with open(path, "w", newline="") as file:
            writer = csv.writer(file)
            writer.writerow(["Date", "Description", "Amount", "Type"])

def validate_date(s):
    if re.search(r"^\d{4}-\d{1,2}-\d{1,2}$", s):
        return True
    return False

def validate_type(s):
    if s in ["Income", "Expense"]:
        return True
    return False

def save_transaction(path, date, desc, amount, type_):
    with open(path, "a", newline="") as file:
        writer = csv.writer(file)
        writer.writerow([date, desc, amount, type_])

def get_balance(path):
    total = 0.0
    with open(path, "r") as file:
        reader = csv.DictReader(file)
        for row in reader:
            val = float(row["Amount"])
            if row["Type"].lower() == "expense":
                total -= val
            else:
                total += val
    return total

if __name__ == "__main__":
    main()