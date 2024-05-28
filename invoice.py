import os
from datetime import datetime

INVOICE_FILE = 'invoices.txt'

class Invoice:
    def __init__(self, order_id, customer_name, contact, items, total_amount, order_type, address=None, payment_status='pending'):
        self.order_id = order_id
        self.customer_name = customer_name
        self.contact = contact
        self.items = items
        self.total_amount = total_amount
        self.order_type = order_type
        self.address = address
        self.payment_status = payment_status
        self.invoice_date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    def get_invoice_data(self):
        items_str = ';'.join([f"{item['item']}({item['quantity']})" for item in self.items])
        return [str(self.order_id), self.customer_name, self.contact, self.order_type, self.address or '', f"{self.total_amount:.2f}", items_str, self.payment_status, self.invoice_date]

    @classmethod
    def save_invoice(cls, invoice_data):
        with open(INVOICE_FILE, 'a') as f:
            f.write(','.join(invoice_data) + '\n')

    @classmethod
    def read_invoices(cls):
        invoices = []
        if os.path.exists(INVOICE_FILE):
            with open(INVOICE_FILE, 'r') as f:
                for line in f:
                    data = line.strip().split(',')
                    if len(data) < 9:
                        print(f"Skipping invalid line: {line}")
                        continue  # Skip invalid lines
                    try:
                        items = [{'item': item.split('(')[0], 'quantity': int(item.split('(')[1].strip(')'))} for item in data[6].split(';')]
                        invoice = cls(data[0], data[1], data[2], items, float(data[5]), data[3], data[4], data[7])
                        invoice.invoice_date = data[8]
                        invoices.append(invoice)
                    except (IndexError, ValueError) as e:
                        print(f"Skipping invalid line: {line} (Error: {e})")
                        continue  # Skip invalid lines
        return invoices

    @classmethod
    def get_next_invoice_id(cls):
        invoices = cls.read_invoices()
        if invoices:
            return max(int(inv.order_id) for inv in invoices) + 1
        return 1
