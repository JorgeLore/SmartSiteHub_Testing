# services/sales_service.py

class SalesService:
    """
    Business-level actions for Sales flows.
    Combines multiple page actions into reusable logic.
    """

    @staticmethod
    def add_items_and_get_expected_total(sales_page, products) -> float:
        """
        Add multiple products to the current ticket and calculate expected total.

        Args:
            sales_page (SalesPage): Instance of SalesPage.
            products (list): List of products with 'name' and 'price'.

        Returns:
            float: Expected total price after adding all products.
        """
        expected_total = 0.0

        for product in products:
            sales_page.add_product_by_code(product["name"])
            expected_total += float(product["price"])

        return expected_total