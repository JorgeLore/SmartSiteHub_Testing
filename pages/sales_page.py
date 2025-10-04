# pages/sales_page.py
from config.logger import get_logger
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from locators.sales_locators import SalesLocators
from selenium.webdriver.common.by import By
import time
import os

logger = get_logger(__name__)

class SalesPage:
    """Page Object for Sales Page.
    Contains methods to interact with tickets, products, and payment options.
    """

    def __init__(self, driver, timeout: int = 10):
        self.driver = driver
        self.timeout = timeout

    # ---------- Utility methods ----------

    def wait_and_click(self, locator):
        """Wait until element is clickable and then click it."""
        element = WebDriverWait(self.driver, self.timeout).until(
            EC.element_to_be_clickable(locator)
        )
        element.click()
        return element

    def write_input(self, locator, value, clear=True):
        """Write text into input field with optional clearing."""
        element = WebDriverWait(self.driver, self.timeout).until(
            EC.presence_of_element_located(locator)
        )
        if clear:
            element.clear()
        element.send_keys(value)
        return element

    def get_text(self, locator) -> str:
        """Return text from element."""
        element = WebDriverWait(self.driver, self.timeout).until(
            EC.presence_of_element_located(locator)
        )
        return element.text.strip()

    def get_value(self, locator) -> str:
        """Return 'value' attribute from element."""
        return self.driver.find_element(*locator).get_attribute("value")

    # ---------- Ticket actions ----------

    def start_new_ticket(self):
        """Create a new ticket."""
        self.wait_and_click(SalesLocators.new_ticket_btn)

    def get_ticket_id(self) -> str:
        """Return the current active ticket ID."""
        return self.get_text(SalesLocators.ticket_name).split(" ")[1]

    def remove_current_ticket(self, confirm=True):
        """Remove current ticket. Confirm or cancel based on 'confirm' flag."""
        ticket_id = self.get_ticket_id()
        self.wait_and_click(SalesLocators.ticket_remove_icon(ticket_id))
        if confirm:
            self.wait_and_click(SalesLocators.remove_ticket_confirm)
        else:
            self.wait_and_click(SalesLocators.remove_ticket_cancel)

    def get_ticket_list(self) -> list[str]:
        """Return all open tickets as a list of names."""
        tickets = self.driver.find_elements(*SalesLocators.all_tickets)
        return [ticket.text.strip() for ticket in tickets]

    # ---------- Product actions ----------

    def add_product_by_code(self, code: str):
        """Add a product to the ticket using its code."""
        ticket_id = self.get_ticket_id()
        input_box = self.write_input(SalesLocators.product_input(ticket_id), code)
        WebDriverWait(self.driver, self.timeout).until(
            EC.presence_of_all_elements_located(SalesLocators.add_product_btn(ticket_id))
        )
        time.sleep(2)
        #results = self.driver.find_elements_by_css_selector(".col-7")
        results = self.driver.find_elements(By.CSS_SELECTOR, ".col-7")
        for result in results:
            product_name = result.text.strip().split("\n")[0]
            if product_name == code:
                result.click()
                break
        logger.info(f"Product {code} added to ticket {ticket_id}")
        time.sleep(0.5)

    def remove_product_by_code(self, code: str):
        """Remove a product from ticket by its code name."""
        products = self.driver.find_elements(*SalesLocators.products_on_ticket)
        names = [item.text for item in products]
        logger.debug(names)
        try:
            idx = names.index(code)
            n = self.driver.find_elements(*SalesLocators.remove_product_btn)
            n_rm = len(n)
            logger.debug(n)
            logger.debug(n_rm)
            self.driver.find_elements(*SalesLocators.remove_product_btn)[idx].click()
            self.wait_and_click(SalesLocators.remove_ticket_confirm)
            logger.info(f"Product '{code}' removed from ticket.")
        except ValueError:
            logger.error(f"Product '{code}' not found in ticket.")
            raise

    def get_ticket_total(self) -> float:
        """Return total amount for current ticket."""
        time.sleep(0.5)
        ticket_id = self.get_ticket_id()
        logger.debug(f"ticket id={ticket_id}")
        total_text = self.get_text(SalesLocators.total_ticket_price(ticket_id))
        return float(total_text.split()[1])

    # ---------- Payment actions ----------

    def open_payment_modal(self):
        """Open the payment modal for the current ticket."""
        ticket_id = self.get_ticket_id()
        self.wait_and_click(SalesLocators.pay_button(ticket_id))

    def pay_with_cash(self, cash_used: float) -> float:
        """Pay ticket using cash. Returns change."""
        self.open_payment_modal()
        self.write_input(SalesLocators.client_cash_input, str(cash_used))
        return float(self.get_value(SalesLocators.change))

    def pay_with_card(self, reference_card: str) -> float:
        """Pay ticket using card. Returns total amount."""
        self.open_payment_modal()
        self.wait_and_click(SalesLocators.payment_with_card)
        self.write_input(SalesLocators.reference_card_input, reference_card)
        return float(self.get_value(SalesLocators.total_price_card))

    def mix_payment_cash(self, cash_used: float) -> tuple[float, float]:
        """Pay ticket using mixed payment (cash + card).
        Returns (change, remaining card amount).
        """
        self.open_payment_modal()
        self.wait_and_click(SalesLocators.payment_with_cash_and_card)
        total_to_pay = float(self.get_text(SalesLocators.total_to_pay).split()[1])
        total_cash = total_to_pay * 0.8  # assume 80% cash, 20% card
        self.write_input(SalesLocators.total_cash_input, str(total_cash))
        self.write_input(SalesLocators.client_cash_input, str(cash_used))
        change = float(self.get_value(SalesLocators.change))
        remaining_card = float(self.get_value(SalesLocators.in_card))
        return change, remaining_card

    # ---------- Misc ----------

    def take_page_screenshot(self, path: str):
        """Save a screenshot of the current page."""
        # Ensure directory exists
        os.makedirs(os.path.dirname(path), exist_ok=True)
        self.driver.save_screenshot(path)
