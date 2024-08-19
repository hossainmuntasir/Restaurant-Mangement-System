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
                        if len(data) < 6:
                            print(f"Skipping invalid line: {line}")
                            continue  # Skip invalid lines
                        items_str = data[5]
                        items = [{'item': item.split('(')[0], 'quantity': int(item.split('(')[1].strip(')'))} for item in items_str.split(';')]
                        orders.append(items)
                    except (IndexError, ValueError) as e:
                        print(f"Skipping invalid line: {line} (Error: {e})")
                        continue  # Skip invalid lines
        return orders

    def analyze_orders(self):
        orders = self.read_orders()
        item_counter = Counter()

        for order in orders:
            for item in order:
                item_counter[item['item']] += item['quantity']

        most_ordered_items = item_counter.most_common()
        return most_ordered_items
