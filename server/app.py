from flask import Flask, request
from scrape import get_products

app = Flask(__name__)

@app.route('/')
def hello():
    search = request.args.get('search')
    if search is None:
        return ''
    products = get_products(search)
    if products is None:
        return ''
    response = {'data': products}
    return response
