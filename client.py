import psycopg2
from psycopg2 import Error

from dataprovider import DataProvider


class Client:

    def __init__(self, client_id, client_name, client_address, client_phone, client_note):
            self.id = client_id
            self.client_name = client_name
            self.client_address = client_address
            self.client_phone = client_phone
            self.client_note = client_note

    @classmethod
    def newClient(cls, dp:DataProvider, client_name, client_address, client_phone, client_note):
        dp.cursor.execute("insert into clients(store_id, client_name, client_address, client_phone, client_note) values(%s,%s,%s,%s,%s) RETURNING id",(store_id,client_name,client_address, client_phone, client_note))
        dp.connection.commit()
        inserted_id = dp.cursor.fetchone()[0]
        return Client(inserted_id, client_name, client_address, client_phone, client_note)

    @classmethod
    def loadFromDb(cls,dp:DataProvider,id):
        dp.exQuery("select id, store_id, client_name, client_address, client_phone, client_note from clients where id=%s",(id))
        row = dp.cursor.fetchone()
        return Client(dp, id , row[1], row[2],row[3], row[4], row[5])

    @classmethod 
    def delClient(cls, dp:DataProvider, client_id: int):
            dp.exQuery("delete from clients where clients.id=%s",(client_id,))
    
    def toString(self):
        return f'{self.client_name}, {self.client_address}, {self.client_phone}'
    
    def getJsonObj(self):
        return {"id":self.id,"client_name":self.client_name, "client_address": self.client_address, "client_phone": self.client_phone, "client_note":self.client_note}
    
    def saveToDb(self):
        self.dp.exQuery('update clients set client_name=%s,client_address=%s, client_phone=%s,client_note=%s where id=',self.client_name, self.client_address, self.client_phone, self.client_note, self.id)