# locators/sales_locators.py
from selenium.webdriver.common.by import By

class SalesLocators:
    """Locators for Sales Page elements."""

    # Ticket buttons
    pending_tickets_btn = (By.ID, "nuevoTicketContenido0-tab")
    new_ticket_btn = (By.CSS_SELECTOR, ".feather-plus-circle")
    ticket_name = (By.CSS_SELECTOR, ".nav-link.active")
    all_tickets = (By.CSS_SELECTOR, ".nav-link")

    # Product management
    remove_product_btn = (By.XPATH, '//img[@onclick="eliminarProductoTicketNormalActual(this);"]')
    products_on_ticket = (By.CSS_SELECTOR, ".widget-list-item-description-title")

    # Ticket removal confirmation
    remove_ticket_confirm = (By.CSS_SELECTOR, ".swal2-confirm")
    remove_ticket_cancel = (By.CSS_SELECTOR, ".swal2-cancel")

    # Payments
    payment_with_cash = (By.ID, "divEfectivoTicketNormal")
    payment_with_card = (By.ID, "divTarjetaTicketNormal")
    payment_with_cash_and_card = (By.ID, "divMixtoTicketNormal")
    client_cash_input = (By.ID, "efectivoCliente")
    total_cash_input = (By.ID, "enEfectivo")
    change = (By.ID, "cambio")
    reference_card_input = (By.ID, "referenciaTarjeta")
    total_price_card = (By.ID, "totalTarjeta")
    in_card = (By.ID, "enTarjeta")
    remaining_amount = (By.ID, "totalRestante")
    total_to_pay = (By.ID, "totalPagarH2ModalTicketNormal")

    # --- Dynamic locators ---
    @staticmethod
    def product_input(ticket_id: str):
        """Return locator for product input field based on ticket ID."""
        return (By.ID, f"buscadorProductos{ticket_id}")

    @staticmethod
    def add_product_btn(ticket_id: str):
        """Return locator for product add button based on ticket ID."""
        return (By.XPATH, f'//*[@id="listaProductosBusqueda{ticket_id}"]/div')

    @staticmethod
    def total_ticket_price(ticket_id: str):
        """Return locator for total ticket price label."""
        return (By.ID, f"totalPagarH2Normal{ticket_id}")

    @staticmethod
    def ticket_remove_icon(ticket_id: str):
        """Return locator for the remove ticket button inside the current ticket tab."""
        return (By.XPATH, f'//*[@id="nuevoTicketContenido{ticket_id}"]/div/div[1]/div/div/div[3]/div[2]/div/div/div[2]/span')

    @staticmethod
    def pay_button(ticket_id: str):
        """Return locator for the pay button of the given ticket."""
        return (By.ID, f'botonParaCobrar-normal{ticket_id}')