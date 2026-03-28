import time
import logging

from selenium.common import StaleElementReferenceException, ElementNotInteractableException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from pages.base_page import BasePage

logger = logging.getLogger(__name__)


class BuzzPage(BasePage):
    """Page Object for the Buzz (social feed) module."""

    # --- Navigation ---
    BUZZ_MENU     = (By.XPATH, "//span[text()='Buzz']")

    # --- Post Creation ---
    POST_INPUT    = (By.XPATH, "//textarea[@placeholder=\"What's on your mind?\"]")
    SHARE_BUTTON  = (By.CSS_SELECTOR, "button[type='submit']")

    # --- Feed ---
    FEED_POSTS    = (By.CSS_SELECTOR, ".orangehrm-buzz-post-body-text")
    SUCCESS_TOAST = (By.XPATH, "//div[contains(@class,'oxd-toast--success')]")

    def navigate_to_buzz(self):
        """Go to the Buzz feed page and wait for the post input to be ready."""
        self.click(self.BUZZ_MENU)
        self.wait.until(EC.visibility_of_element_located(self.POST_INPUT))
        return self

    def _get_fresh_post_box(self):
        """Always fetch a fresh reference to avoid StaleElementReferenceException."""
        return self.wait.until(EC.presence_of_element_located(self.POST_INPUT))

    def _type_via_js(self, message):

        # Step 1 — Click to focus and trigger Vue's initial render
        post_box = self._get_fresh_post_box()
        self.driver.execute_script("arguments[0].click(); arguments[0].focus();", post_box)

        # Step 2 — Wait for Share button to appear (Vue re-render complete)
        self.wait.until(EC.element_to_be_clickable(self.SHARE_BUTTON))
        time.sleep(0.3)

        # Step 3 — Inject value and fire all events Vue needs to update v-model
        post_box = self._get_fresh_post_box()
        self.driver.execute_script("""
            var el = arguments[0];
            var text = arguments[1];

            // Set the native input value
            var nativeInputValueSetter = Object.getOwnPropertyDescriptor(
                window.HTMLTextAreaElement.prototype, 'value'
            ).set;
            nativeInputValueSetter.call(el, text);

            // Fire events so Vue's v-model picks up the change
            el.dispatchEvent(new Event('input',  { bubbles: true }));
            el.dispatchEvent(new Event('change', { bubbles: true }));
        """, post_box, message)

        time.sleep(0.3)

        # Step 4 — Verify value landed correctly
        post_box = self._get_fresh_post_box()
        actual = post_box.get_attribute("value")

        if actual != message:
            logger.warning(f"JS injection mismatch. Got: '{actual[:40]}'. Retrying with clipboard paste.")
            self._type_via_clipboard(message)
        else:
            logger.info(f"JS injection confirmed: '{actual[:40]}'")

    def _type_via_clipboard(self, message):
        """
        Fallback strategy: select-all + clipboard paste via JS execCommand.
        Used only if the primary JS injection fails.
        """
        post_box = self._get_fresh_post_box()
        self.driver.execute_script("""
            var el = arguments[0];
            el.focus();
            el.select();
            document.execCommand('selectAll');
            document.execCommand('delete');
        """, post_box)
        time.sleep(0.2)

        # Type as one atomic send_keys call (minimises re-render windows)
        for attempt in range(3):
            try:
                post_box = self._get_fresh_post_box()
                post_box.send_keys(message)
                time.sleep(0.3)
                actual = post_box.get_attribute("value")
                if actual == message:
                    logger.info("Clipboard fallback succeeded.")
                    return
            except (StaleElementReferenceException, ElementNotInteractableException) as e:
                logger.warning(f"Clipboard attempt {attempt + 1} failed: {e}. Retrying...")
                time.sleep(0.5)

        raise RuntimeError(f"Failed to type into Buzz post box after all retries. Message: '{message}'")

    def create_post(self, message):
        """
        Type a message in the Buzz post input and click Share.
        Returns the message text for verification.
        """
        self.navigate_to_buzz()

        # Use JS injection as the primary approach (immune to StaleElement)
        self._type_via_js(message)

        # Re-fetch Share button fresh before clicking
        share_btn = self.wait.until(EC.element_to_be_clickable(self.SHARE_BUTTON))
        self.driver.execute_script("arguments[0].click();", share_btn)

        # Wait for feed to update
        try:
            self.wait.until(EC.visibility_of_element_located(self.SUCCESS_TOAST))
            logger.info("Success toast confirmed.")
        except Exception:
            time.sleep(2)
            logger.info("No toast — proceeding to feed verification.")

        self.driver.refresh()

        return message

    def is_post_in_feed(self, message):
        """Return True if any post in the feed contains the given message text."""

        try:
            # posts = self.driver.find_elements(*self.FEED_POSTS)
            posts = self.wait.until(EC.visibility_of_all_elements_located(self.FEED_POSTS))
            for post in posts:
                if message[:30].lower() in post.text.lower():
                    return True
            return False
        except Exception:
            return False

    def is_success_toast_visible(self):
        return self.is_visible(self.SUCCESS_TOAST)