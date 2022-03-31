import sys
from PyQt5.QtWidgets import QApplication
from ui.login_form import loginWindow

app = QApplication(sys.argv)


win = loginWindow()
win.show()
sys.exit(app.exec())
