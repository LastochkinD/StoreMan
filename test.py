from datetime import datetime

from buydocument import BuyDocument
from docproduct import DocProduct
from product import Product
from client import Client
from dataprovider import DataProvider

dp = DataProvider()
cl1 = Client(dp,1)
cl1.client_note = "Бла dsfgdsf"
cl1.client_name = "ООО Четрые пенька"
cl1.save()