# pages/sales_page.py

from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time

class SalesPage:
    """Sales page with all functionalities"""
    
    def __init__(self, driver):
        self.driver = driver
        self.pending_tickets_btn = (By.ID, "nuevoTicketContenido0-tab")
        self.new_ticket_btn = (By.CSS_SELECTOR, ".feather-plus-circle")
        self.ticket_name = (By.CSS_SELECTOR, ".nav-link.active")
        self.all_tickets = (By.CSS_SELECTOR, ".nav-link")
        self.remove_product_btn = (By.CSS_SELECTOR, ".datosVista button[onclick*='eliminarProductoTicketNormalActual(this);']")
        self.products_on_ticket = (By.CSS_SELECTOR, ".widget-list-item-description-title")
        self.remove_ticket_confirm = (By.CSS_SELECTOR, ".swal2-confirm")
        self.remove_ticket_cancel = (By.CSS_SELECTOR, ".swal2-cancel")
        self.payment_with_cash = (By.ID, "divEfectivoTicketNormal")
        self.payment_with_card = (By.ID, "divTarjetaTicketNormal")
        self.payment_with_cash_and_card = (By.ID, "divMixtoTicketNormal")
        self.client_cash_input = (By.ID, "efectivoCliente")
        self.total_cash_input = (By.ID, "enEfectivo")
        self.change = (By.ID, "cambio")
        self.reference_card_input = (By.ID, "referenciaTarjeta")
        self.total_price_card = (By.ID, "totalTarjeta")
        self.in_card = (By.ID, "enTarjeta")
        self.remaining_ammount = (By.ID, "totalRestante")
        self.total_to_pay = (By.ID, "totalPagarH2ModalTicketNormal")
        

    def start_new_ticket(self):
        """Start a new ticket for sales"""
        self.driver.find_element(*self.new_ticket_btn).click()
        
    def get_ticket_id(self):
        """Get and return the number id of the current ticket"""
        return self.driver.find_element(*self.ticket_name).text.split(" ")[1]

    def add_product_by_code(self, code):
        """Add a product to the current ticket by its name code"""
        ticket_id = self.get_ticket_id()
        
        self.product_input = (By.ID, f"buscadorProductos{ticket_id}")
        self.add_product_btn = (By.XPATH, f'//*[@id="listaProductosBusqueda{ticket_id}"]/div')
        
        input_box = self.driver.find_element(*self.product_input)
        input_box.clear()
        input_box.send_keys(code)
        time.sleep(2)
        resultados = self.driver.find_elements(By.CSS_SELECTOR, ".col-7")
        for r in resultados:
            try:
                nombre = r.text.strip().split('\n')[0]
                if nombre == code:
                    r.click()
                    break
            except Exception as e:
                print(f"Error al procesar elemento: {e}")
        time.sleep(2) 

    def get_ticket_total(self):
        """Get and return the total price of the current ticket."""
        ticket_id = self.get_ticket_id()
        print(ticket_id)
        self.total_text = (By.ID, f"totalPagarH2Normal{ticket_id}")
        return float(self.driver.find_element(*self.total_text).text.split()[1])
        
    def remove_product_by_code(self, code):
        """Remove a product from the current ticket by the name code."""
        products = self.driver.find_elements(*self.products_on_ticket)
        product_names = [item.text for item in products]
        print(product_names)
        
        try:
            indice = product_names.index(code)
            print(f"El índice de producto es: {indice}")
        except ValueError:
            print("El producto no se encuentra en la lista.")

        print(*self.remove_product_btn)
        test = self.driver.find_elements(*self.remove_product_btn)
        print(test)
        test[indice].click()
        self.driver.find_element(By.CLASS_NAME, value='swal2-confirm').click()
        time.sleep(2)
        
    def remove_current_ticket(self):
        """Remove the current ticket."""
        ticket_id = self.get_ticket_id()
        
        self.driver.find_element(By.XPATH, f'//*[@id="nuevoTicketContenido{ticket_id}"]/div/div[1]/div/div/div[3]/div[2]/div/div/div[2]/span').click()
        WebDriverWait(self.driver, 5).until(EC.element_to_be_clickable(self.remove_ticket_confirm)).click()
        
    def cancel_remove_current_ticket(self):
        """Cancel the remove of the current ticket"""
        ticket_id = self.get_ticket_id()
        
        self.driver.find_element(By.XPATH, f'//*[@id="nuevoTicketContenido{ticket_id}"]/div/div[1]/div/div/div[3]/div[2]/div/div/div[2]/span').click()
        WebDriverWait(self.driver, 5).until(EC.element_to_be_clickable(self.remove_ticket_cancel)).click()
        
    def get_ticket_list(self):
        """Return all current open tickets."""
        all_tickets = self.driver.find_elements(*self.all_tickets)
        all_tickets_names = []
        for ticket in all_tickets:
            print(ticket.text)
            all_tickets_names.append(ticket.text.strip())
        return all_tickets_names
    
    def pay_with_cash(self, cash_used):
        """"Choose to pay with cash and return the change."""
        ticket_id = self.get_ticket_id()
        self.driver.find_element(By.ID, f'botonParaCobrar-normal{ticket_id}').click()
        self.driver.find_element(*self.client_cash_input).send_keys(cash_used)
        change = self.driver.find_element(*self.change).get_attribute("value")
        return float(change)
    
    def pay_with_card(self, reference_card):
        """"Choose to pay with card, input reference and return total to p."""
        ticket_id = self.get_ticket_id()
        self.driver.find_element(By.ID, f'botonParaCobrar-normal{ticket_id}').click()
        self.driver.find_element(*self.payment_with_card).click()
        self.driver.find_element(*self.reference_card_input).send_keys(reference_card)
        total = self.driver.find_element(*self.total_price_card).get_attribute("value")
        return float(total)
    
    def mix_payment_cash(self, cash_used):
        """"Choose to pay with card, input reference and return total to p."""
        ticket_id = self.get_ticket_id()
        self.driver.find_element(By.ID, f'botonParaCobrar-normal{ticket_id}').click()
        self.driver.find_element(*self.payment_with_cash_and_card).click()
        total_cash = float(self.driver.find_element(*self.total_to_pay).text.split(' ')[1])*0.8
        self.driver.find_element(*self.total_cash_input).send_keys(total_cash)
        self.driver.find_element(*self.client_cash_input).clear()
        self.driver.find_element(*self.client_cash_input).send_keys(cash_used)
        change = self.driver.find_element(*self.change).get_attribute("value")
        remaining_card = self.driver.find_element(*self.in_card).get_attribute("value")
        time.sleep(5)
        return float(change), float(remaining_card)
    
    def take_page_screenshot(self, path):
        self.driver.save_screenshot(path)










    '''  
    def is_receipt_generated(self):
        return self.driver.find_element(*self.receipt_modal).is_displayed()
    '''