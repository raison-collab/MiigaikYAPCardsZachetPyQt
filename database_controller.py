import sqlite3


class DatabaseController:
    def __init__(self, path: str):
        self.path = path

        self.connection = sqlite3.connect(path)

    def get_all_data(self):
        with self.connection as con:
            return con.cursor().execute('SELECT * FROM employee_cards').fetchall()

    def check_employee_by_card_number(self, card_number: int) -> bool:
        with self.connection as con:
            result = con.cursor().execute('SELECT * FROM employee_cards WHERE card_number=?', (card_number,)).fetchall()

        if len(result):
            return True
        return False

    def add_employee(self, card_number: int, first_name: str, second_name: str):
        with self.connection as con:
            con.cursor().execute('INSERT INTO employee_cards VALUES (?,?,?)', (card_number, first_name, second_name))

    def get_employee_by_card_number(self, card_number: int) -> tuple:
        with self.connection as con:
            return con.cursor().execute('SELECT * FROM employee_cards WHERE card_number=?', (card_number,)).fetchone()

