import sys
import PyQt5.QtWidgets
from ui.login_form import loginWindow

app = PyQt5.QtWidgets.QApplication(sys.argv)


win = loginWindow()
win.show()
sys.exit(app.exec())
