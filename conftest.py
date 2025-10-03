
# conftest.py

import pytest
from selenium import webdriver

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