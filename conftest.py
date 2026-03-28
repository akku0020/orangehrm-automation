# Pytest configuration — add HTML report options

def pytest_configure(config):
    """Configure pytest-html report metadata."""
    config._metadata = {
        "Project": "OrangeHRM Automation - Noesys Assignment",
        "Tester": "Akhilesh",
        "Application": "https://opensource-demo.orangehrmlive.com",
        "Framework": "Python + Selenium 4 + POM",
    }