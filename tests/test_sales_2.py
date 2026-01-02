"""
Sales Module Test Cases
=======================
Automated UI test cases for the Sales module in Smart Site POS.
Each test validates a different functionality in the ticket and payment workflow.

Author: Jorge Lorenzo
"""

import pytest
import random
import pandas as pd
from pages.login_page import LoginPage
from pages.sales_page import SalesPage
from services.sales_service import SalesService
from config.settings import settings
from config.logger import get_logger

# ---------------------- Global Test Configuration ---------------------- #

SMART_SITE_POS = settings.SMART_SITE_POS
USER = settings.USER
PASSWORD = settings.PASSWORD
INITIAL_CASH = 10000
logger = get_logger("test_sales")

# Load CSV data with product info (executed once per module)
data = pd.read_csv("data/products.csv").to_dict(orient="records")

def get_random_product_sets(num_tests: int, products_per_test: int):
    """
    Generate random product combinations for test parametrization.
    Args:
        num_tests: Number of test iterations to generate.
        products_per_test: Number of products per iteration.
    Returns:
        List of product combinations.
    """
    return [random.sample(data, k=products_per_test) for _ in range(num_tests)]

# ---------------------- Pytest Fixtures ---------------------- #

@pytest.fixture(scope="module")
def sales_page(driver):
    """
    Perform login and initialize the SalesPage.
    Executed once per module to reduce overhead.
    """
    login_page = LoginPage(driver)
    login_page.load(SMART_SITE_POS)
    login_page.login(USER, PASSWORD)
    login_page.set_initial_cash(INITIAL_CASH)
    return SalesPage(driver)

# ---------------------- Sales Test Cases ---------------------- #

@pytest.mark.sales
class TestSales:

    @pytest.mark.tc_sales_001
    @pytest.mark.parametrize("products", get_random_product_sets(3, 1))
    def test_add_single_item_and_validate_total(self, products, sales_page):
        """TC-SALES-001: Add a single product and validate total."""
        product = products[0]
        logger.info(f"Executing TC-SALES-001 with product: {product['name']}")
        sales_page.start_new_ticket()
        sales_page.add_product_by_code(product["name"])
        total = sales_page.get_ticket_total()
        assert total == float(product["price"]), f"Expected {product['price']}, got {total}"

    @pytest.mark.tc_sales_002
    @pytest.mark.parametrize("products", get_random_product_sets(3, 3))
    def test_add_multiple_items_and_validate_total(self, products, sales_page):
        """TC-SALES-002: Add multiple products and validate total sum."""
        sales_page.start_new_ticket()
        expected_total = SalesService.add_items_and_get_expected_total(sales_page, products)
        total = sales_page.get_ticket_total()
        assert total == expected_total, f"Expected {expected_total}, got {total}"

    @pytest.mark.tc_sales_003
    @pytest.mark.parametrize("products", get_random_product_sets(3, 3))
    def test_remove_item_and_validate_total(self, products, sales_page):
        """TC-SALES-003: Remove one product and verify total is updated."""
        sales_page.start_new_ticket()
        expected_total = SalesService.add_items_and_get_expected_total(sales_page, products)
        product_to_remove = random.choice(products)
        sales_page.remove_product_by_code(product_to_remove["name"])
        expected_total -= float(product_to_remove["price"])
        total = sales_page.get_ticket_total()
        assert total == expected_total, f"Expected {expected_total}, got {total}"

    @pytest.mark.tc_sales_004
    def test_remove_current_ticket(self, sales_page):
        """TC-SALES-004: Remove a ticket and confirm deletion."""
        sales_page.start_new_ticket()
        sales_page.start_new_ticket()
        current_ticket = sales_page.get_ticket_id()
        sales_page.remove_current_ticket()
        tickets = sales_page.get_ticket_list()
        assert all(f"Ticket {current_ticket}" not in name for name in tickets), "Ticket was not deleted correctly"

    @pytest.mark.tc_sales_005
    def test_cancel_remove_current_ticket(self, sales_page):
        """TC-SALES-005: Cancel a ticket deletion and confirm ticket still exists."""
        sales_page.start_new_ticket()
        sales_page.start_new_ticket()
        current_ticket = sales_page.get_ticket_id()
        sales_page.remove_current_ticket(confirm=False)
        tickets = sales_page.get_ticket_list()
        assert f"Ticket {current_ticket}" in tickets, "Ticket was deleted when cancellation was expected"

    @pytest.mark.tc_sales_006
    @pytest.mark.parametrize("products", get_random_product_sets(1, 3))
    def test_change_when_cash_is_used(self, products, sales_page):
        """TC-SALES-006: Pay with cash and verify change is correct."""
        CASH_USED = 1000
        sales_page.start_new_ticket()
        expected_total = SalesService.add_items_and_get_expected_total(sales_page, products)
        expected_change = CASH_USED - expected_total
        change = sales_page.pay_with_cash(CASH_USED)
        assert change == expected_change, f"Expected change {expected_change}, got {change}"

    @pytest.mark.tc_sales_007
    @pytest.mark.parametrize("products", get_random_product_sets(1, 3))
    def test_total_when_card_is_used(self, products, sales_page):
        """TC-SALES-007: Pay with card and validate total matches."""
        REFERENCE = 123456789
        sales_page.start_new_ticket()
        expected_total = SalesService.add_items_and_get_expected_total(sales_page, products)
        total_to_pay = sales_page.pay_with_card(REFERENCE)
        assert expected_total == total_to_pay, f"Expected {expected_total}, got {total_to_pay}"

    @pytest.mark.tc_sales_008
    @pytest.mark.parametrize("products", get_random_product_sets(1, 3))
    def test_total_when_mix_payment_with_cash(self, products, sales_page):
        """TC-SALES-008: Pay with cash + card (mixed payment) and validate balances."""
        CASH_USED = 1000
        sales_page.start_new_ticket()

        expected_total = SalesService.add_items_and_get_expected_total(sales_page, products)
        expected_change = CASH_USED - expected_total * 0.8
        expected_remaining_card = expected_total * 0.2

        change, remaining_card = sales_page.mix_payment_cash(CASH_USED)

        assert round(expected_change, 1) == round(change, 1), "Mismatch in cash change"
        assert round(expected_remaining_card, 1) == round(remaining_card, 1), "Mismatch in remaining card payment"