import sys

from PyQt5.QtWidgets import QApplication
app = QApplication(sys.argv)
from ui.login_form import loginWindow




win = loginWindow()
win.show()
sys.exit(app.exec())
