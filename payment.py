from datetime import datetime
import os
PAYMENT_FILE = 'payments.txt'

class Payment:
    @staticmethod
    def process_payment(invoice, payment_method):
        # Simulate payment processing
        if payment_method in ['cash', 'card']:
            invoice.payment_status = 'paid'
            Payment.save_payment(invoice.order_id, payment_method, invoice.total_amount)
            return True
        return False

    @staticmethod
    def save_payment(order_id, payment_method, amount):
        with open(PAYMENT_FILE, 'a') as f:
            f.write(f"{order_id},{payment_method},{amount},{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")

    @staticmethod
    def read_payments():
        payments = []
        if os.path.exists(PAYMENT_FILE):
            with open(PAYMENT_FILE, 'r') as f:
                for line in f:
                    data = line.strip().split(',')
                    payment = {
                        'order_id': data[0],
                        'payment_method': data[1],
                        'amount': float(data[2]),
                        'payment_date': data[3]
                    }
                    payments.append(payment)
        return payments
