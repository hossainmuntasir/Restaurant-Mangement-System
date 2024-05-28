import os
from collections import Counter

ORDERS_FILE = 'orders.txt'

class Analytics:
    def __init__(self, filename):
        self.filename = filename

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
                        items_str = data[4:]
                        items = []
                        for item in items_str:
                            if ':' in item:
                                name, quantity = item.split(':')
                                items.append({'item': name.strip(), 'quantity': int(quantity)})
                            elif '(' in item:
                                name, quantity = item.split('(')
                                quantity = quantity.rstrip(')')
                                items.append({'item': name.strip(), 'quantity': int(quantity)})
                        orders.append(items)
                    except (IndexError, ValueError) as e:
                        print(f"Skipping invalid line: {line} (Error: {e})")
                        continue  # Skip invalid lines
        print("Orders read:", orders)  # Debug print statement
        return orders

    def analyze_orders(self):
        orders = self.read_orders()
        item_counter = Counter()

        for order in orders:
            for item in order:
                item_counter[item['item']] += item['quantity']

        most_ordered_items = item_counter.most_common()
        print("Most ordered items:", most_ordered_items)  # Debug print statement
        return most_ordered_items

# Example usage:
# analytics = Analytics(ORDERS_FILE)
# most_ordered_items = analytics.analyze_orders()
# print(most_ordered_items)
