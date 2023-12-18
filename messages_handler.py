from PyQt6.QtWidgets import QMessageBox


class MessageHandler:
    def show_message(self, icon: QMessageBox.Icon, window_title: str, message: str):
        error = QMessageBox()
        error.setWindowTitle(window_title)
        error.setIcon(icon)
        error.setText(message)
        error.setDefaultButton(QMessageBox.StandardButton.Ok)
        error.exec()