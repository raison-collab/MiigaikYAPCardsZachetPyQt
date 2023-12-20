import datetime
import sys
import threading
import time

from PyQt6.QtWidgets import QApplication

from temp_cards_checker import TempCardsChecker
from windows import MainWindow


def check_temp_cards(main_window_: MainWindow):
    temp_cards_checker = TempCardsChecker('data.db', main_window_)
    temp_cards_checker.check_temp_cards()


if __name__ == '__main__':
    app = QApplication(sys.argv)

    main_window = MainWindow()
    thr_1 = threading.Thread(target=check_temp_cards, name='TempCardsChecker', args=(main_window,), daemon=True)

    main_window.show()

    thr_1.start()

    sys.exit(app.exec())
