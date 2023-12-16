from pprint import pprint

from PyQt6 import uic

from PyQt6.QtWidgets import QMainWindow, QPushButton, QLineEdit, QMessageBox

from database_controller import DatabaseController
from messages_handler import MessageHandler
from utils import Util
from validators import FieldValidator


db = DatabaseController('data.db')


class RegWindow(QMainWindow, MessageHandler, FieldValidator):
    def __init__(self):
        super().__init__()

        uic.loadUi('reg_window.ui', self)

        self.first_name_field: QLineEdit = self.findChild(QLineEdit, 'first_name')
        self.second_name_field: QLineEdit = self.findChild(QLineEdit, 'second_name')
        self.card_number_field: QLineEdit = self.findChild(QLineEdit, 'card_number')

        self.reg_button: QPushButton = self.findChild(QPushButton, 'reg_button')

        self.set_events()
        self.set_card_number()

    def set_events(self):
        self.reg_button.clicked.connect(self.register_user)

    def set_card_number(self):
        all_cards_numbers = [row[0] for row in db.get_all_data()]
        card_number = Util.generate_random_card_number([1000, 1_000_000])

        if card_number in all_cards_numbers:
            return self.set_card_number()

        self.card_number_field.setText(str(card_number))

    def register_user(self):
        if not self.valid_fields():
            return self.show_message(QMessageBox.Icon.Critical, 'Ошибка', 'Проверьте правильность ввода данных')

        card_number = int(self.card_number_field.text())
        f_name = self.first_name_field.text()
        s_name = self.second_name_field.text()

        check_employee = db.check_employee_by_card_number(card_number)

        if check_employee:
            return self.show_message(QMessageBox.Icon.Critical, 'Ошибка', 'Пользователь с таким номером пропуска существует')

        db.add_employee(card_number, f_name, s_name)

        self.show_message(QMessageBox.Icon.Information, 'Успешная регистрация', 'Пользователь успешно зарегистрирован')
        self.close()
        self.clear_fields()

    def clear_fields(self):
        self.first_name_field.clear()
        self.second_name_field.clear()
        self.card_number_field.clear()

    def valid_fields(self) -> bool:
        card_number_text = self.card_number_field.text().strip()
        first_name_text = self.first_name_field.text().strip()
        second_name_text = self.second_name_field.text().strip()

        if (not len(first_name_text) or len(first_name_text.split()) > 1) or \
                (not len(second_name_text) or len(second_name_text.split()) > 1) or \
                (len(card_number_text.split()) > 1 or not card_number_text.isdigit()):
            return False

        return True


class MainWindow(QMainWindow, MessageHandler, FieldValidator):
    def __init__(self):
        super().__init__()

        uic.loadUi('main_window.ui', self)

        self.reg_button: QPushButton = self.findChild(QPushButton, 'RegButton')
        self.access_employee_button: QPushButton = self.findChild(QPushButton, 'access_employee_button')

        self.card_number_field: QLineEdit = self.findChild(QLineEdit, 'card_number')

        self.set_events()

        self.reg_window = None

    def set_events(self):
        self.reg_button.clicked.connect(self.show_reg_window)
        self.access_employee_button.clicked.connect(self.access_employee)

    def access_employee(self):
        if not self.valid_fields():
            return self.show_message(QMessageBox.Icon.Critical, 'Ошибка', 'Проверьте правильность ввода данных')

        card_number = int(self.card_number_field.text())
        check_employee = db.check_employee_by_card_number(card_number)

        if not check_employee:
            return self.show_message(QMessageBox.Icon.Critical, 'Ошибка', 'Данного пользователя не существует')

        # todo Update field with time in DB
        employee_data = db.get_employee_by_card_number(card_number)

        self.show_message(QMessageBox.Icon.Information, 'Информация о сотруднике', f'Номер пропуска: {employee_data[0]}\nИмя: {employee_data[1]}\nФамилия: {employee_data[2]}')

        self.clear_fields()

    def valid_fields(self):
        card_number_text = self.card_number_field.text()
        if len(card_number_text.split()) > 1 or not card_number_text.isdigit():
            return False
        return True

    def clear_fields(self):
        self.card_number_field.clear()

    def show_reg_window(self):
        self.reg_window = RegWindow()
        self.reg_window.show()
