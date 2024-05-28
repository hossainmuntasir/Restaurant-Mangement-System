import os

TABLES_FILE = 'tables.txt'
RESERVATIONS_FILE = 'reservations.txt'

class Table:
    def __init__(self, table_id, capacity, status):
        self.table_id = table_id
        self.capacity = capacity
        self.status = status

    def __repr__(self):
        return f"Table(table_id={self.table_id}, capacity={self.capacity}, status={self.status})"

    @classmethod
    def read_tables(cls, filename):
        tables = []
        if os.path.exists(filename):
            with open(filename, 'r') as f:
                for line in f:
                    table_id, capacity, status = line.strip().split(',')
                    tables.append(cls(int(table_id), int(capacity), status))
        print("Loaded tables:", tables)  # Debug print statement
        return tables

    @classmethod
    def save_tables(cls, tables, filename):
        with open(filename, 'w') as f:
            for table in tables:
                f.write(f"{table.table_id},{table.capacity},{table.status}\n")

    @classmethod
    def find_table(cls, tables, table_id):
        for table in tables:
            if table.table_id == table_id:
                return table
        return None

    @classmethod
    def change_table_status(cls, tables, table_id, new_status):
        table = cls.find_table(tables, table_id)
        if table:
            table.status = new_status
            cls.save_tables(tables, TABLES_FILE)
            return True
        return False

class Reservation:
    def __init__(self, customer_name, contact, day, time, table_id, number_of_person):
        self.customer_name = customer_name
        self.contact = contact
        self.day = day
        self.time = time
        self.table_id = table_id
        self.number_of_person = number_of_person

    def get_reservation_data(self):
        return [self.customer_name, self.contact, self.day, self.time, str(self.table_id), str(self.number_of_person)]

class ReservationManager:
    def __init__(self, filename):
        self.filename = filename

    def save_reservation(self, reservation):
        with open(self.filename, 'a') as f:
            f.write(','.join(reservation) + '\n')
