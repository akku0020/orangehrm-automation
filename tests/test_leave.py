"""
Scenario 4: Apply for leave and validate the success confirmation message.
"""

import pytest
from pages.login_page import LoginPage
from pages.leave_page import LeavePage
from utils.driver_setup import get_driver
from utils.config import VALID_USERNAME, VALID_PASSWORD, LEAVE_DATA


class TestLeave:

    @pytest.fixture(autouse=True)
    def setup_teardown(self):
        """Log in before each test and quit driver after."""
        self.driver = get_driver()

        login_page = LoginPage(self.driver)
        login_page.open()
        login_page.login(VALID_USERNAME, VALID_PASSWORD)
        assert login_page.is_dashboard_visible(), "Login failed — cannot run Leave tests."

        self.leave = LeavePage(self.driver)
        yield
        self.driver.quit()

    def test_apply_leave_success(self):
        """
        TC-009: Apply for leave with valid data and verify success toast is shown.
        """
        self.leave.apply_leave(
            from_date=LEAVE_DATA["from_date"],
            to_date=LEAVE_DATA["to_date"],
            comment=LEAVE_DATA["comment"],
        )

        assert self.leave.is_success_toast_visible(), \
            "Success toast notification should appear after applying for leave."

        print("\n TC-009 PASSED: Leave applied successfully. Success toast visible.")

    def test_apply_leave_same_day(self):
        """
        TC-010: Apply for single-day leave (from_date == to_date) and verify success.
        """
        self.leave.apply_leave(
            from_date="2026-05-05",
            to_date="2026-05-05",
            comment="Single day automation test leave",
        )

        assert self.leave.is_success_toast_visible(), \
            "Success toast should appear for single-day leave."

        print("\nTC-010 PASSED: Single-day leave applied successfully.")