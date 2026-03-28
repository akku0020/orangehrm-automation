"""
Scenario 2: Add a new employee in PIM module and verify it appears in employee list.
Scenario 3: Search for an employee by ID and validate the correct record is displayed.
"""

import pytest
from pages.login_page import LoginPage
from pages.pim_page import PimPage
from utils.driver_setup import get_driver
from utils.config import VALID_USERNAME, VALID_PASSWORD, NEW_EMPLOYEE


class TestPim:

    @pytest.fixture(autouse=True)
    def setup_teardown(self):
        """Log in before each test and quit driver after."""
        self.driver = get_driver()

        # Login
        login_page = LoginPage(self.driver)
        login_page.open()
        login_page.login(VALID_USERNAME, VALID_PASSWORD)
        assert login_page.is_dashboard_visible(), "Login failed — cannot run PIM tests."

        self.pim = PimPage(self.driver)
        yield
        self.driver.quit()

    def test_add_new_employee(self):
        """
        TC-006: Add a new employee in PIM and verify they appear in the employee list.
        """
        first  = NEW_EMPLOYEE["first_name"]
        middle = NEW_EMPLOYEE["middle_name"]
        last   = NEW_EMPLOYEE["last_name"]

        # Add employee and capture generated ID
        employee_id = self.pim.add_employee(first, middle, last)
        print(f"\n  Generated Employee ID: {employee_id}")

        assert employee_id, "Employee ID should be auto-generated after adding employee."

        # Search in Employee List to confirm the record exists
        self.pim.search_employee_by_name(first)

        result_count = self.pim.get_search_result_count()
        assert result_count >= 1, \
            f"Expected at least 1 result for '{first} {last}', but found {result_count}."

        assert self.pim.is_employee_in_results(last), \
            f"Employee '{first} {last}' not found in search results."

        print(f"\nTC-006 PASSED: Employee '{first} {last}' added and found in list.")

    def test_search_nonexistent_employee(self):
        """
        TC-008: Search for a non-existent employee ID should show no records.
        """
        self.pim.search_employee_by_id("XXXXX99999")

        result_count = self.pim.get_search_result_count()
        # Either 0 rows or a "No Records Found" message is acceptable
        no_records = self.pim.is_no_records_found() or result_count == 0
        assert no_records, \
            "Expected no results for a non-existent employee ID."

        print("\nTC-008 PASSED: No records found for invalid employee ID.")