# pages/inventory_page.py

from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

class InventoryPage:
    """
    Page Object for the inventory management page.
    Encapsulates locators and actions to interact with the inventory.
    """

    def __init__(self, driver):
        self.driver = driver
        
        # Go to inventory page
        self.inventory_btn = (By.LINK_TEXT, "Inventario")
        self.driver.find_element(*self.inventory_btn).click()
        
        # Locators for Inventario pages
        self.inventory_report_btn = (By.LINK_TEXT, "Reporte de inventario")
        self.inventory_title = (By.CLASS_NAME, "size-titulo-seccion")
        '''
        self.add_product_btn = (By.ID, "add-product-btn")
        self.name_input = (By.ID, "product-name")
        self.price_input = (By.ID, "product-price")
        self.code_input = (By.ID, "product-code")
        self.stock_input = (By.ID, "product-stock")
        self.save_btn = (By.ID, "save-product")
        self.error_message = (By.ID, "error-message")
        self.search_box = (By.ID, "search-box")
        self.product_list_items = (By.CSS_SELECTOR, ".product-list .product-item"
        '''
        
    def inventory_report(self):
        self.driver.find_element(*self.inventory_report_btn).click()
        return self.driver.find_element(*self.inventory_title).text

'''
    def add_product(self, name, price, code, stock):
        """Add a new product to the inventory."""
        self.driver.find_element(*self.add_product_btn).click()
        self.driver.find_element(*self.name_input).clear()
        self.driver.find_element(*self.name_input).send_keys(name)
        self.driver.find_element(*self.price_input).clear()
        self.driver.find_element(*self.price_input).send_keys(price)
        self.driver.find_element(*self.code_input).clear()
        self.driver.find_element(*self.code_input).send_keys(code)
        self.driver.find_element(*self.stock_input).clear()
        self.driver.find_element(*self.stock_input).send_keys(stock)
        self.driver.find_element(*self.save_btn).click()

    def get_error_message(self):
        """Return the validation or business rule error message."""
        return self.driver.find_element(*self.error_message).text

    def search_product(self, search_term):
        """Search for products by name or partial name and return their text."""
        search = self.driver.find_element(*self.search_box)
        search.clear()
        search.send_keys(search_term)
        search.send_keys(Keys.RETURN)
        products = self.driver.find_elements(*self.product_list_items)
        return [p.text for p in products]

    def is_product_in_list(self, product_name):
        """Check if a product appears in the product list."""
        products = self.driver.find_elements(*self.product_list_items)
        return any(product_name in p.text for p in products)
'''