import array
import json

import my_utils
from product import Product
from docproduct import DocProduct
from client import Client
from datetime import datetime
from dataprovider import DataProvider


class BuyDocument:

    @classmethod
    def addBuyProduct(cls, dp: DataProvider, store_id, bd_id, pr_id, qty, price):
        dp.exQuery("insert into buy_documents_p(store_id,buy_document_id,product_id,buy_qty,buy_price) values(%s,%s,%s,%s,%s) returning id",(store_id,bd_id,pr_id,qty,price,))

    def __init__(self, id:int, store_id:int, buy_num:str, buy_date, supplier: Client, doc_products):
        self.id = id
        self.buy_num = buy_num
        self.buy_date = buy_date
        self.supplier = supplier
        self.doc_products = doc_products

    @classmethod
    def newBuyDocument(cls,dp:DataProvider, store_id):
        dp.exQuery("insert into buy_documents(store_id) values (%s) RETURNING id",(store_id,))
        row = dp.cursor.fetchone()
        inserted_id=row[0]
        return BuyDocument(inserted_id, store_id, "", datetime.now(), None, [])

    @classmethod
    def getFromDb(cls, dp:DataProvider, id):
            dp.exQuery("select buy_documents.id, buy_documents.store_id, buy_documents.buy_num, buy_documents.buy_date, clients.id supplier_id, clients.client_name, clients.client_address, clients.client_phone, clients.client_note from buy_documents inner join clients on buy_documents.supplier_id=clients.id where buy_documents.id=%s",(id,))
            row = dp.cursor.fetchone()
            supplier = Client(row[4],row[1], row[5],row[6],row[7],row[8])
            store_id = row[1]
            buy_num = row[2]
            buy_date = row[3]
            dp.exQuery("select buy_documents_p.id, product_id, product_code, product_name, rec_price, buy_qty, buy_price from buy_documents_p inner join products on products.id=buy_documents_p.product_id where buy_document_id=%s",(id,))
            rows = dp.cursor.fetchall()
            products = []
            for row in rows:
                pr = Product(row[1],row[2],row[3],row[4])
                doc_p = DocProduct(row[0],store_id,pr,row[5],row[6])
                products.append(doc_p)
            return BuyDocument(id,store_id,buy_num,buy_date,supplier,products)

    @classmethod
    def updateToDb(cls, dp:DataProvider, id, store_id, buy_num, buy_date, supplier_id):
        dp.exQuery("update buy_documents set store_id=%s, buy_num=%s, buy_date=%s, supplier_id=%s where id=%s",(store_id, buy_num, buy_date.strftime("%Y-%m-%d"), supplier_id, id))

    def toString(self):
        date_str = self.buy_date.strftime('%d.%m.%Y')
        return f'Документ №{self.buy_num}, дата:{self.buy_date}, поставщик:{self.supplier.client_name}'
    
    def getJsonObj(self):
        products = []
        for product in self.doc_products:
            products.append({"id":product.id, "product_code":product.product.product_code, "product_name":product.product.product_name, "rec_price":product.product.rec_price, "qty": product.qty, "buy_price": product.doc_price})
        obj = {"id":self.id, "buy_num":self.buy_num, "buy_date":self.buy_date, "products":products}
        return obj

    def addProduct(self, doc_product:DocProduct):
        self.products.append(doc_product)


