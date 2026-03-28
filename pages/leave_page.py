
import time

from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from pages.base_page import BasePage


class LeavePage(BasePage):
    """Page Object for the Leave module."""

    # --- Navigation ---
    LEAVE_MENU        = (By.XPATH, "//span[text()='Leave']")
    APPLY_LEAVE_MENU  = (By.XPATH, "//a[text()='Apply']")

    # --- Apply Leave Form ---
    LEAVE_TYPE_DROPDOWN = (By.XPATH, "//label[text()='Leave Type']/following::div[contains(@class,'oxd-select-text')][1]")
    LEAVE_TYPE_OPTION   = (By.XPATH, "//div[@class='oxd-select-option']//span[contains(.,'CAN - Personal')]")
    FROM_DATE_INPUT     = (By.XPATH, "//label[text()='From Date']/following::input[1]")
    TO_DATE_INPUT       = (By.XPATH, "//label[text()='To Date']/following::input[1]")
    COMMENT_INPUT       = (By.XPATH, "//label[text()='Comments']/following::textarea[1]")
    APPLY_BUTTON        = (By.CSS_SELECTOR, "button[type='submit']")

    # --- Success / Confirmation ---
    SUCCESS_TOAST       = (By.XPATH, "//div[contains(@class,'oxd-toast--success')]")
    TOAST_TITLE         = (By.CSS_SELECTOR, ".oxd-text.oxd-text--p.oxd-text--toast-title.oxd-toast-content-text")
    TOAST_MESSAGE       = (By.CSS_SELECTOR, ".oxd-text.oxd-text--p.oxd-text--toast-message.oxd-toast-content-text")

    def navigate_to_apply(self):
        """Go to Leave > Apply."""
        self.click(self.LEAVE_MENU)
        self.click(self.APPLY_LEAVE_MENU)
        time.sleep(1)
        return self

    def select_leave_type(self):
        """Click the Leave Type dropdown and select the first available option."""
        self.click(self.LEAVE_TYPE_DROPDOWN)
        time.sleep(0.5)
        self.click(self.LEAVE_TYPE_OPTION)

    def set_date(self, locator, date_str):
        """
        Clear date input and enter a date in MM/DD/YYYY format.
        date_str format expected: 'YYYY-MM-DD'
        """

        element = self.find(locator)
        self.click(element)
        ActionChains(self.driver).key_down(Keys.CONTROL).send_keys('a').key_up(Keys.CONTROL).send_keys(Keys.DELETE).perform()
        element.send_keys(date_str)
        element.send_keys(Keys.TAB)
        time.sleep(0.3)

    def apply_leave(self, from_date, to_date, comment):
        """Fill and submit the leave application form."""
        self.navigate_to_apply()
        self.select_leave_type()
        self.set_date(self.FROM_DATE_INPUT, from_date)
        self.set_date(self.TO_DATE_INPUT, to_date)
        self.type_text(self.COMMENT_INPUT, comment)
        self.click(self.APPLY_BUTTON)
        time.sleep(1.5)

    def is_success_toast_visible(self):
        """Return True if the green success toast notification is shown."""
        return self.is_visible(self.SUCCESS_TOAST)

    def get_toast_message(self):
        """Return the text of the success toast."""
        try:
            return self.get_text(self.TOAST_MESSAGE)
        except Exception:
            return ""