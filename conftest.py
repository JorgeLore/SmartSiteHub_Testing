
# conftest.py
import os
import pytest
import allure
from datetime import datetime
from selenium import webdriver

SCREENSHOTS_DIR = "logs/screenshots"

@pytest.fixture(scope="session")
def driver():
    """
    Fixture to initialize and quit the WebDriver.
    This fixture has 'session' scope, so it runs once per test session.
    """
    options = webdriver.ChromeOptions()
    # options.add_argument("--headless=new")  # Remove if you want to see the browser
    driver = webdriver.Chrome(options=options)
    driver.maximize_window()
    driver.implicitly_wait(10)
    yield driver
    driver.quit()

@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """Take screenshot on test failure and attach it to Allure."""
    outcome = yield
    report = outcome.get_result()

    if report.when == "call" and report.failed:
        driver = item.funcargs.get("driver", None)
        if driver:
            os.makedirs(SCREENSHOTS_DIR, exist_ok=True)

            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            test_name = item.name
            screenshot_path = os.path.join(
                SCREENSHOTS_DIR, f"{test_name}_{timestamp}.png"
            )

            driver.save_screenshot(screenshot_path)

            with open(screenshot_path, "rb") as image:
                allure.attach(
                    image.read(),
                    name=f"Screenshot - {test_name}",
                    attachment_type=allure.attachment_type.PNG
                )