import datetime
import re
from datetime import timedelta
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
        temp_cards_data = db.get_temp_cards_data()
        all_cards_numbers = [row[0] for row in db.get_all_data_employee_cards()] + [row[0] for row in temp_cards_data if temp_cards_data]
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
            return self.show_message(QMessageBox.Icon.Critical, 'Ошибка',
                                     'Пользователь с таким номером пропуска существует')

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
        birthday_text = self.birthday_field.text().strip().replace('.', '/')
        jobtitle_text = self.jobtitle_field.text().strip()
        phone_number_text = self.phone_number_field.text().strip().replace('+', '')
        mail_text = self.mail_field.text().strip()

        check_card_number = (not self.is_empty(card_number_text) and self.count_words(
            card_number_text) == 1 and card_number_text.isdigit())
        check_f_name = (not self.is_empty(first_name_text) and self.count_words(first_name_text) == 1)
        check_s_name = (not self.is_empty(second_name_text) and self.count_words(second_name_text) == 1)
        check_l_name = (not self.is_empty(last_name_text) and self.count_words(last_name_text) == 1)
        check_birthday = False if re.match(r'(0?[1-9]|[12][0-9]|3[01]).(0?[1-9]|1[012]).((19|20)\d\d)',
                                           birthday_text) is None or self.count_words(birthday_text) > 1 else True
        check_jobtitle = (not self.is_empty(jobtitle_text) and self.count_words(jobtitle_text) == 1)
        check_phone_number = False if re.match(r'((8|\+7)[\- ]?)?(\(?\d{3}\)?[\- ]?)?[\d\- ]{7,10}',
                                               phone_number_text) is None or self.count_words(
            phone_number_text) > 1 or len(phone_number_text) != 11 or not phone_number_text.isdigit() else True
        check_mail = False if re.match(r'([a-zA-Z0-9._-]+@[a-zA-Z0-9._-]+\.[a-zA-Z0-9_-]+)',
                                       mail_text) is None or self.count_words(mail_text) > 1 else True

        return True if (
                    check_card_number and check_f_name and check_s_name and check_l_name and check_birthday and check_jobtitle and check_phone_number and check_mail) else False


class TempCardWindow(QMainWindow, MessageHandler, FieldValidator):
    def __init__(self):
        super().__init__()

        uic.loadUi('temp_card_window.ui', self)

        self.first_name_field: QLineEdit = self.findChild(QLineEdit, 'first_name')
        self.second_name_field: QLineEdit = self.findChild(QLineEdit, 'second_name')
        self.card_number_field: QLineEdit = self.findChild(QLineEdit, 'card_number')
        self.phone_number_field: QLineEdit = self.findChild(QLineEdit, 'phone_number')

        self.access_button: QPushButton = self.findChild(QPushButton, 'access_button')

        self.time_ = 4  # время на которое выдается пропуск

        self.set_events()
        self.set_card_number()

    def set_events(self):
        self.access_button.clicked.connect(self.issue_temp_card)

    def set_card_number(self):
        temp_cards_data = db.get_temp_cards_data()
        all_cards_numbers = [row[0] for row in db.get_all_data_employee_cards()] + [row[0] for row in temp_cards_data if temp_cards_data]
        card_number = Util.generate_random_card_number([1000, 1_000_000])

        if card_number in all_cards_numbers:
            return self.set_card_number()

        self.card_number_field.setText(str(card_number))

    def issue_temp_card(self):
        if not self.valid_fields():
            return self.show_message(QMessageBox.Icon.Critical, 'Ошибка', 'Проверьте правильность ввода данных')

        f_name_text = self.first_name_field.text().strip()
        s_name_text = self.second_name_field.text().strip()
        card_number_text = self.card_number_field.text().strip()
        p_number_text = self.phone_number_field.text().strip()

        datetime_now = datetime.datetime.now()

        date_time_in = datetime_now.strftime('%d/%m/%Y %H:%M:%S')
        date_time_out = (datetime_now + timedelta(hours=self.time_)).strftime('%d/%m/%Y %H:%M:%S')

        report_message = (f'Имя: {f_name_text}\n'
                          f'Фамилия: {s_name_text}\n'
                          f'Номер пропуска: {card_number_text}\n'
                          f'Номер телефона: {p_number_text}\n'
                          f'Время входа: {date_time_in}\n'
                          f'Время выхода: {date_time_out}\n')

        db.add_temp_card(int(card_number_text), f_name_text, s_name_text, p_number_text, 1, [date_time_in, date_time_out])

        self.show_message(QMessageBox.Icon.Information, 'Временный пропуск добавлен', report_message)

        self.close()

    def valid_fields(self) -> bool:
        f_name_text = self.first_name_field.text().strip()
        s_name_text = self.second_name_field.text().strip()
        card_number_text = self.card_number_field.text().strip()
        phone_number_text = self.phone_number_field.text().strip().replace('+', '')

        check_f_name = (not self.is_empty(f_name_text) and self.count_words(f_name_text) == 1)
        check_s_name = (not self.is_empty(s_name_text) and self.count_words(s_name_text) == 1)
        check_card_number = (not self.is_empty(card_number_text) and self.count_words(card_number_text) == 1 and card_number_text.isdigit())
        check_phone_number = False if re.match(r'((8|\+7)[\- ]?)?(\(?\d{3}\)?[\- ]?)?[\d\- ]{7,10}',
                                               phone_number_text) is None or self.count_words(
            phone_number_text) > 1 or len(phone_number_text) != 11 or not phone_number_text.isdigit() else True

        return check_f_name and check_s_name and check_card_number and check_phone_number

    def clear_fields(self):
        self.first_name_field.clear()
        self.second_name_field.clear()
        self.card_number_field.clear()
        self.phone_number_field.clear()


class ParkingTicketWindow(QMainWindow, FieldValidator, MessageHandler):
    def __init__(self):
        super().__init__()

        uic.loadUi('parking_ticket_window.ui', self)

        self.employee_allocated_places = 0  # кол-во выданных талонов для сотрудников
        self.guest_allocated_places = 0  # кол-во выданных талонов для гостей

        self.for_guest_places = 10  # кол-во мест для гостей
        self.for_employee_places = 30  # кол-во мест для сотрудников

        self.for_employee_button: QPushButton = self.findChild(QPushButton, 'employee_button')
        self.for_guest_button: QPushButton = self.findChild(QPushButton, 'guest_button')
        self.info_places_button: QPushButton = self.findChild(QPushButton, 'info_places_button')

        self.set_events()

    def update_employee_places(self):
        self.for_employee_places = 30 + self.for_guest_places - self.guest_allocated_places

    def set_events(self):
        self.for_employee_button.clicked.connect(self.issue_employee_ticket)
        self.for_guest_button.clicked.connect(self.issue_guest_ticket)
        self.info_places_button.clicked.connect(self.get_info_places)

    def issue_employee_ticket(self):
        if self.employee_allocated_places == self.for_employee_places:
            return self.show_message(QMessageBox.Icon.Warning, 'Свободных мест нет', 'Свободных мест на парковке нет')

        self.employee_allocated_places += 1

        self.update_employee_places()

        report_message = f'Свободные места для сотрудников: {self.for_employee_places - self.employee_allocated_places}/{self.for_employee_places}\n'

        return self.show_message(QMessageBox.Icon.Information, 'Талон для сотрудника выдан', report_message)

    def issue_guest_ticket(self):
        if self.guest_allocated_places == self.for_guest_places:
            return self.show_message(QMessageBox.Icon.Warning, 'Свободных мест нет', 'Свободных мест на парковке нет')

        self.guest_allocated_places += 1

        self.update_employee_places()

        report_message = f'Свободные места для гостей: {self.for_guest_places - self.guest_allocated_places}/{self.for_guest_places}'

        return self.show_message(QMessageBox.Icon.Information, ' Талон для гостя выдан', report_message)

    def get_info_places(self):
        report_message = (f'Свободные места для сотрудников: {self.for_employee_places - self.employee_allocated_places}/{self.for_employee_places}\n'
                          f'Свободные места для гостей: {self.for_guest_places - self.guest_allocated_places}/{self.for_guest_places}')

        return self.show_message(QMessageBox.Icon.Information, 'Информация о местах', report_message)


class MainWindow(QMainWindow, MessageHandler, FieldValidator):
    def __init__(self):
        super().__init__()

        uic.loadUi('main_window.ui', self)

        self.reg_button: QPushButton = self.findChild(QPushButton, 'RegButton')
        self.access_employee_button: QPushButton = self.findChild(QPushButton, 'access_employee_button')
        self.out_employee_button: QPushButton = self.findChild(QPushButton, 'out_employee_button')
        self.issue_temp_card_button: QPushButton = self.findChild(QPushButton, 'temp_card_button')
        self.issue_parking_ticket_button: QPushButton = self.findChild(QPushButton, 'parking_ticket_button')

        self.card_number_field: QLineEdit = self.findChild(QLineEdit, 'card_number')

        self.set_events()

        self.reg_window = None
        self.temp_card_window = None
        self.parking_ticket_window = None

    def set_events(self):
        self.reg_button.clicked.connect(self.show_reg_window)
        self.access_employee_button.clicked.connect(self.access_employee)
        self.out_employee_button.clicked.connect(self.out_employee)
        self.issue_temp_card_button.clicked.connect(self.show_temp_card_window)
        self.issue_parking_ticket_button.clicked.connect(self.show_parking_ticket_window)

    def access_employee(self):
        if not self.valid_fields():
            return self.show_message(QMessageBox.Icon.Critical, 'Ошибка', 'Проверьте правильность ввода данных')

        card_number = int(self.card_number_field.text())
        check_employee = db.check_employee_by_card_number(card_number)

        if not check_employee:
            return self.show_message(QMessageBox.Icon.Critical, 'Ошибка', 'Данного пользователя не существует')

        employee_data = db.get_employee_by_card_number(card_number)
        date_time_in = datetime.datetime.now().strftime('%d/%m/%Y %H:%M:%S')

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

        if not self.valid_fields():
            return self.show_message(QMessageBox.Icon.Critical, 'Ошибка', 'Проверьте правильность ввода данных')

        date_time_out = datetime.datetime.now().strftime('%d/%m/%Y %H:%M:%S')
        card_number = int(self.card_number_field.text())

        temp_card_data = db.get_temp_card_data(card_number)
        if temp_card_data:
            if not temp_card_data[4]:
                return self.show_message(QMessageBox.Icon.Warning, 'Неактивный пропуск', 'Пропуск данного пользователя неактивен. Обратитесь к старшему охраннику')
            else:
                report_message = (f'Номер временного пропуска: {temp_card_data[0]}\n'
                                  f'Имя: {temp_card_data[1]}\n'
                                  f'Фамилия: {temp_card_data[2]}\n'
                                  f'Номер телефона: {temp_card_data[3]}\n'
                                  f'Время входа: {temp_card_data[5]}\n'
                                  f'Время выхода: {temp_card_data[6]}\n')

                db.update_temp_card_active(card_number, 0)

                self.clear_fields()

                return self.show_message(QMessageBox.Icon.Information, 'Временный пропуск', report_message)

        if not db.check_employee_by_card_number(card_number):
            return self.show_message(QMessageBox.Icon.Critical, 'Ошибка', 'Данного пользователя не существует')

        employee_visiting = db.get_employee_visiting(card_number)[-1] if db.check_employee_in_visitors(card_number) else [False]  # связано с проверкой ниже, чтобы не переписывать код, сделал костыль)

        if employee_visiting[-1] is not None:
            return self.show_message(QMessageBox.Icon.Critical, 'Ошибка', 'Данный сотрудник не заходил на территорию')

        db.update_employee_visiting_time_from(card_number, date_time_out)

        employee_data = db.get_employee_by_card_number(card_number)
        employee_visiting = db.get_employee_visiting(card_number)[-1]
        time_diff = Util.calc_time_different(*employee_visiting[1:])

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

    def show_temp_card_window(self):
        self.temp_card_window = TempCardWindow()
        self.temp_card_window.show()

    def show_parking_ticket_window(self):
        self.parking_ticket_window = ParkingTicketWindow()
        self.parking_ticket_window.show()
