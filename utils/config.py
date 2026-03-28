# utils/config.py
import random

BASE_URL = "https://opensource-demo.orangehrmlive.com"

VALID_USERNAME = "Admin"
VALID_PASSWORD = "admin123"
INVALID_USERNAME = "wronguser"
INVALID_PASSWORD = "wrongpass123"

# New employee test data
NEW_EMPLOYEE = {
    "first_name": "Tester",
    "middle_name": "Test",
    "last_name": "QA",
}

# Leave application test data
LEAVE_DATA = {
    "leave_type": "CAN - Personal",
    "from_date": "2026-30-03",
    "to_date": "2026-31-03",
    "comment": "Automation test leave request",
}


random_value = str((random.randint(100000, 999999)))
# Buzz post test data
BUZZ_POST = {
    "message": f"{random_value}Hello from Automation! This is a test post by Tester. #QA #Testing",
}

IMPLICIT_WAIT = 10
EXPLICIT_WAIT = 15