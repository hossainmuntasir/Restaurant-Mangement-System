from flask import Flask, request, render_template, redirect, url_for, jsonify
from order import Menu, Order, OrderManager
from reservation import Table, Reservation, ReservationManager
from manage_menu import MenuManager
from invoice import Invoice
from payment import Payment
from analytics import Analytics

app = Flask(__name__)

menu_manager = MenuManager('menu.txt')
order_manager = OrderManager('orders.txt')
tables = Table.read_tables('tables.txt')
reservation_manager = ReservationManager('reservations.txt')
analytics = Analytics('orders.txt')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/select_role', methods=['POST'])
def select_role():
    role = request.form['role']
    if role == 'customer':
        return redirect(url_for('customer_home'))
    elif role == 'staff':
        return redirect(url_for('staff_home'))
    else:
        return redirect(url_for('welcome'))

@app.route('/customer')
def customer_home():
    return render_template('customer_home.html')

@app.route('/staff')
def staff_home():
    return render_template('staff_home.html')

@app.route('/order')
def order_page():
    current_menu = menu_manager.read_menu()
    return render_template('order.html', menu=current_menu)

@app.route('/submit_order', methods=['POST'])
def submit_order():
    customer_name = request.form['customer_name']
    contact = request.form['contact']
    order_type = request.form['order_type']
    table_no = request.form.get('table_no', '')
    address = request.form.get('address', '')

    items = request.form.getlist('item')
    quantities = request.form.getlist('quantity[]')

    order = Order(customer_name, contact, order_type, table_no if order_type == 'dine-in' else address)

    for i, item in enumerate(items):
        quantity = int(quantities[i])
        price = float(request.form[f'price_{i}'])
        order.add_item(item, quantity, price)

    order.calculate_total()
    order_manager.save_order(order.get_order_data())

    order_id = Invoice.get_next_invoice_id()
    invoice = Invoice(order_id, order.customer_name, order.contact, order.items, order.total_amount, order_type, address)
    Invoice.save_invoice(invoice.get_invoice_data())

    analytics.analyze_orders()
    return redirect(url_for('show_invoice', order_id=order_id))


@app.route('/invoice/<order_id>')
def show_invoice(order_id):
    invoices = Invoice.read_invoices()
    invoice = next((inv for inv in invoices if inv.order_id == str(order_id)), None)
    if invoice:
        return render_template('invoice.html', invoice=invoice)
    return "Invoice not found", 404

@app.route('/process_payment', methods=['POST'])
def process_payment():
    order_id = request.form['order_id']
    payment_method = request.form['payment_method']
    invoices = Invoice.read_invoices()
    invoice = next((inv for inv in invoices if inv.order_id == str(order_id)), None)
    if invoice and Payment.process_payment(invoice, payment_method):
        Invoice.save_invoice(invoice.get_invoice_data())
        return render_template('payment_success.html')
    return "Payment failed", 400

@app.route('/reservation')
def reservation_page():
    return render_template('reservation.html', tables=tables)

@app.route('/reservation_manage')
def manage_reservations_page():
    return render_template('reservation_manage.html', tables=tables)

@app.route('/submit_reservation', methods=['POST'])
def submit_reservation():
    customer_name = request.form['customer_name']
    contact = request.form['contact']
    day = request.form['day']
    time = request.form['time']
    table_id = int(request.form['table_id'])
    number_of_person = int(request.form['number_of_person'])

    table = Table.find_table(tables, table_id)
    if table and table.status == 'available':
        table.status = 'reserved'
        Table.save_tables(tables, 'tables.txt')

        reservation = Reservation(
            customer_name, contact, day, time, table_id, number_of_person)
        reservation_manager.save_reservation(
            reservation.get_reservation_data())
        return redirect(url_for('reservation_page'))
    else:
        return "Table not available", 400

@app.route('/manage_menu')
def manage_menu_page():
    current_menu = menu_manager.read_menu()
    return render_template('manage_menu.html', menu=current_menu)

@app.route('/add_menu_item', methods=['POST'])
def add_menu_item():
    item = request.form['item']
    price = request.form['price']
    menu_manager.add_menu_item(item, price)
    return redirect(url_for('manage_menu_page'))

@app.route('/edit_menu_item/<item>', methods=['GET', 'POST'])
def edit_menu_item(item):
    if request.method == 'POST':
        new_item = request.form['new_item']
        new_price = request.form['new_price']
        menu_manager.update_menu_item(item, new_item, new_price)
        return redirect(url_for('manage_menu_page'))
    else:
        current_menu = menu_manager.read_menu()
        for menu_item in current_menu:
            if menu_item['item'] == item:
                return render_template('edit_menu_item.html', item=menu_item)
        return "Item not found", 404

@app.route('/delete_menu_item/<item>', methods=['POST'])
def delete_menu_item(item):
    menu_manager.delete_menu_item(item)
    return redirect(url_for('manage_menu_page'))

@app.route('/change_table_status', methods=['POST'])
def change_table_status():
    data = request.get_json()
    table_id = int(data['table_id'])
    new_status = data['new_status']
    tables = Table.read_tables('tables.txt')

    if Table.change_table_status(tables, table_id, new_status):
        return jsonify({'status': 'success', 'message': f'Table {table_id} status changed to {new_status}'})
    else:
        return jsonify({'status': 'error', 'message': 'Table not found'})

@app.route('/api/tables', methods=['GET'])
def get_tables():
    global tables
    tables = Table.read_tables('tables.txt')
    return jsonify([{'table_id': table.table_id, 'capacity': table.capacity, 'status': table.status} for table in tables])

@app.route('/analytics')
def analytics_page():
    most_ordered_items = analytics.analyze_orders()
    return render_template('analytics.html', most_ordered_items=most_ordered_items)

@app.route('/order')
def online_order_page():
    current_menu = menu_manager.read_menu()
    return render_template('order.html', menu=current_menu)

# @app.route('/submit_online_order', methods=['POST'])
# def submit_online_order():
#     customer_name = request.form['customer_name']
#     contact = request.form['contact']
#     order_type = request.form['order_type']
#     address = request.form['address'] if order_type == 'delivery' else None
#     items = request.form.getlist('item')
#     quantities = request.form.getlist('quantity')

#     order_id = Invoice.get_next_invoice_id()
#     order = Order(customer_name, contact, order_type, address)

#     for i, item in enumerate(items):
#         quantity = int(quantities[i])
#         price = float(request.form[f'price_{i+1}'])
#         order.add_item(item, quantity, price)

#     order.calculate_total()
#     order_manager.save_order(order.get_order_data())

#     invoice = Invoice(order_id, order.customer_name, order.contact, order.items, order.total_amount, order_type, address)
#     Invoice.save_invoice(invoice.get_invoice_data())

#     analytics.analyze_orders()
#     return redirect(url_for('show_invoice', order_id=order_id))

@app.route('/view_menu')
def view_menu():
    current_menu = menu_manager.read_menu()
    return render_template('view_menu.html', menu=current_menu)

if __name__ == '__main__':
    app.run(debug=True)
