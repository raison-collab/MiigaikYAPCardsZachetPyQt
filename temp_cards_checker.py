import datetime
import sqlite3
import time

from PyQt6.QtWidgets import QMessageBox
from dateutil.parser import parse

from database_controller import DatabaseController
from messages_handler import MessageHandler
from windows import MainWindow


class TempCardsChecker(DatabaseController):
    def __init__(self, database_path: str, message_handler: MessageHandler):
        super().__init__(database_path)

        self.window = message_handler

    def check_temp_cards(self):
        while True:
            cards = self.get_temp_cards_data()
            if cards: cards = [el for el in cards if el[4]]
            else: continue

            for card in cards:
                if datetime.datetime.now() >= parse(card[-1]):
                    self.update_temp_card_active(card[0], 0)

                    report_message = (f'Временный пропуск истек. Обратитесь к старшему охраннику!\n'
                                      f'Инфорация о сотруднике:\n'
                                      f'Номер пропуска: {card[0]}\n'
                                      f'Имя: {card[1]}\n'
                                      f'Фамилия: {card[2]}\n'
                                      f'Номер телефона: {card[3]}\n'
                                      f'Время прибытия: {card[5]}\n'
                                      f'Пропуск годен до: {card[6]}')

                    self.window.show_message(QMessageBox.Icon.Critical, 'Истек временный пропуск', report_message)

            time.sleep(3)

