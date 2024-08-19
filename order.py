import os
from datetime import datetime

ORDERS_FILE = 'orders.txt'

class Menu:
    def __init__(self, filename):
        self.filename = filename
        self.items = self.read_menu()

    def read_menu(self):
        menu = []
        if os.path.exists(self.filename):
            with open(self.filename, 'r') as f:
                for line in f:
                    item, price = line.strip().split(',')
                    menu.append({'item': item, 'price': float(price)})
        return menu

class Order:
    def __init__(self, customer_name, contact, order_type, address=None):
        self.customer_name = customer_name
        self.contact = contact
        self.order_type = order_type
        self.address = address
        self.items = []
        self.total_amount = 0.0
        self.order_date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    def add_item(self, item, quantity, price):
        self.items.append({'item': item, 'quantity': quantity, 'price': price})
        self.total_amount += quantity * price

    def calculate_total(self):
        self.total_amount = sum(item['quantity'] * item['price'] for item in self.items)

    def get_order_data(self):
        items_str = ';'.join([f"{item['item']}({item['quantity']})" for item in self.items])
        return {
            'customer_name': self.customer_name,
            'contact': self.contact,
            'order_type': self.order_type,
            'address': self.address,
            'items': items_str,
            'total_amount': self.total_amount,
            'order_date': self.order_date
        }

class OrderManager:
    def __init__(self, filename):
        self.filename = filename

    def save_order(self, order):
        with open(self.filename, 'a') as f:
            items_str = order['items']
            order_data = f"{order['customer_name']},{order['contact']},{order['order_type']},{order['address']},{order['total_amount']:.2f},{items_str},{order['order_date']}\n"
            f.write(order_data)

    def read_orders(self):
        orders = []
        if os.path.exists(self.filename):
            with open(self.filename, 'r') as f:
                for line in f:
                    try:
                        data = line.strip().split(',')
                        if len(data) < 7:
                            print(f"Skipping invalid line: {line}")
                            continue  # Skip invalid lines
                        items_str = data[5]
                        items = [{'item': item.split('(')[0], 'quantity': int(item.split('(')[1].strip(')'))} for item in items_str.split(';')]
                        order = {
                            'customer_name': data[0],
                            'contact': data[1],
                            'order_type': data[2],
                            'address': data[3],
                            'items': items,
                            'total_amount': float(data[4]),
                            'order_date': data[6]
                        }
                        orders.append(order)
                    except (IndexError, ValueError) as e:
                        print(f"Skipping invalid line: {line} (Error: {e})")
                        continue  # Skip invalid lines
        print("Orders read:", orders)  # Debug print statement
        return orders
