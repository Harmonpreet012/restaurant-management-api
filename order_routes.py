from flask.json import jsonify
from flask_pymongo import PyMongo
from order import Order
from flask import Flask, request
import json

#setting up pymongo
app = Flask(__name__)
configuration_file = open("configuration.json")
data = json.load(configuration_file)

mongo_uri =data["mongo_uri"]
mongo = PyMongo(app = app, uri = mongo_uri)

def order():
    if request.method == "GET":
        if request.args.get("order_id"):
            try:
                response = mongo.db.orders.find_one({"order_id": int(request.args.get("order_id"))})
                order = Order(customer_id=response["customer_id"], restaurant_id=response["restaurant_id"], discount = response["discount"])
                return jsonify({"status":"ok", "data":order.get_dict()})
            except:
                return jsonify({"status":"error"})

        elif request.args.get("restaurant_id"):
            try:
                response = mongo.db.orders.find({"restaurant_id":int(request.args.get("restaurant_id")), "status": request.args.get("status")})
                orders = []
                for order in response:
                    order = Order(customer_id=order["customer_id"], restaurant_id=order["restaurant_id"], discount = order["discount"])
                    orders.append({order.get_dict()})
                return jsonify({"status":"ok", "data":orders})
            except:
                return jsonify({"status":"error"})
        else:
            try:
                response = mongo.db.orders.find({"status": request.args.get("status")})
                orders = []
                for order in response:
                    order = Order(customer_id=order["customer_id"], restaurant_id=order["restaurant_id"], discount = order["discount"])
                    orders.append(order.get_dict())
                return jsonify({"status":"ok", "data":orders})
            except:
                return jsonify({"status": "error"})

    if request.method == "POST":
        new_order = Order(
            customer_id         = request.form["customer_id"],
            restaurant_id       = request.form["restaurant_id"],
            discount            = request.form["discount_percent"] )
        try:
            mongo.db.orders.insert_one(new_order.get_dict())
            return jsonify({"status":"ok", "data":new_order.order_id})
        except:
            return jsonify({"status":"error"})

def assign_order():

    if request.method == "POST":
        #assigning table to order.
        try:
            filter = {"order_id": int(request.form["order_id"])}
            mongo.db.orders.update_one(filter = filter, update = {
                "$set":{
                    "table": int(request.form["table_id"])
                }
            })

            #assigning order to table.
            response = mongo.db.orders.find_one({"order_id": int(request.form["order_id"])})
            restaurant_id = int(response["restaurant_id"])

            response = mongo.db.restaurants.find_one({"restaurant_id": restaurant_id})
            tables = response["tables"]
            
            for table in tables:
                if table['table_id']==int(request.form["table_id"]):
                    table['current_order'] = int(request.form["order_id"])
                    break

            filter = {"restaurant_id": restaurant_id}
            mongo.db.restaurants.update_one(filter = filter, update = {
                "$set":{
                    "tables": tables
                }
            })
            return jsonify({"status":"ok"})
        except:
            return jsonify({"status":"error"})


def item():
    if request.method == "GET":
        try:
            order_id = int(request.form["order_id"])
            items = []
            response = mongo.db.orders.find({"order_id": order_id})

            for item in response:
                items.append(item)

            return jsonify({"data":items, "status":"ok"})
        except:
            return jsonify({"status":"error"})
    
    if request.method == "POST":
        try:
            order_id = int(request.form["order_id"])
            item_id  = int(request.form["item_id"])
            response = mongo.db.orders.find_one({"order_id": order_id})
            
            restaurant_id = int(response["restaurant_id"])
            
            items = response["items"]

            total_price = int(response["total_price"] )

            response = mongo.db.restaurants.find_one({"restaurant_id": restaurant_id})
            for item in response["menu"]:
                if item["id"] == item_id:
                    total_price = total_price + item["cost"]
                    break

            items.append(item_id)
            mongo.db.orders.update_one(filter = {"order_id":order_id}, update = {
                "$set":{
                    "items":       items,
                    "total_price": total_price

                }
            })
            return jsonify({"status": "ok"})
        except:
            return jsonify({"status":"error"})

def place_order():
    try:
        order_id = int(request.form["order_id"])
        mongo.db.orders.update_one(filter = {"order_id": order_id}, update={
            "$set":{
                "status":"placed"
            }
        })
        return jsonify({"status":"ok"})
    except: 
        return jsonify({"status":"error"})    