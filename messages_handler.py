from PyQt6.QtWidgets import QMessageBox


class MessageHandler:
    def show_message(self, icon: QMessageBox.Icon, window_title: str, error_message: str):
        error = QMessageBox()
        error.setWindowTitle(window_title)
        error.setIcon(icon)
        error.setText(error_message)
        error.setDefaultButton(QMessageBox.StandardButton.Ok)
        error.exec()