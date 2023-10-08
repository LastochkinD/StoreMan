from client import Client
from dataprovider import DataProvider
import json


class Store:
    id: int
    dp: DataProvider


    def __init__(self):
       self.dp = DataProvider()
       self.id = 1
       self.store_name = "Магазин электроники" 

    def getProducts(self):
        self.dp.exQuery("SELECT id, product_code, product_name, rec_price FROM products where products.store_id = %s order by product_code",(self.id,))
        rows = self.dp.cursor.fetchall()
        data = []
        for row in rows:
            product = {
                "id": row[0],
                "product_code": row[1],
                "product_name": row[2],
                "rec_price": float(row[3]) if row[3] is not None else None
            }
            data.append(product)
        return data
    
    def getClients(self):
        self.dp.exQuery("SELECT id, client_name, client_address, client_phone, client_note FROM clients order by client_name",())
        rows = self.dp.cursor.fetchall()
        data = []
        for row in rows:
            client = {
                "id": row[0],
                "client_name": row[1],
                "client_address": row[2],
                "client_phone": row[3],
                "client_note": row[4],
            }
            data.append(client)
        return data    

    def getProduct(self,id: int):
        self.dp.exQuery(f"SELECT id, product_code, product_name, rec_price FROM products where products.id={str(id)}")
        row = self.dp.cursor.fetchone()
        product_data = {
            'id': row[0],
            'product_code': row[1],
            'product_name': row[2],
            'rec_price': float(row[3]) if row[3] is not None else None
        }
        return product_data
    
    def acceptBuyDoc(self,buy_doc_id):
        self.dp.cursor.execute("select accepted from buy_documents where id = %s",(buy_doc_id,))
        row = self.dp.cursor.fetchone()
        if row[0]==0:
            self.dp.cursor.execute("insert into stock(store_id,bd_id,bdp_id, product_id,buy_price,stock_qty) (select store_id,buy_document_id,id,product_id,buy_price,buy_qty from buy_documents_p where buy_document_id = %s)",(buy_doc_id,))
            self.dp.cursor.execute("update buy_documents set accepted = 1 where id=%s",(buy_doc_id,))
            self.dp.connection.commit()
            return 1
        else:
            return -1


    def getBuyDocs(self):
        pass
