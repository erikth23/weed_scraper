import time
import logging
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

product_css_selector = 'div[class*="product-list-item__Container"]'
brand_css_selector = 'span[class*="Brand"]'
name_css_selector = 'span[class*="Name"]'
price_tile_selector = 'button[class*="clickable"]'
label_selector = 'span[class*="Label"]'
price_selector = 'span[class*="Price"]'
pagination_div_selector = 'div[class*="PaginationControlsContainer"]'
hyphen = '-'
next = "next"

class c21_scraper:

    def __init__(self, file_writer):
        options = Options()
        options.headless = True

        self.driver = webdriver.Chrome(executable_path="/Users/erikth/chromedriver", options=options)
        self.file_writer = file_writer



    def load_page(self, url):
        self.driver.get(url)
        time.sleep(5)

        scroll_height = self.driver.execute_script("return document.body.scrollHeight")
        script = "window.scrollTo({top: %s, left: 0, behavior: 'smooth'})"%(scroll_height)
        
        self.driver.execute_script(script)
        time.sleep(2)
        self.driver.execute_script(script)


    def extract_products(self, url):
        self.load_page(url)

        cannabis_elements = self.driver.find_elements(By.CSS_SELECTOR, product_css_selector)
        cannabis_products = list(map(self.extract_product_data, cannabis_elements))

        try:
            is_disabled = self.driver.find_element(By.CSS_SELECTOR, 'button[aria-label*="next"').get_attribute("disabled")
        except NoSuchElementException:
            is_disabled = True

        return (cannabis_products, is_disabled)


    def extract_product_data(self, element):
        try:
            name = element.find_element(By.CSS_SELECTOR, name_css_selector).text
            price_elements = element.find_elements(By.CSS_SELECTOR, price_tile_selector)
        except NoSuchElementException:
            return None

        try:
            brand = element.find_element(By.CSS_SELECTOR, brand_css_selector).text
        except NoSuchElementException:
            logging.exception('No brand found', exc_info=False)
            if hyphen in name:
                brand = name.split(hyphen)[0].strip()
            else:
                brand = ""

        price_elements = list(map(self.extract_cost_data, price_elements))

        for price in price_elements:
            self.file_writer.write_row_to_file({
                        "brand": brand,
                        "name": name,
                        "label": price.get("label"),
                        "price": price.get("price")
                    })

        return {
            "name": name,
            "brand": brand,
            "price_elements": price_elements
        }



    def extract_cost_data(self, element):
        try:
            label = element.get_attribute("value")
            price = element.find_element(By.CSS_SELECTOR, price_selector).text
        except NoSuchElementException:
            return None

        return {
            "label":label,
            "price":price
        }


    def cleanup(self):
        self.file_writer.cleanup()
        self.driver.close()







# Old page extractor
#
# def extract_products_from_page(driver, url):
#     driver.get(url)
#     time.sleep(5)

#     scroll_height = driver.execute_script("return document.body.scrollHeight")
#     script = "window.scrollTo({top: %s, left: 0, behavior: 'smooth'})"%(scroll_height)
#     driver.execute_script(script)
#     time.sleep(2)
#     driver.execute_script(script)

#     cannabis_elements = driver.find_elements(By.CSS_SELECTOR, product_css_selector)

#     cannabis_products = list(map(extract_product_data, cannabis_elements))

#     return cannabis_products