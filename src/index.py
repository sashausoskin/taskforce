import sys
import platform
import ctypes
from PyQt5.QtWidgets import QApplication
from ui.login_form import loginWindow


if platform.system() == "Windows":  # This is required for the taskbar icon to work
    MYAPPID = 'sonicsasha.taskforce.build.version1'
    ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(MYAPPID)

app = QApplication(sys.argv)


win = loginWindow()
win.show()
sys.exit(app.exec())
