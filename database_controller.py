import sqlite3


class DatabaseController:
    def __init__(self, path: str):
        self.path = path

        self.connection = sqlite3.connect(path)

    def get_all_data_employee_cards(self):
        with self.connection as con:
            return con.cursor().execute('SELECT * FROM employee_cards').fetchall()

    def check_employee_by_card_number(self, card_number: int) -> bool:
        with self.connection as con:
            result = con.cursor().execute('SELECT * FROM employee_cards WHERE card_number=?', (card_number,)).fetchall()

        if len(result):
            return True
        return False

    def check_employee_in_visitors(self, card_number: int) -> bool:
        with self.connection as con:
            result = con.cursor().execute('SELECT * FROM employee_visiting WHERE card_number=?', (card_number,)).fetchall()

        if len(result):
            return True
        return False

    def add_employee(self, data: tuple):
        with self.connection as con:
            con.cursor().execute('INSERT INTO employee_cards VALUES (?,?,?,?,?,?,?,?)', data)

    def get_employee_by_card_number(self, card_number: int) -> tuple:
        with self.connection as con:
            return con.cursor().execute('SELECT * FROM employee_cards WHERE card_number=?', (card_number,)).fetchone()

    def add_employee_visiting_time_in(self, card_number: int, time_in: str):
        with self.connection as con:
            con.cursor().execute('INSERT INTO employee_visiting (card_number, time_in) VALUES (?, ?)', (card_number, time_in))

    def update_employee_visiting_time_from(self, card_number: int, time_from: str):
        with self.connection as con:
            con.cursor().execute(f'UPDATE employee_visiting SET time_from="{time_from}" WHERE card_number={card_number}')

    def get_employee_visiting(self, card_number) -> list:
        with self.connection as con:
            return con.cursor().execute('SELECT * FROM employee_visiting WHERE card_number=?', (card_number,)).fetchall()

    def add_temp_card(self, card_number: int, first_name: str, second_name: str, phone_number: str, is_active: int, datetime_interval: list):
        with self.connection as con:
            con.cursor().execute('INSERT INTO temp_cards VALUES (?,?,?,?,?,?,?)', (card_number, first_name, second_name, phone_number, is_active, datetime_interval[0], datetime_interval[1]))

    def update_temp_card_active(self, card_number: int, active_status: int):
        with self.connection as con:
            con.cursor().execute(f'UPDATE temp_cards SET is_active={active_status} WHERE card_number={card_number}')

    def get_temp_cards_data(self) -> list:
        with self.connection as con:
            return con.cursor().execute('SELECT * FROM temp_cards').fetchall()

    def get_temp_card_data(self, card_number: int) -> tuple:
        with self.connection as con:
            return con.cursor().execute('SELECT * FROM temp_cards WHERE card_number=?', (card_number,)).fetchone()
