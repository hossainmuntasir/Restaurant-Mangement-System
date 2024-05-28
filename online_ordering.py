import os
from datetime import datetime

ONLINE_ORDERS_FILE = 'online_orders.txt'

class OnlineOrder:
    def __init__(self, order_id, customer_name, contact, order_type, address=None):
        self.order_id = order_id
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
            'order_id': self.order_id,
            'customer_name': self.customer_name,
            'contact': self.contact,
            'order_type': self.order_type,
            'address': self.address or '',
            'items': items_str,
            'total_amount': self.total_amount,
            'order_date': self.order_date
        }

class OnlineOrderManager:
    def __init__(self, filename):
        self.filename = filename

    def save_order(self, order):
        with open(self.filename, 'a') as f:
            items_str = order['items']
            order_data = f"{order['order_id']},{order['customer_name']},{order['contact']},{order['order_type']},{order['address']},{order['total_amount']:.2f},{items_str},{order['order_date']}\n"
            f.write(order_data)

    def read_orders(self):
        orders = []
        if os.path.exists(self.filename):
            with open(self.filename, 'r') as f:
                for line in f:
                    try:
                        data = line.strip().split(',')
                        if len(data) < 8:
                            print(f"Skipping invalid line: {line}")
                            continue  # Skip invalid lines
                        items_str = data[7:]
                        items = [{'item': item.split('(')[0], 'quantity': int(item.split('(')[1])} for item in items_str]
                        order = {
                            'order_id': data[0],
                            'customer_name': data[1],
                            'contact': data[2],
                            'order_type': data[3],
                            'address': data[4],
                            'total_amount': float(data[5]),
                            'items': items,
                            'order_date': data[6]
                        }
                        orders.append(order)
                    except (IndexError, ValueError) as e:
                        print(f"Skipping invalid line: {line} (Error: {e})")
                        continue  # Skip invalid lines
        print("Orders read:", orders)  # Debug print statement
        return orders
