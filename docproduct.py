from product import Product

class DocProduct:
    def __init__(self, id, store_id, product: Product, qty: float, price: float):
        self.id = id
        self.store_id = store_id
        self.product = product
        self.qty = qty
        self.doc_price = price
