import csv
import re
from datetime import datetime

def main():
    filename = "finance.csv"
    initialize_csv(filename)
    
    while True:
        print("\n--- Finance Tracker ---")
        print("1. Add Transaction")
        print("2. View Balance")
        print("3. Exit")
        choice = input("Choose an option: ")

        if choice == "1":
            while True:
                d = input("Date (YYYY-MM-DD), e.g., 2026-01-31): ")
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
            
            save_transaction(filename, d, desc, amt, t)
        
        elif choice == "2":
            print(f"Current Balance: ${get_balance(filename):.2f}")
        elif choice == "3":
            break

def initialize_csv(filename):
    try:
        with open(filename, "r") as file:
            return
    except FileNotFoundError:
        with open(filename, "w", newline="") as file:
            writer = csv.writer(file)
            writer.writerow(["Date", "Description", "Amount", "Type"])


def validate_date(s):
    if re.search(r"^\d{4}-\d{1,2}-\d{1,2}$", s):
        return True
    else:
        return False
    

def validate_type(s):
    if s in ["Income", "Expense"]:
        return True
    else:
        return False

def save_transaction(filename, date, desc, amount, type_):
    with open(filename, "a", newline="") as file:
        writer = csv.writer(file)
        writer.writerow([date, desc, amount, type_])


def get_balance(filename):
    total = 0.0
    with open(filename, "r") as file:
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