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
            response = mongo.db.orders.find_one({"order_id": int(request.args.get("order_id"))})
            order = Order(customer_id=response["customer_id"], restaurant_id=response["restaurant_id"], discount = response["discount"])
            return jsonify(order.get_dict())

        elif request.args.get("restaurant_id"):
            response = mongo.db.orders.find({"restaurant_id":int(request.args.get("restaurant_id")), "status": request.args.get("status")})
            orders = []
            for order in response:
                order = Order(customer_id=order["customer_id"], restaurant_id=order["restaurant_id"], discount = order["discount"])
                orders.append(order.get_dict())
            return jsonify(orders)
        else:
            response = mongo.db.orders.find({"status": request.args.get("status")})
            orders = []
            for order in response:
                order = Order(customer_id=order["customer_id"], restaurant_id=order["restaurant_id"], discount = order["discount"])
                orders.append(order.get_dict())
            return jsonify(orders)

    if request.method == "POST":
        new_order = Order(
            customer_id         = request.form["customer_id"],
            restaurant_id       = request.form["restaurant_id"],
            discount            = request.form["discount_percent"] )
        mongo.db.orders.insert_one(new_order.get_json())
        return jsonify({"order-id":new_order.order_id})

def assign_order():

    #assigning table to order.
    filter = {"order_id": int(request.form["order_id"])}
    mongo.db.orders.update(filter = filter, update = {
        "$set":{
            "table": int(request.form["table_id"])
        }
    })

    #assigning order to table.
    response = mongo.db.orders.find({"order_id": int(request.form["order_id"])})
    restaurant_id = int(response["restaurant_id"])
    response = mongo.db.orders.find({"restaurant_id": restaurant_id})
    tables = response["table"]
    for table in tables:
        if table.id == request.form["table_id"]:
            table.current_order = int(request.form["order_id"])
            break
    filter = {"restaurant_id": restaurant_id, "table_id": int(request.form["table_id"])}
    mongo.db.restaurants.update(filter = filter, update = {
        "$set":{
            "tables": tables
        }
    })

    return jsonify({"status":"ok"})


def item():
    if request.method == "GET":
        order_id = int(request.form["order_id"])
        items = []
        response = mongo.db.orders.find({"order_id": order_id})

        for item in response:
            items.append(item)

        return jsonify(items)
    
    if request.method == "POST":
        order_id = int(request.form["order_id"])
        item_id  = request.form["item_id"]
        response = mongo.db.find_one({"order_id": order_id})
        
        restaurant_id = int(response["restaurant_id"])
        items = response["items"]
        total_price = int(response["total_price"] )

        response = mongo.db.restaurants.find_one({"restaurant_id": restaurant_id})
        for item in response["menu"]:
            if item.item_id == item_id:
                total_price = total_price + item.cost
                break

        items.append(item_id)
        mongo.db.orders.update(filter = filter, update = {
            "$set":{
                "items":       items,
                "total_price": total_price

            }
        })
        return jsonify({"status": "ok"})

def place_order():
    order_id = request.args.get("order_id")
    response = mongo.db.orders.update(filter = {"order_id": order_id}, update={
        "$set":{
            "status":"placed"
        }
    })
    return jsonify({"status":"ok"})
    