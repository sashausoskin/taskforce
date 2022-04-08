import sys
from PyQt5.QtWidgets import QApplication
from ui.login_form import loginWindow
import platform
import ctypes

if platform.system()=="Windows": #This is required for the taskbar icon to work
    myappid = u'sonicsasha.taskforce.build.version1'
    ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(myappid)

app = QApplication(sys.argv)


win = loginWindow()
win.show()
sys.exit(app.exec())
