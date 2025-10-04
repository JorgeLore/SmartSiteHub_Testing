# tests/test_sales.py

import pytest
import os
import random
import pandas as pd
from pages.login_page import LoginPage
from pages.sales_page import SalesPage
from utils import sales_helpers
from config.settings import settings
from config.logger import get_logger

SMART_SITE_POS = settings.SMART_SITE_POS
USER = settings.USER
PASSWORD = settings.PASSWORD
INITIAL_CASH = 10000
TITLE_TEST = "ACCESORIO PARA CABELLO"

logger = get_logger("test_sales")

# Load CSV data once at module level
data = pd.read_csv("data/products.csv").to_dict(orient="records")
print(data)
# Generate random combinations of products for 10 test iterations
def get_random_product_sets(num_tests, products_per_test):
    product_sets = []
    for _ in range(num_tests):
        chosen = random.sample(data, k=products_per_test)
        product_sets.append(chosen)
    return product_sets

@pytest.fixture(scope="module")
def sales_page(driver):
    """
    Fixture to perform login first, then return InventoryPage object.
    """
    login_page = LoginPage(driver)
    login_page.load(SMART_SITE_POS)
    login_page.login(USER, PASSWORD)
    login_page.set_initial_cash(INITIAL_CASH)
    return SalesPage(driver)

@pytest.mark.sales
class TestSales:

    @pytest.mark.tc_sales_001
    @pytest.mark.parametrize("products", get_random_product_sets(num_tests=3, products_per_test=1))
    def test_add_single_item_and_validate_total(self, products, sales_page):
        """TC-SALES-001: Add single item to ticket and validate total."""
        logger.info("Running test case 1: Add single product")
        product = products[0]
        print(product["name"])
        print(product["price"])
        sales_page.start_new_ticket()
        sales_page.add_product_by_code(product["name"])
        total = sales_page.get_ticket_total()
        print(total)
        assert total == float(product["price"])

    @pytest.mark.tc_sales_002
    @pytest.mark.parametrize("products", get_random_product_sets(num_tests=3, products_per_test=3))
    def test_add_multiple_items_and_validate_total(self, products, sales_page):
        """TC-SALES-002: Add multiple items to ticket and validate summed total."""
        sales_page.start_new_ticket()
        expected_total = sales_helpers.add_items_and_get_total(sales_page, products)
        total = sales_page.get_ticket_total()
        assert total == expected_total, f"Expected total {expected_total}, got {total}"
    
    @pytest.mark.tc_sales_003
    @pytest.mark.parametrize("products", get_random_product_sets(num_tests=3, products_per_test=3))
    def test_remove_item_and_validate_total(self, products, sales_page):
        """TC-SALES-003: Remove item and ensure total updates correctly."""
        sales_page.start_new_ticket()
        expected_total = sales_helpers.add_items_and_get_total(sales_page, products)
        product_to_remove = random.choice(products)
        sales_page.remove_product_by_code(product_to_remove["name"])
        expected_total -= float(product_to_remove["price"])
        total = sales_page.get_ticket_total()
        assert total == expected_total, f"Expected total {expected_total}, got {total}"
        
    @pytest.mark.tc_sales_004
    def test_remove_current_ticket(self, sales_page):
        """TC-SALES-004: Ensure that the ticket is properly deleted"""
        sales_page.start_new_ticket()
        sales_page.start_new_ticket()
        sales_page.start_new_ticket()
        sales_page.remove_current_ticket()
        tickets = sales_page.get_ticket_list()
        assert all("Ticket 3" not in name for name in tickets), "Ticket no eliminado correctamente"

    @pytest.mark.tc_sales_005
    def test_cancel_remove_current_ticket(self, sales_page):
        """TC-SALES-005: Cancel a ticket deletion"""
        sales_page.start_new_ticket()
        sales_page.start_new_ticket()
        sales_page.start_new_ticket()
        sales_page.remove_current_ticket(False)
        tickets = sales_page.get_ticket_list()
        assert "Ticket 3" in tickets, "Ticket removed or deletion not proper canceled"
    
    @pytest.mark.tc_sales_006
    @pytest.mark.parametrize("products", get_random_product_sets(num_tests=1, products_per_test=3))
    def test_change_when_cash_is_used(self, products, sales_page):
        """TC-SALES-006: Pay with cash and ensure change is calculated correctly"""
        CASH_USED = 1000
        sales_page.start_new_ticket()
        expected_total = sales_helpers.add_items_and_get_total(sales_page, products)
        #total = sales_page.get_ticket_total()
        expected_change = CASH_USED - expected_total
        change = sales_page.pay_with_cash(CASH_USED)
        assert change == expected_change, "Incorrect change"
    
    @pytest.mark.tc_sales_007
    @pytest.mark.parametrize("products", get_random_product_sets(num_tests=1, products_per_test=3))
    def test_total_when_card_is_used(self, products, sales_page):
        """TC-SALES-007: Pay with card and ensure the total pay matches with the expected to pay"""
        REFERENCE = 123456789
        sales_page.start_new_ticket()
        expected_total = sales_helpers.add_items_and_get_total(sales_page, products)
        total_to_pay = sales_page.pay_with_card(REFERENCE)
        assert expected_total == total_to_pay, "Mismatch with the total to pay"
        
    @pytest.mark.tc_sales_008
    @pytest.mark.parametrize("products", get_random_product_sets(num_tests=1, products_per_test=3))
    def test_total_when_mix_payment_with_cash(self, products, sales_page):
        """TC-SALES-008: Mix payment. Ensure correctly amount to pay with cash and card."""
        CASH_USED = 1000
        sales_page.start_new_ticket()
        [print(f"{product} \n") for product in products]
        expected_total = sales_helpers.add_items_and_get_total(sales_page, products)
        expected_change = CASH_USED - expected_total*0.8 #Multiplied by 0.8 for generate remaining card 
        expected_remaining_card = expected_total*0.2
        change, remaining_card = sales_page.mix_payment_cash(CASH_USED)
        print(f"{change} vs {expected_change}")
        print(f"{remaining_card} vs {expected_remaining_card}")
        sales_page.take_page_screenshot("./logs/tc_sales_008/screenshot.png")
        assert round(expected_change, 1) == round(change, 1), "Mismatch with the change"
        assert round(expected_remaining_card, 1) == round(remaining_card, 1), "Mismatch with the remaining card"