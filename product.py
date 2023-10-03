from dataprovider import DataProvider
import json


class Product:

    def __init__(self, id, product_code: str, product_name: str, rec_price: float):
            self.id = id
            self.product_code = product_code
            self.product_name = product_name
            self.rec_price = rec_price

    @classmethod
    def newProduct(cls, dp:DataProvider, store_id):
        inserted_id = dp.exQuery("insert into products(store_id) values (%s) RETURNING id",(store_id,)) 
        return Product(inserted_id, None, None, None)
    
    @classmethod
    def getProductFromDb(cls, dp:DataProvider, id):
            dp.exQuery("select id, product_code, product_name, rec_price from products where products.id=%s",(id,))
            row = dp.cursor.fetchone()
            return Product(row[0], row[1], row[2], row[3])
    
    @classmethod
    def delProduct(cls,dp:DataProvider,id):
        dp.exQuery('delete from products where id=%s',(id))
    
    def saveToDb(self, dp:DataProvider):
        dp.exQuery("update products set product_code=%s, product_name=%s, rec_price=%s where id=%s",(self.product_code, self.product_name, self.rec_price, self.id))

    def toString(self):
        return (f'Код: {self.product_code}, Наименование: {self.product_name}, Цена: {self.rec_price}')
    
    def getJsonObj(self):
        return {'id': self.id, 'product_code': self.product_code, 'product_name': self.product_name, 'rec_price': str(self.rec_price)}