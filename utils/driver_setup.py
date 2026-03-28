from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from utils.config import IMPLICIT_WAIT


def get_driver(headless=False):
    """
    Initialize and return a Chrome WebDriver instance.
    Set headless=True for CI/CD environments.
    """
    options = Options()

    if headless:
        options.add_argument("--headless=new")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")

    options.add_argument("--start-maximized")
    options.add_argument("--disable-notifications")
    options.add_argument("--disable-popup-blocking")

    driver = webdriver.Chrome(options=options)
    return driver