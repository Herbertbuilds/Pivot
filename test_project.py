from project import validate_date, validate_type

def test_validate_date():
    assert validate_date("2026-01-31") == True
    assert validate_date("31-01-2026") == False
    assert validate_date("2026/01/31") == False

def test_validate_type():
    assert validate_type("Income") == True
    assert validate_type("Expense") == True
    assert validate_type("Cat") == False

def test_validate_date_format():
    assert validate_date("2026-1-1") == False
    assert validate_date("yesterday") == False