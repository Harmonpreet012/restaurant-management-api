import random
from flask import jsonify, Flask

class Order:
    def __init__(self, customer_id, restaurant_id, discount =0, order_id = -1, status="building", table=-1 ):
        self.restaurant_id  = int(restaurant_id)
        self.customer_id    = int(customer_id)
        self.items          = []
        self.total_price    = 0
        self.discount       = int(discount)
        self.status         = status
        self.table          = table
        self.order_id       = int(order_id)
        if order_id==-1:
            self.order_id = random.randint(100000, 999999)
    
    def get_dict(self):
        text = {
            "order_id":      self.order_id,
            "restaurant_id": self.restaurant_id,
            "customer_id":   self.customer_id,
            "total_price":   self.total_price,
            "items":         self.items,
            "status":        self.status,
            "discount":      self.discount,
            "table":         self.table
        }
        return text
