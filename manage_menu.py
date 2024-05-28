import os

MENU_FILE = 'menu.txt'

class MenuManager:
    def __init__(self, filename):
        self.filename = filename
        self.menu = self.read_menu()

    def read_menu(self):
        menu = []
        if os.path.exists(self.filename):
            with open(self.filename, 'r') as f:
                for line in f:
                    item, price = line.strip().split(',')
                    menu.append({'item': item, 'price': float(price)})
        return menu

    def write_menu(self, menu):
        with open(self.filename, 'w') as f:
            for item in menu:
                f.write(f"{item['item']},{item['price']}\n")

    def add_menu_item(self, item, price):
        self.menu.append({'item': item, 'price': float(price)})
        self.write_menu(self.menu)
        self.menu = self.read_menu()  # Reload menu

    def update_menu_item(self, old_item, new_item, new_price):
        for item in self.menu:
            if item['item'] == old_item:
                item['item'] = new_item
                item['price'] = float(new_price)
                break
        self.write_menu(self.menu)
        self.menu = self.read_menu()  # Reload menu

    def delete_menu_item(self, item_name):
        self.menu = [item for item in self.menu if item['item'] != item_name]
        self.write_menu(self.menu)
        self.menu = self.read_menu()  # Reload menu
