# OrangeHRM Automation - Noesys Software Assignment

Automation test suite for OrangeHRM using Python + Selenium with Page Object Model (POM).

## 📁 Project Structure

```
orangehrm_automation/
├── pages/                  # Page Object Model classes
│   ├── base_page.py
│   ├── login_page.py
│   ├── pim_page.py
│   ├── leave_page.py
│   └── buzz_page.py
├── tests/                  # Test scenarios
│   ├── test_login.py
│   ├── test_pim.py
│   ├── test_leave.py
│   └── test_buzz.py
├── utils/
│   ├── config.py           # Configuration & credentials
│   └── driver_setup.py     # WebDriver setup
├── requirements.txt
└── README.md
```

## ⚙️ Setup Instructions

### 1. Install Python dependencies
```bash
pip install -r requirements.txt
```

### 2. Install ChromeDriver
Make sure Google Chrome is installed. `webdriver-manager` handles the driver automatically.

### 3. Run all tests
```bash
pytest tests/ -v --html=report.html
```

### 4. Run a specific test file
```bash
pytest tests/test_login.py -v
```

## 🔐 Credentials (OrangeHRM Demo)
- URL: https://opensource-demo.orangehrmlive.com
- Username: `Admin`
- Password: `admin123`

## 📋 Test Scenarios Covered
1. ✅ Login with valid and invalid credentials
2. ✅ Add new employee in PIM and verify in employee list
3. ✅ Search employee by ID and validate correct record
4. ✅ Apply for leave and validate success confirmation
5. ✅ Create Buzz post and verify it appears on feed