from flask import Flask, request, jsonify
from flask_cors import CORS
import json
from datetime import datetime

from store import Store
from product import Product
from client import Client
from buydocument import BuyDocument
from selldocument import SellDocument
from docproduct import DocProduct

store = Store()

app = Flask(__name__)
CORS(app)

#Получить список товаров
@app.route("/get_products", methods = ['get'])
def get_products():
    return jsonify(store.getProducts())

#Получить список клиентов
@app.route("/get_clients", methods = ['get'])
def get_clients():
    return jsonify(store.getClients())

#Получить список клиентов
@app.route("/get_buy_docs", methods = ['get'])
def get_buy_docs():
    sup_name_filter = request.args.get('sup_name_filter')
    if sup_name_filter is None:
        sup_name_filter = ''
    return jsonify(BuyDocument.getBuyDocs(store.dp,sup_name_filter))

#Добавить клиента
@app.route("/add_client", methods = ['post'])
def addClient():
    json_text = request.get_data()
    json_obj = json.loads(json_text)
    client = Client.newClient(store.dp,store.id,json_obj["client_name"],json_obj["client_address"],json_obj["client_phone"],json_obj["client_note"])
    return jsonify(client.getJsonObj())


#Обновить данные клиента
@app.route("/update_client", methods = ['post'])
def updateClient():
    json_text = request.get_data()
    json_obj = json.loads(json_text)
    client = Client.loadFromDb(store.dp,json_obj["id"])
    client.client_name = json_obj["client_name"]
    client.client_address = json_obj["client_address"]
    client.client_phone = json_obj["client_phone"]
    client.client_note = json_obj["client_note"]
    Client.saveToDb
    return jsonify(client.getJsonObj())

#Удалить клиента
@app.route("/del_client", methods = ['post'])
def delClient():
    json_text = request.get_data()
    json_obj = json.loads(json_text)
    print(json_obj["client_id"])
    result = Client.delClient(store.dp, int(json_obj["client_id"]))
    return jsonify({"Result":result})

#Получить товар
@app.route("/get_product", methods = ['get'])
def get_product():
    product = Product.getProductFromDb(store.dp, request.args.get('id'))
    return jsonify(product.getJsonObj())

@app.route("/update_product", methods = ['post'])
def update_product():
    json_obj = json.loads(request.get_data())
    product = Product.getProductFromDb(store.dp,json_obj["id"])
    product.product_code = json_obj["product_code"]
    product.product_name = json_obj["product_name"]
    product.rec_price = json_obj["rec_price"]
    product.saveToDb(store.dp)
    return jsonify({"Result":"Ok"})

@app.route("/new_product", methods = ['post'])
def new_product():
    json_obj = json.loads(request.get_data())
    product = Product.newProduct(store.dp, store.id)
    return jsonify({"Result":"Ok","inserted_id":product.id})

@app.route("/del_product", methods = ['get'])
def delproduct():
    Product.delProduct(store.dp,request.args.get('id'))
    return jsonify({"Result":"Ok"})

@app.route("/get_buy_doc", methods = ['get'])
def get_buy_doc():
    buy_doc = BuyDocument.getFromDb(store.dp,request.args.get('id'))
    return jsonify(buy_doc.getJsonObj())

@app.route("/new_buy_doc", methods = ['post'])
def newBuyDoc():
    json_obj = json.loads(request.get_data())
    buy_doc = BuyDocument.newBuyDocument(store.dp,json_obj["store_id"])
    return jsonify({"Result":"Ok","inserted_id":buy_doc.id})

@app.route("/update_buy_doc", methods = ['post'])
def updateBuyDoc():
    json_obj = json.loads(request.get_data())
    BuyDocument.updateToDb(store.dp, json_obj["id"], json_obj["store_id"], json_obj["buy_num"], datetime.strptime(json_obj["buy_date"], '%d.%m.%Y'), json_obj["supplier_id"])
    return jsonify({"Result":"Ok"})

@app.route("/add_buy_product", methods = ['post'])
def addBuyProduct():
    json_obj = json.loads(request.get_data())
    BuyDocument.addBuyProduct(store.dp,json_obj["store_id"],json_obj["buy_document_id"],json_obj["product_id"],json_obj["qty"],json_obj["price"])
    return jsonify({"Result":"Ok"})

@app.route("/get_sell_doc", methods = ['get'])
def get_sell_doc():
    sell_doc = SellDocument.getFromDb(store.dp,request.args.get('id'))
    return jsonify(sell_doc.getJsonObj())

@app.route("/new_sell_doc", methods = ['post'])
def newSellDoc():
    json_obj = json.loads(request.get_data())
    sell_doc = SellDocument.newSellDocument(store.dp,store.id)
    return jsonify({"Result":"Ok","inserted_id":sell_doc.id})

@app.route("/update_sell_doc", methods = ['post'])
def updateSellDoc():
    json_obj = json.loads(request.get_data())
    SellDocument.updateToDb(store.dp,json_obj["id"],store.id,json_obj["sell_num"],datetime.strptime(json_obj["sell_date"], '%d.%m.%Y'),json_obj["client_id"])
    return jsonify({"Result":"Ok"})

@app.route("/add_sell_product", methods = ['post'])
def addSellProduct():
    json_obj = json.loads(request.get_data())
    SellDocument.addSellProduct(store.dp, json_obj["store_id"], json_obj["stock_id"], json_obj["sell_document_id"],json_obj["product_id"],json_obj["qty"],json_obj["price"])
    return jsonify({"Result":"Ok"})

@app.route("/accept_buy_doc", methods = ['post'])
def acceptBuyDoc():
    json_obj = json.loads(request.get_data())
    store.acceptBuyDoc(int(json_obj["buy_doc_id"]))
    return jsonify({"Result":"Ok"})