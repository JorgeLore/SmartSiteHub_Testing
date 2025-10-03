def add_items_and_get_total(sales_page, products):
    expected_total = 0
    for product in products:
            sales_page.add_product_by_code(product["name"])
            expected_total += float(product["price"])
    return expected_total