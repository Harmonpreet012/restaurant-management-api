import random
class Table:
    def __init__(self, table_id, capacity):
        self.table_id           = table_id
        self.current_order      = -1
        self.capacity           = capacity
    
    def get_dict(self):
        my_dict = {
            "table_id":        self.table_id,
            "current_order":   self.current_order,
            "capacity":        self.capacity
        }
        return my_dict

class MenuItem:
    def __init__(self, id, name, cost, quantity = "full", description ="", discount = 0 ):
        self.id             = int(id)
        self.name           = name
        self.cost           = int(cost)
        self.description    = description
        self.discount       = discount
        self.quantity       = quantity 
    
    def get_dict(self):
        my_dict = {
            "id":          self.id,
            "dish_name":   self.name,
            "cost":        self.cost,
            "description": self.description,
            "discount":    self.discount,
            "quantity":    self.quantity 
        }  
        return my_dict


class Restaurant:
    def __init__(self, name, owner_name, address, contact_number, restaurant_id=-1):
        self.restaurant_id  = restaurant_id
        if( self.restaurant_id == -1 ):
            self.restaurant_id  = random.randint(1001, 9999)
        self.name           = name
        self.address        = address
        self.owner_name     = owner_name
        self.contact_number = str(contact_number)
        self.tables         = []
        self.menu           = []
    
    def get_dict(self):
        my_dict = {
            "restaurant_id":   self.restaurant_id,
            "restaurant_name": self.name,
            "address":         self.address,
            "owner_name":      self.owner_name,
            "contact_number":  self.contact_number,
            "menu":            self.menu, 
            "tables":          self.tables
        }
        return my_dict

    