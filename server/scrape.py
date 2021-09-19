from product import Product
import requests
from bs4 import BeautifulSoup
from requests.utils import requote_uri
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions
from os.path import dirname, join

main_path = dirname(__file__)

def get_products(search):
    products = {}
    i = 0
    try:
        # emag
        with requests.Session() as session:
            store = "Emag"
            response = session.get(requote_uri(f"https://www.emag.ro/search/{search}/sort-priceasc"))
            content = response._content  #response.text
            page = BeautifulSoup(content, "html.parser")
            products_grid = page.find("div", {"id": "card_grid"})
            items = products_grid.findAll("div", {"class": "card-item js-product-data"})
            for item in items:
                item_name = item["data-name"]
                item_price = item.find("p", {"class": "product-new-price"}).text[:-6] + " Lei"
                if "de la" in item_price:
                    continue
                item_link = item.find("div", {"class":"card-heading"}).find("a")["href"]
                products[i] = Product(item_name, item_price, item_link, store).to_dict()
                i += 1

        # altex
        store = "Altex"
        options = Options()
        options.headless = True
        options.add_argument(f'user-agent={"Mozilla/5.0 (Windows NT 5.2) AppleWebKit/5360 (KHTML, like Gecko) Chrome/39.0.837.0 Mobile Safari/5360"}')
        path_geckodriver = "webdriver/chromedriver.exe"
        driver = webdriver.Chrome(chrome_options=options, executable_path=join(main_path, path_geckodriver))
        driver.get(requote_uri(f"https://altex.ro/cauta/filtru/order/price/dir/asc/?q={search}"))
        # time.sleep(2)
        WebDriverWait(driver, 2).until(
            expected_conditions.visibility_of_element_located(
                (By.CLASS_NAME, 'Products--grid')
            )
        )
        content = driver.page_source
        driver.quit()
        page = BeautifulSoup(content, "html.parser")
        products_grid = page.find("ul", {"class": "Products--grid"})
        items = products_grid.findAll("li", {"class": "Products-item"})
        for item in items:
            item_name = item.find("a", {"class": "Product-name"})["title"]
            item_price = item.find("span", {"class":"Price-int"}).text + " Lei"
            item_link = item.find("a", {"class": "Product-name"})["href"]
            products[i] = Product(item_name, item_price, item_link, store).to_dict()
            i += 1
        
        #cel
        store = "CEL"
        options = Options()
        options.headless = True
        options.add_argument(f'user-agent={"Mozilla/5.0 (Windows NT 5.2) AppleWebKit/5360 (KHTML, like Gecko) Chrome/39.0.837.0 Mobile Safari/5360"}')
        path_geckodriver = "webdriver/chromedriver.exe"
        driver = webdriver.Chrome(chrome_options=options, executable_path=join(main_path, path_geckodriver))
        driver.get(requote_uri(f"https://www.cel.ro/cauta/{search}/0c-1"))
        # time.sleep(2)
        WebDriverWait(driver, 2).until(
            expected_conditions.visibility_of_element_located(
                (By.CLASS_NAME, 'productlisting')
            )
        )
        content = driver.page_source
        driver.quit()
        page = BeautifulSoup(content, "html.parser")
        products_grid = page.find("div", {"class": "productlisting"})
        items = products_grid.findAll("div", {"class": "product_data"})
        for item in items:
            item_name = item.find("a", {"class": "productListing-data-b"}).find("span").text
            item_price = item.find("div", {"class" : "pret_n"}).find("b", {"productprice": "1"}).text + " Lei"
            item_link = item.find("a", {"class": "productListing-data-b"})["href"]
            if "https://www.cel.ro" not in item_link:
                item_link = "https://www.cel.ro" + item_link
            products[i] = Product(item_name, item_price, item_link, store).to_dict()
            i += 1
    except Exception as e:
        print(e)
        return None
    return products
