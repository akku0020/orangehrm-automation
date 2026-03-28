import time
import random
from selenium.common import TimeoutException
from selenium.webdriver import ActionChains, Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait

from pages.base_page import BasePage

# How long to wait for the "already exists" error to appear after clicking Save
DUPLICATE_ID_WAIT = 3   # seconds
MAX_ID_RETRIES    = 5   # max attempts before giving up

class PimPage(BasePage):
    """Page Object for the PIM (Employee Management) module."""

    # --- Navigation ---
    PIM_MENU          = (By.XPATH, "//span[text()='PIM']")
    ADD_EMPLOYEE_MENU = (By.XPATH, "//a[text()='Add Employee']")
    EMPLOYEE_LIST_MENU = (By.XPATH, "//a[text()='Employee List']")

    # --- Add Employee Form ---
    FIRST_NAME_INPUT  = (By.NAME, "firstName")
    MIDDLE_NAME_INPUT = (By.NAME, "middleName")
    LAST_NAME_INPUT   = (By.NAME, "lastName")
    EMPLOYEE_ID_FIELD = (By.XPATH, "//label[text()='Employee Id']/following::input[1]")
    SAVE_BUTTON       = (By.CSS_SELECTOR, "button[type='submit']")
    DUPLICATE_ID_ERROR = (By.XPATH, "//span[contains(.,'Employee Id already exists')]")

    # --- Employee List / Search ---
    SEARCH_FIRST_NAME = (By.XPATH, "//label[contains(.,'Employee Name')]/parent::div/following-sibling::div//input")
    SEARCH_EMP_ID     = (By.XPATH, "//label[contains(.,'Employee Id')]/parent::div/following-sibling::div//input")
    SEARCH_BUTTON     = (By.CSS_SELECTOR, "button[type='submit']")
    SEARCH_RESULTS    = (By.CSS_SELECTOR, ".oxd-table-body .oxd-table-row")
    NO_RECORDS_MSG    = (By.CSS_SELECTOR, ".oxd-text.oxd-text--p.oxd-text--toast-message.oxd-toast-content-text")

    # --- Success Toast ---
    TOAST_MESSAGE = (By.CSS_SELECTOR, ".oxd-text.oxd-text--p.oxd-text--toast-message.oxd-toast-content-text")

    # ── Navigation ────────────────────────────────────────────────────────────

    def navigate_to_add_employee(self):
        self.click(self.PIM_MENU)
        self.click(self.ADD_EMPLOYEE_MENU)
        return self

    def navigate_to_employee_list(self):
        self.click(self.PIM_MENU)
        self.click(self.EMPLOYEE_LIST_MENU)
        return self

    # ── Employee ID helpers ───────────────────────────────────────────────────

    def _generate_random_id(self):
        """Generate a random 6-digit Employee ID unlikely to collide."""
        return str(random.randint(100000, 999999))

    def _set_employee_id(self, emp_id):
        """Clear the Employee ID field and type the given ID."""
        id_field = self.find(self.EMPLOYEE_ID_FIELD)
        # id_field.clear()
        ActionChains(self.driver).key_down(Keys.CONTROL).send_keys('a').key_up(Keys.CONTROL).send_keys(Keys.DELETE).perform()
        id_field.send_keys(emp_id)

    def _is_duplicate_id_error_shown(self):
        """
        Explicitly wait up to DUPLICATE_ID_WAIT seconds for the
        'already exists' error message to appear under the ID field.

        Returns True  → duplicate error appeared  → need a new ID
        Returns False → no error within timeout   → save was accepted
        """
        try:
            short_wait = WebDriverWait(self.driver, DUPLICATE_ID_WAIT)
            short_wait.until(EC.visibility_of_element_located(self.DUPLICATE_ID_ERROR))
            error_text = self.driver.find_element(*self.DUPLICATE_ID_ERROR).text
            return True
        except TimeoutException:
            # No error appeared within the wait window — ID was accepted
            return False

    # ── Core add_employee with retry logic ────────────────────────────────────

    def add_employee(self, first_name, middle_name, last_name):
        """
        Fill the Add Employee form and handle duplicate Employee ID gracefully.

        Flow:
          1. Fill name fields.
          2. Read the auto-generated Employee ID.
          3. Click Save.
          4. Wait briefly for a duplicate-ID error message.
               → Error shown?  Replace ID with a random number and retry Save.
               → No error?     Wait for profile page redirect — done.
          5. Repeat up to MAX_ID_RETRIES times before raising an exception.

        Returns the final accepted Employee ID.
        """
        self.navigate_to_add_employee()

        # Fill name fields (these never change across retries)
        self.type_text(self.FIRST_NAME_INPUT, first_name)
        self.type_text(self.MIDDLE_NAME_INPUT, middle_name)
        self.type_text(self.LAST_NAME_INPUT, last_name)

        # Read the auto-generated ID OrangeHRM pre-fills
        id_field = self.find(self.EMPLOYEE_ID_FIELD)
        employee_id = id_field.get_attribute("value")

        for attempt in range(1, MAX_ID_RETRIES + 1):
            self.click(self.SAVE_BUTTON)

            # ── Check: did a duplicate-ID error appear? ──────────────────────
            if self._is_duplicate_id_error_shown():
                # Generate a fresh random ID and overwrite the field
                employee_id = self._generate_random_id()
                self._set_employee_id(employee_id)
                # Loop back and try Save again

            else:
                # No duplicate error — wait for successful redirect
                try:
                    self.wait.until(EC.url_contains("viewPersonalDetails"))
                    time.sleep(1)
                    return employee_id
                except TimeoutException:
                    raise RuntimeError(
                        f"Save clicked and no duplicate error shown, but profile "
                        f"page never loaded. Check for an unexpected validation error."
                    )

        raise RuntimeError(
            f"Failed to create employee after {MAX_ID_RETRIES} attempts. "
            f"All generated IDs were duplicates or another error occurred."
        )

    # ── Search helpers ────────────────────────────────────────────────────────

    def search_employee_by_name(self, first_name):
        self.navigate_to_employee_list()
        time.sleep(1)
        self.type_text(self.SEARCH_FIRST_NAME, first_name)
        self.click(self.SEARCH_BUTTON)
        time.sleep(1.5)

    def search_employee_by_id(self, employee_id):
        self.navigate_to_employee_list()
        time.sleep(1)
        self.type_text(self.SEARCH_EMP_ID, employee_id)
        self.click(self.SEARCH_BUTTON)
        time.sleep(1.5)

    def get_search_result_count(self):
        try:
            wait = WebDriverWait(self.driver, 10)
            rows = wait.until(EC.visibility_of_all_elements_located(self.SEARCH_RESULTS))
            # rows = self.driver.find_elements(*self.SEARCH_RESULTS)
            return len(rows)
        except Exception:
            return 0

    def is_no_records_found(self):
        return self.is_visible(self.NO_RECORDS_MSG)

    def is_employee_in_results(self, name_fragment):
        wait = WebDriverWait(self.driver, 10)
        rows = wait.until(EC.visibility_of_all_elements_located(self.SEARCH_RESULTS))
        # rows = self.driver.find_elements(*self.SEARCH_RESULTS)
        for row in rows:
            if name_fragment.lower() in row.text.lower():
                return True
        return False