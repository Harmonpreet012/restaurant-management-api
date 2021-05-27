import random
from flask import jsonify, Flask
from flask_pymongo import PyMongo

app = Flask(__name__)
mongo = PyMongo(app = app, uri = "mongodb+srv://db0:0000@cluster0.ssb5h.mongodb.net/ToastApp?retryWrites=true&w=majority")

class NewItem:
    def __init__(self, item_id, quantity):
        self.item_id  =  item_id
        self.quantity = quantity

class Order:
    def __init__(self, customer_id, restaurant_id, discount =0 ):
        self.restaurant_id  = restaurant_id
        self.customer_id    = customer_id
        self.items          = []
        self.total_price    = 0
        self.discount       = discount
        self.status         = "placed"
        self.table          = -1
        self.order_id = random.randint(100000, 999999)
    
    def get_json(self):
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
