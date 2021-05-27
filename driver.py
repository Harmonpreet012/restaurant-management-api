from flask import Flask
from flask.templating import render_template
from flask_pymongo import PyMongo
import order_routes
import restaurant_routes

app = Flask(__name__, static_url_path='/static')

@app.route('/')
def home():
    return render_template("home.html")

#Routes for orders
app.add_url_rule('/order', view_func = order_routes.order, methods = ['GET', 'POST'])
app.add_url_rule('/order/assign', view_func = order_routes.assign, methods = ['POST'])
app.add_url_rule('/order/item', view_func = order_routes.item, methods = ['POST'])

#routes for restaurants
app.add_url_rule('/restaurant', view_func = restaurant_routes.restaurant, methods = ['GET', 'POST'])
app.add_url_rule('/restaurant/table', view_func = restaurant_routes.table, methods = ['GET','POST', 'DELETE'])
app.add_url_rule('/restaurant/menu', view_func = restaurant_routes.menu, methods = ['GET', 'POST', 'DELETE'])

app.run()