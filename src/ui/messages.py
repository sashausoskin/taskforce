from PyQt5.QtWidgets import QMessageBox


def error(title, message):
    msg = QMessageBox()
    msg.setIcon(QMessageBox.Critical)
    msg.setText(message)
    msg.setWindowTitle(title)
    msg.exec_()

def success(title, message):
    msg = QMessageBox()
    msg.setIcon(QMessageBox.Information)
    msg.setText(message)
    msg.setWindowTitle(title)
    msg.exec_()