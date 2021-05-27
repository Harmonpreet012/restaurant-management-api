from restaurant_routes import restaurant
from flask.json import jsonify
from flask_pymongo import PyMongo
from order import Order
from flask import Flask, request

app = Flask(__name__)
mongo = PyMongo(app = app, uri = "mongodb+srv://db0:0000@cluster0.ssb5h.mongodb.net/ToastApp?retryWrites=true&w=majority")

def order():
    if request.method == "GET":
        if request.args.get("order_id"):
            response = mongo.db.orders.find({"order_id": int(request.args.get("order_id"))})
            return jsonify(response)

        elif request.args.get("restaurant_id"):
            response = mongo.db.orders.find({"restaurant_id":int(request.args.get("restaurant_id")), "status": request.args.get("status")})
            for res in response:
                return

        else:
            res = mongo.db.orders.find({"status": request.args.get("status")})

    if request.method == "POST":
        new_order = Order(
            customer_id         = request.form["customer_id"],
            restaurant_id       = request.form["restaurant_id"],
            discount            = request.form["discount_percent"] )
        mongo.db.orders.insert_one(new_order.get_json())
        return jsonify({"order-id":new_order.order_id})

def assign():
    order_id = request.form["order_id"]
    table_id = request.form["table_id"]
    #restaurant_id = 

def item():
    order_id = request.form["order_id"]
    table_id = request.form["table_id"]
    #restaurant_id = 