# pages/login_page.py

from selenium.webdriver.common.by import By

class LoginPage:
    """
    Page Object for the login page.
    """

    def __init__(self, driver):
        self.driver = driver

        # Locators
        self.username_input = (By.ID, "email")
        self.password_input = (By.ID, "password")
        self.login_button = (By.CSS_SELECTOR, ".btn-primary")
        self.error_message = (By.CSS_SELECTOR, ".invalid-feedback")
        self.initial_cash = (By.NAME, "cantidad")
        self.cash_button = (By.CSS_SELECTOR, ".btn-primary")
        self.driver.implicitly_wait(5)

    def load(self, base_url):
        """
        Navigate to the login page.
        """
        self.driver.get(base_url)

    def login(self, username, password):
        """
        Fill in username and password and submit the form.
        """
        self.driver.find_element(*self.username_input).clear()
        self.driver.find_element(*self.username_input).send_keys(username)
        self.driver.find_element(*self.password_input).clear()
        self.driver.find_element(*self.password_input).send_keys(password)
        self.driver.find_element(*self.login_button).click()

    def get_error_message(self):
        """
        Get error message if login fails.
        """
        return self.driver.find_element(*self.error_message).text
    
    def set_initial_cash(self, cash):
        """
        Set the initial cash.
        """
        self.driver.find_element(*self.initial_cash).clear()
        self.driver.find_element(*self.initial_cash).send_keys(cash)
        self.driver.find_element(*self.cash_button).click()