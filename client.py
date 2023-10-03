from dataprovider import DataProvider
class Client:

    def __init__(self, client_id, store_id, client_name, client_address, client_phone, client_note):
            self.id = client_id
            self.client_name = client_name
            self.client_address = client_address
            self.client_phone = client_phone
            self.client_note = client_note

    @classmethod
    def newClient(dp:DataProvider,store_id,client_name,client_address, client_phone, client_note):
        inserted_id = dp.exQuery("insert into clients(store_id, client_name, client_address, client_phone, client_note) values(%s,%s,%s,%s,%s) RETURNING id",(store_id,client_name,client_address, client_phone, client_note))
        return Client(inserted_id,store_id,client_name,client_address, client_phone, client_note)

    @classmethod
    def loadFromDb(dp:DataProvider,id):
        dp.exQuery("select id, store_id, client_name, client_address, client_phone, client_note from clients where id=%s",(id))
        row = dp.cursor.fetchone()
        return Client(id,row[1],row[2],row[3], row[4], row[5])

    
    def toString(self):
        return f'{self.client_name}, {self.client_address}, {self.client_phone}'
    
    def save(self):
        self.dp.exQuery(f'update clients set client_name=\'{self.client_name}\',client_address=\'{self.client_address}\', client_phone=\'{self.client_phone}\',client_note=\'{self.client_note}\'')