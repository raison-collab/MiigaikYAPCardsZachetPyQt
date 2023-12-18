import datetime
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
        self.last_name_field: QLineEdit = self.findChild(QLineEdit, 'last_name')
        self.birthday_field: QLineEdit = self.findChild(QLineEdit, 'birthday')
        self.jobtitle_field: QLineEdit = self.findChild(QLineEdit, 'jobtitle')
        self.phone_number_field: QLineEdit = self.findChild(QLineEdit, 'phone_number')
        self.mail_field: QLineEdit = self.findChild(QLineEdit, 'mail')

        self.reg_button: QPushButton = self.findChild(QPushButton, 'reg_button')

        self.set_events()
        self.set_card_number()

    def set_events(self):
        self.reg_button.clicked.connect(self.register_user)

    def set_card_number(self):
        all_cards_numbers = [row[0] for row in db.get_all_data_employee_cards()]
        card_number = Util.generate_random_card_number([1000, 1_000_000])

        if card_number in all_cards_numbers:
            return self.set_card_number()

        self.card_number_field.setText(str(card_number))

    def register_user(self):
        if not self.valid_fields():
            return self.show_message(QMessageBox.Icon.Critical, 'Ошибка', 'Проверьте правильность ввода данных')

        card_number = int(self.card_number_field.text().strip())
        f_name = self.first_name_field.text().strip()
        s_name = self.second_name_field.text().strip()
        l_name = self.last_name_field.text().strip()
        birthday = self.birthday_field.text().strip()
        jobtitle = self.jobtitle_field.text().strip()
        p_number = self.phone_number_field.text().strip()
        mail = self.mail_field.text().strip()

        check_employee = db.check_employee_by_card_number(card_number)

        if check_employee:
            return self.show_message(QMessageBox.Icon.Critical, 'Ошибка', 'Пользователь с таким номером пропуска существует')

        db.add_employee((card_number, f_name, s_name, l_name, birthday, jobtitle, p_number, mail))

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
        last_name_text = self.last_name_field.text().strip()
        birthday_text = self.birthday_field.text().strip()
        jobtitle_text = self.jobtitle_field.text().strip()
        phone_number_text = self.phone_number_field.text().strip()
        mail_text = self.mail_field.text().strip()

        if (not len(first_name_text) or len(first_name_text.split()) > 1) or \
                (not len(second_name_text) or len(second_name_text.split()) > 1) or \
                (not len(last_name_text) or len(last_name_text.split()) > 1) or \
                (not len(birthday_text) or len(birthday_text.split()) > 1) or \
                (not len(jobtitle_text) or len(jobtitle_text.split()) > 1) or \
                (not len(phone_number_text) or len(phone_number_text.split()) > 1) or \
                (not len(mail_text) or len(mail_text.split()) > 1) or \
                (len(card_number_text.split()) > 1 or not card_number_text.isdigit()):
            return False

        return True


class MainWindow(QMainWindow, MessageHandler, FieldValidator):
    def __init__(self):
        super().__init__()

        uic.loadUi('main_window.ui', self)

        self.reg_button: QPushButton = self.findChild(QPushButton, 'RegButton')
        self.access_employee_button: QPushButton = self.findChild(QPushButton, 'access_employee_button')
        self.out_employee_button: QPushButton = self.findChild(QPushButton, 'out_employee_button')

        self.card_number_field: QLineEdit = self.findChild(QLineEdit, 'card_number')

        self.set_events()

        self.reg_window = None

    def set_events(self):
        self.reg_button.clicked.connect(self.show_reg_window)
        self.access_employee_button.clicked.connect(self.access_employee)
        self.out_employee_button.clicked.connect(self.out_employee)

    def access_employee(self):
        if not self.valid_fields():
            return self.show_message(QMessageBox.Icon.Critical, 'Ошибка', 'Проверьте правильность ввода данных')

        card_number = int(self.card_number_field.text())
        check_employee = db.check_employee_by_card_number(card_number)

        if not check_employee:
            return self.show_message(QMessageBox.Icon.Critical, 'Ошибка', 'Данного пользователя не существует')

        # todo Update field with time in DB
        employee_data = db.get_employee_by_card_number(card_number)
        date_time_in = datetime.datetime.now().strftime('%d.%m.%Y %H:%M:%S')

        db.add_employee_visiting_time_in(card_number, date_time_in)

        report_message = (f'Номер пропуска: {employee_data[0]}\n'
                          f'Имя: {employee_data[1]}\n'
                          f'Фамилия: {employee_data[2]}\n'
                          f'Отчество: {employee_data[3]}\n'
                          f'Дата рождения: {employee_data[4]}\n'
                          f'Должность: {employee_data[5]}\n'
                          f'Номер телефона: {employee_data[6]}\n'
                          f'Почта: {employee_data[7]}\n'
                          f'Последнее Прибытие: {date_time_in}\n')

        self.show_message(QMessageBox.Icon.Information, 'Информация о сотруднике', report_message)

        self.clear_fields()

    def out_employee(self):
        date_time_out = datetime.datetime.now().strftime('%d.%m.%Y %H:%M:%S')
        card_number = int(self.card_number_field.text())

        if not db.check_employee_by_card_number(card_number):
            return self.show_message(QMessageBox.Icon.Critical, 'Ошибка', 'Данного пользователя не существует')

        employee_visiting = db.get_employee_visiting(card_number)[-1] if db.check_employee_in_visitors(card_number) else [False]  # связано с проверкой в строке 151, чтобы не переписывать код, сделал костыль)

        if employee_visiting[-1] is not None:
            return self.show_message(QMessageBox.Icon.Critical, 'Ошибка', 'Данный сотрудник не заходил на территорию')

        db.add_employee_visiting_time_from(card_number, date_time_out)

        employee_data = db.get_employee_by_card_number(card_number)
        employee_visiting = db.get_employee_visiting(card_number)[-1]
        time_diff = Util.calc_time_different(*employee_visiting[1:])

        # todo Доработать базу данных в коде

        report_message = (f'Номер пропуска: {employee_data[0]}\n'
                          f'Имя: {employee_data[1]}\n'
                          f'Фамилия: {employee_data[2]}\n'
                          f'Отчество: {employee_data[3]}\n'
                          f'Дата рождения: {employee_data[4]}\n'
                          f'Должность: {employee_data[5]}\n'
                          f'Номер телефона: {employee_data[6]}\n'
                          f'Почта: {employee_data[7]}\n'
                          f'Последнее Прибытие: {employee_visiting[1]}\n'
                          f'Ушел: {employee_visiting[2]}\n'
                          f'Провел времени на территории: {time_diff}')

        self.show_message(QMessageBox.Icon.Information, 'Информация о сотруднике', report_message)

        self.clear_fields()

    def valid_fields(self):
        card_number_text = self.card_number_field.text()
        if len(card_number_text.split()) > 1 or not card_number_text.isdigit() or not len(card_number_text):
            return False
        return True

    def clear_fields(self):
        self.card_number_field.clear()

    def show_reg_window(self):
        self.reg_window = RegWindow()
        self.reg_window.show()
