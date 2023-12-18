import sys

from PyQt6.QtWidgets import QApplication

from windows import MainWindow

if __name__ == '__main__':
    app = QApplication(sys.argv)

    main_window = MainWindow()
    main_window.show()

    sys.exit(app.exec())