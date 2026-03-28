
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from utils.config import EXPLICIT_WAIT


class BasePage:
    """
    Base class for all Page Objects.
    Provides common reusable methods for WebDriver interactions.
    """

    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, EXPLICIT_WAIT)

    def find(self, locator):
        """Wait for element to be present and return it."""
        return self.wait.until(EC.presence_of_element_located(locator))

    def click(self, locator):
        """Wait for element to be clickable, then click."""
        element = self.wait.until(EC.element_to_be_clickable(locator))
        element.click()

    def type_text(self, locator, text):
        """Clear field and type text."""
        element = self.find(locator)
        element.clear()
        element.send_keys(text)

    def get_text(self, locator):
        """Return text content of an element."""
        return self.find(locator).text

    def is_visible(self, locator):
        """Return True if element is visible, False otherwise."""
        try:
            self.wait.until(EC.visibility_of_element_located(locator))
            return True
        except Exception:
            return False

    def wait_for_url_contains(self, partial_url):
        """Wait until the current URL contains a given substring."""
        self.wait.until(EC.url_contains(partial_url))

    def navigate_to(self, url):
        """Open a URL in the browser."""
        self.driver.get(url)