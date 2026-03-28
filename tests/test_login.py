"""
Scenario 1: Verify login with valid and invalid credentials.
"""

import pytest
from pages.login_page import LoginPage
from utils.driver_setup import get_driver
from utils.config import VALID_USERNAME, VALID_PASSWORD, INVALID_USERNAME, INVALID_PASSWORD


class TestLogin:

    @pytest.fixture(autouse=True)
    def setup_teardown(self):
        """Set up WebDriver before each test; quit after."""
        self.driver = get_driver()
        self.login_page = LoginPage(self.driver)
        self.login_page.open()
        yield
        self.driver.quit()

    def test_valid_login(self):
        """TC-001: Login with valid credentials should show the Dashboard."""
        self.login_page.login(VALID_USERNAME, VALID_PASSWORD)

        assert self.login_page.is_dashboard_visible(), \
            "Dashboard should be visible after successful login."

        print("\nTC-001 PASSED: Valid login redirected to Dashboard.")

    def test_invalid_username(self):
        """TC-002: Login with invalid username should show error message."""
        self.login_page.login(INVALID_USERNAME, VALID_PASSWORD)

        assert self.login_page.is_error_displayed(), \
            "Error message should appear for invalid username."

        error = self.login_page.get_error_message()
        assert "Invalid credentials" in error, \
            f"Expected 'Invalid credentials' but got: '{error}'"

        print(f"\nTC-002 PASSED: Error shown - '{error}'")

    def test_invalid_password(self):
        """TC-003: Login with invalid password should show error message."""
        self.login_page.login(VALID_USERNAME, INVALID_PASSWORD)

        assert self.login_page.is_error_displayed(), \
            "Error message should appear for invalid password."

        error = self.login_page.get_error_message()
        assert "Invalid credentials" in error, \
            f"Expected 'Invalid credentials' but got: '{error}'"

        print(f"\nTC-003 PASSED: Error shown - '{error}'")

    def test_both_fields_invalid(self):
        """TC-004: Login with both fields invalid should show error message."""
        self.login_page.login(INVALID_USERNAME, INVALID_PASSWORD)

        assert self.login_page.is_error_displayed(), \
            "Error message should appear when both credentials are invalid."

        print("\nTC-004 PASSED: Error shown for completely invalid credentials.")

    def test_empty_credentials(self):
        """TC-005: Login with empty fields should show validation errors."""
        self.login_page.click_login()

        # OrangeHRM shows "Required" field errors for empty submission
        assert self.login_page.is_required_popup_displayed(), \
            "Dashboard should NOT appear with empty credentials."

        print("\nTC-005 PASSED: Login blocked with empty credentials.")