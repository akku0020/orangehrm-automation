
from selenium.webdriver.common.by import By
from pages.base_page import BasePage
from utils.config import BASE_URL


class LoginPage(BasePage):
    """Page Object for the OrangeHRM Login page."""

    # --- Locators ---
    USERNAME_INPUT = (By.NAME, "username")
    PASSWORD_INPUT = (By.NAME, "password")
    LOGIN_BUTTON   = (By.CSS_SELECTOR, "button[type='submit']")
    ERROR_MESSAGE  = (By.CSS_SELECTOR, ".oxd-alert-content-text")
    DASHBOARD_HEADER = (By.CSS_SELECTOR, ".oxd-topbar-header-breadcrumb h6")
    REQUIRED_POPUP    = (By.XPATH, "//span[.='Required']")

    def open(self):
        """Navigate to the login page."""
        self.navigate_to(f"{BASE_URL}/web/index.php/auth/login")
        return self

    def enter_username(self, username):
        self.type_text(self.USERNAME_INPUT, username)
        return self

    def enter_password(self, password):
        self.type_text(self.PASSWORD_INPUT, password)
        return self

    def click_login(self):
        self.click(self.LOGIN_BUTTON)
        return self

    def login(self, username, password):
        """Full login flow: enter credentials and submit."""
        self.enter_username(username)
        self.enter_password(password)
        self.click_login()
        return self

    def get_error_message(self):
        """Return the login error message text."""
        return self.get_text(self.ERROR_MESSAGE)

    def is_dashboard_visible(self):
        """Return True if the Dashboard header is visible after login."""
        return self.is_visible(self.DASHBOARD_HEADER)

    def is_error_displayed(self):
        """Return True if an error alert is shown."""
        return self.is_visible(self.ERROR_MESSAGE)

    def is_required_popup_displayed(self):
        """Return True if required popup for empty field is displayed"""
        return self.is_visible(self.REQUIRED_POPUP)
