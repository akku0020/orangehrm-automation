"""
Scenario 5: Create a Buzz post and verify it appears on the Buzz feed.
"""

import pytest
from pages.login_page import LoginPage
from pages.buzz_page import BuzzPage
from utils.driver_setup import get_driver
from utils.config import VALID_USERNAME, VALID_PASSWORD, BUZZ_POST


class TestBuzz:

    @pytest.fixture(autouse=True)
    def setup_teardown(self):
        """Log in before each test and quit driver after."""
        self.driver = get_driver()

        login_page = LoginPage(self.driver)
        login_page.open()
        login_page.login(VALID_USERNAME, VALID_PASSWORD)
        assert login_page.is_dashboard_visible(), "Login failed — cannot run Buzz tests."

        self.buzz = BuzzPage(self.driver)
        yield
        self.driver.quit()

    def test_create_buzz_post_appears_in_feed(self):
        """
        TC-011: Create a Buzz post and verify it appears at the top of the feed.
        """
        message = BUZZ_POST["message"]

        posted_message = self.buzz.create_post(message)
        is_in_feed = self.buzz.is_post_in_feed(posted_message)
        assert is_in_feed, \
            f"Post '{message[:50]}...' should appear in the Buzz feed after posting."

        print(f"\nTC-011 PASSED: Buzz post created and found in feed.")
