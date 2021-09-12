from product import Product
import requests
from bs4 import BeautifulSoup
from requests.utils import requote_uri

def main():
    search = "televizoare"
    products = {}
    i = 0
    with requests.Session() as session:
        store = "Altex"
        headers = {'User-Agent': "Mozilla/5.0 (Windows NT 5.2) AppleWebKit/5360 (KHTML, like Gecko) Chrome/39.0.837.0 Mobile Safari/5360"}
        response = session.get(requote_uri(f"https://altex.ro/cauta/?q={search}"), headers = headers, timeout=5)
        content = response._content  #response.text
        page = BeautifulSoup(content, "html.parser")
        print(page)
        products_grid = page.find("ul", {"class": "Products--grid"})
        items = products_grid.findAll("li", {"class": "Products-item"})
        for item in items:
            item_name = item.find("a", {"class": "Product-name"})["title"]
            item_price = item.find("span", {"class":"Price-int"}).text + " Lei"
            item_link = item.find("a", {"class": "Product-name"})["href"]
            products[i] = Product(item_name, item_price, item_link, store).to_dict()
            i += 1
    print(products)

if __name__ == "__main__":
    main()
