import os

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
    def __init__(self, customer_name, contact, table_no):
        self.customer_name = customer_name
        self.contact = contact
        self.table_no = table_no
        self.items = []
        self.total_amount = 0.0

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
            'table_no': self.table_no,
            'items': items_str,
            'total_amount': self.total_amount
        }

class OrderManager:
    def __init__(self, filename):
        self.filename = filename

    def save_order(self, order):
        with open(self.filename, 'a') as f:
            items_str = order['items']
            order_data = f"{order['customer_name']},{order['contact']},{order['table_no']},{order['total_amount']:.2f},{items_str}\n"
            f.write(order_data)

    def read_orders(self):
        orders = []
        if os.path.exists(self.filename):
            with open(self.filename, 'r') as f:
                for line in f:
                    try:
                        data = line.strip().split(',')
                        if len(data) < 5:
                            print(f"Skipping invalid line: {line}")
                            continue  # Skip invalid lines
                        items_str = data[4]
                        items = [{'item': item.split('(')[0], 'quantity': int(item.split('(')[1][:-1])} for item in items_str.split(';')]
                        order = {
                            'customer_name': data[0],
                            'contact': data[1],
                            'table_no': data[2],
                            'items': items,
                            'total_amount': float(data[3])
                        }
                        orders.append(order)
                    except (IndexError, ValueError) as e:
                        print(f"Skipping invalid line: {line} (Error: {e})")
                        continue  # Skip invalid lines
        print("Orders read:", orders)  # Debug print statement
        return orders
