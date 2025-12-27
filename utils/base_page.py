# utils/base_page.py
import os
import logging
from datetime import datetime
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

logger = logging.getLogger(__name__)

class BasePage:
    """Base class providing reusable Selenium utilities for all page objects."""

    def __init__(self, driver, timeout: int = 10):
        self.driver = driver
        self.timeout = timeout

    # ---------- Wait & interaction utilities ----------

    def wait_and_click(self, locator):
        """Wait until an element is clickable and click it."""
        element = WebDriverWait(self.driver, self.timeout).until(
            EC.element_to_be_clickable(locator)
        )
        element.click()
        logger.debug(f"Clicked element: {locator}")
        return element

    def write_input(self, locator, value, clear=True):
        """Wait until input is visible, optionally clear it, then send keys."""
        element = WebDriverWait(self.driver, self.timeout).until(
            EC.presence_of_element_located(locator)
        )
        if clear:
            element.clear()
        element.send_keys(value)
        logger.debug(f"Input written into {locator}: {value}")
        return element

    def get_text(self, locator) -> str:
        """Wait until element is visible and return its text."""
        element = WebDriverWait(self.driver, self.timeout).until(
            EC.presence_of_element_located(locator)
        )
        text = element.text.strip()
        logger.debug(f"Text extracted from {locator}: {text}")
        return text

    def get_value(self, locator) -> str:
        """Return the 'value' attribute of a given element."""
        value = self.driver.find_element(*locator).get_attribute("value")
        logger.debug(f"Value extracted from {locator}: {value}")
        return value

    # ---------- Screenshot utilities ----------

    def take_screenshot(self, path: str) -> str:
        """
        Save a screenshot of the current page.
        Creates directories automatically if needed.
        If given a folder path, it will generate a unique timestamped filename.
        """
        os.makedirs(os.path.dirname(path), exist_ok=True)
        if os.path.isdir(path):
            filename = f"screenshot_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png"
            path = os.path.join(path, filename)

        self.driver.save_screenshot(path)
        logger.info(f"Screenshot saved at: {path}")
        return path

    # ---------- Utility methods ----------

    def wait_for_element(self, locator):
        """Wait for an element to be present in the DOM."""
        return WebDriverWait(self.driver, self.timeout).until(
            EC.presence_of_element_located(locator)
        )

    def element_exists(self, locator) -> bool:
        """Check if element exists (returns True/False)."""
        try:
            self.driver.find_element(*locator)
            return True
        except Exception:
            return False