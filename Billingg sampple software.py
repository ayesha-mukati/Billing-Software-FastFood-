#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import tkinter as tk
from tkinter import messagebox
from pymongo import MongoClient
from bson.objectid import ObjectId

# MongoDB setup
client = MongoClient('mongodb://localhost:27017/')
db = client['billing_system']
items_collection = db['items']

bills_collection = db['bills']

# Item list with prices
items = {
    "MOZERRELA PIZZA": 100,
    "FERRERO ROCHER CAKE": 50,
    "Burger": 70,
    "Coffee": 150,
    "Nachos": 200
    
    
    
}



# First form: Add items to cart
class AddItemsForm:
    def __init__(self, root):
        self.root = root
        self.cart = []
        self.total = 0

        self.root.title("Billing System - Add Items")
        
        self.label = tk.Label(root, text="AYESHA'S CAKE SHOP AND FAST FOOD CENTER SHOPPING CART")
        self.label.pack()

        self.label = tk.Label(root, text="Select Item")
        self.label.pack()

        self.item_var = tk.StringVar(root)
        self.item_var.set("ORDER HERE")  # default value

        self.dropdown = tk.OptionMenu(root, self.item_var, *items.keys())
        self.dropdown.pack()

        self.quantity_label = tk.Label(root, text="Quantity")
        self.quantity_label.pack()

        self.quantity_var = tk.IntVar(value=1)
        self.quantity_entry = tk.Entry(root, textvariable=self.quantity_var)
        self.quantity_entry.pack()

        self.add_button = tk.Button(root, text="Add to Cart", command=self.add_to_cart)
        self.add_button.pack()

        self.view_cart_button = tk.Button(root, text="View Cart", command=self.view_cart)
        self.view_cart_button.pack()

    def add_to_cart(self):
        item_name = self.item_var.get()
        quantity = self.quantity_var.get()
        price = items[item_name]
        total_item_price = price * quantity
        self.cart.append({
            "item": item_name,
            "quantity": quantity,
            "price_per_item": price,
            "total_price": total_item_price
        })
        self.total += total_item_price
        messagebox.showinfo("Success", f"Added {quantity} {item_name}(s) to cart.")

    def view_cart(self):
        BillForm(self.root, self.cart, self.total)


# Second form: Display bill and save to MongoDB
class BillForm:
    def __init__(self, root, cart, total):
        self.root = root
        self.cart = cart
        self.total = total

        self.bill_window = tk.Toplevel(self.root)
        self.bill_window.title("Billing System - Bill")

        self.bill_text = tk.Text(self.bill_window, width=50, height=20)
        self.bill_text.pack()

        self.display_bill()

        self.save_button = tk.Button(self.bill_window, text="Save Bill", command=self.save_bill)
        self.save_button.pack()

    def display_bill(self):
        bill_text = ""
        for item in self.cart:
            bill_text += f"{item['item']} (x{item['quantity']}): {item['total_price']}\n"
        bill_text += f"\nTotal: {self.total}"
        self.bill_text.insert(tk.END, bill_text)

    def save_bill(self):
        bill_data = {
            "items": self.cart,
            "total": self.total
        }
        bills_collection.insert_one(bill_data)
        messagebox.showinfo("Success", "Bill saved to database!")


# Main application
if __name__ == "__main__":
    root = tk.Tk()
    app = AddItemsForm(root)
    root.mainloop()


# In[ ]:





# In[ ]:




