from hashlib import new
from flask import request, Flask, jsonify
from restaurant import MenuItem, Restaurant, Table
from flask_pymongo import PyMongo

app = Flask(__name__)
mongo = PyMongo(app = app, uri = "mongodb+srv://db0:0000@cluster0.ssb5h.mongodb.net/ToastApp?retryWrites=true&w=majority")

def restaurant():
    if request.method == "GET":
        if request.args.get("restaurant_id"):
            response = mongo.db.restaurants.find({"restaurant_id": int(request.args.get("restaurant_id")) })
        else:    
            response = mongo.db.restaurants.find()

        res_dict = []
        for res in response:
            obj = Restaurant(
                name= res["restaurant_name"],
                owner_name = res["owner_name"], 
                address = res["address"], 
                contact_number= res["contact_number"], 
                restaurant_id= res["restaurant_id"] )

            res_dict.append(obj.get_dict())
        return jsonify(res_dict)
    
    if request.method == "POST":

        restaurant = Restaurant(
            name            = request.form["name"],
            address         = request.form["address"],
            owner_name      = request.form["owner_name"],
            contact_number  = request.form["contact_number"] )

        mongo.db.restaurants.insert_one(restaurant.get_dict())
        return {"restaurant-id":restaurant.restaurant_id}

def menu():
    if request.method == "GET":
        restaurant_id = int(request.args.get("restaurant_id"))
        response = mongo.db.restaurants.find_one({"restaurant_id": restaurant_id})
        return jsonify(response["menu"])

    if request.method == "POST":
        restaurant_id = int(request.form["restaurant_id"])
        response = mongo.db.restaurants.find_one({"restaurant_id": restaurant_id})
        
        new_item = MenuItem(
            id          = len(response["menu"])+1,
            name        = request.form["dish_name"],
            cost        = int(request.form["cost"]),
            quantity    = request.form["quantity"],
            description = request.form["description"],
            discount    = int(request.form["discount_percent"])  )

        prev_menu = response["menu"]
        prev_menu.append(new_item.get_dict())
        filter = {"restaurant_id": int(restaurant_id)}

        mongo.db.restaurants.update_one(filter = filter, update= { 
            "$set": {
                "menu":prev_menu
                }
            })
        return jsonify({"status":"ok"})

    if request.method == "DELETE":
        restaurant_id = int(request.form["restaurant_id"])
        response = mongo.db.restaurants.find_one({"restaurant_id": restaurant_id})
        prev_menu = response["menu"]

        
        for item in prev_menu:
            if item["id"] == int(request.form["id"]):
                prev_menu.remove(item)
                break
        filter = {"restaurant_id": int(restaurant_id)}

        mongo.db.restaurants.update_one(filter = filter, update= { 
            "$set": {
                "menu":prev_menu
                }
            })
        return jsonify({"status":"ok"})           

def table():
    if request.method == "GET":
        restaurant_id = int(request.args.get("restaurant_id"))
        response = mongo.db.restaurants.find_one({"restaurant_id": restaurant_id})
        return jsonify(response["tables"])        
    
    if request.method == "POST":        
        restaurant_id = int(request.form["restaurant_id"])
        response = mongo.db.restaurants.find_one({"restaurant_id": restaurant_id})
        prev_table_count = len(response["tables"])
        
        prev_table = response["tables"]
        new_table = Table(table_id= prev_table_count+1, capacity = int(request.form["capacity"]))
        prev_table.append(new_table.get_dict())

        filter = {"restaurant_id": int(restaurant_id)}
        mongo.db.restaurants.update_one(filter = filter, update= { 
            "$set": {
                "tables":prev_table
                }
        })
        return jsonify({"status":"ok"})

    if request.method == "DELETE":
        restaurant_id = int(request.form["restaurant_id"])
        response = mongo.db.restaurants.find_one({"restaurant_id": restaurant_id})
        tables = response["tables"]

        
        for table in tables:
            if table["table_id"] == int(request.form["table_id"]):
                tables.remove(table)
                break
        filter = {"restaurant_id": int(restaurant_id)}

        mongo.db.restaurants.update_one(filter = filter, update= { 
            "$set": {
                "tables":tables
                }
        })
        return jsonify({"status":"ok"})
