import json

import my_utils
from product import Product
from docproduct import DocProduct
from client import Client
from datetime import datetime
from dataprovider import DataProvider


class SellDocument:

    def __init__(self, id:int, store_id:int, sell_num:str, sell_date, client: Client, doc_products):
        self.id = id
        self.sell_num = sell_num
        self.sell_date = sell_date
        self.client = client
        self.doc_products = doc_products

    @classmethod
    def addSellProduct(cls, dp: DataProvider, store_id, sd_id, pr_id, qty, price):
        dp.exQuery("insert into sell_documents_p(store_id,sell_document_id,product_id,sell_qty,sell_price) values(%s,%s,%s,%s,%s) returning id",(store_id,sd_id,pr_id,qty,price,))

    @classmethod
    def newSellDocument(cls,dp:DataProvider, store_id):
        dp.exQuery("insert into sell_documents(store_id) values (%s) RETURNING id",(store_id,))
        inserted_id = dp.cursor.fetchone()[0]
        return SellDocument(inserted_id, store_id, "", "", None, [])

    @classmethod
    def getFromDb(cls, dp:DataProvider, id):
            dp.exQuery("select sell_documents.id, sell_documents.store_id, sell_documents.sell_num, sell_documents.sell_date, sell_documents.client_id, clients.client_name, clients.client_address, clients.client_phone, clients.client_note from sell_documents left outer join clients on sell_documents.client_id=clients.id where sell_documents.id=%s",(id,))
            row = dp.cursor.fetchone()
            if row is not None:
                client = Client(row[4] ,row[1], row[5], row[6], row[7], row[8])
                store_id = row[1]
                sell_num = row[2]
                sell_date = row[3]
                dp.exQuery("select sell_documents_p.id, product_id, product_code, product_name, rec_price, sell_qty, sell_price from sell_documents_p inner join products on products.id=sell_documents_p.product_id where sell_document_id=%s",(id,))
                rows = dp.cursor.fetchall()
                products = []
                for row in rows:
                    pr = Product(row[1],row[2],row[3],row[4])
                    doc_p = DocProduct(row[0],store_id,pr,row[5],row[6])
                    products.append(doc_p)
                return SellDocument(id,store_id,sell_num,sell_date,client,products)
            else:
                return None

    @classmethod
    def updateToDb(cls, dp:DataProvider, id, store_id, sell_num, sell_date, client_id):
        dp.exQuery("update sell_documents set store_id=%s, sell_num=%s, sell_date=%s, client_id=%s where id=%s",(store_id, sell_num, sell_date.strftime("%Y-%m-%d"), client_id, id))

    def toString(self):
        date_str = self.buy_date.strftime('%d.%m.%Y')
        return f'Документ №{self.sell_num}, дата:{self.sell_date}, поставщик:{self.client.client_name}'
    
    def getJsonObj(self):
        products = []
        for product in self.doc_products:
            products.append({"id":product.id, "product_code":product.product.product_code, "product_name":product.product.product_name, "rec_price":product.product.rec_price, "qty": product.qty, "sell_price": product.doc_price})
        obj = {"id":self.id, "sell_num":self.sell_num, "sell_date":self.sell_date, "products":products}
        return obj

    def addProduct(self, doc_product:DocProduct):
        self.products.append(doc_product)

