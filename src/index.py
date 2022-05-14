import sys
import platform
import ctypes
from PyQt5.QtWidgets import QApplication
from services.user_service import WrongCredentials, user_service
from ui.login_form import loginWindow
import config


if platform.system() == "Windows":  # This is required for the taskbar icon to work
    MYAPPID = 'sonicsasha.taskforce.build.version1'
    ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(MYAPPID)

app = QApplication(sys.argv)

ini = config.get_config()
win = loginWindow()

try:
    user_service.login(ini["AUTO_LOGIN"]["username"],
                       ini["AUTO_LOGIN"]["password"])
    win.usernameFill.setText(ini["AUTO_LOGIN"]["username"])
    win.passwordFill.setText(ini["AUTO_LOGIN"]["password"])
    win.login()
except (KeyError, WrongCredentials):
    ini["AUTO_LOGIN"]["username"] = ""
    ini["AUTO_LOGIN"]["password"] = ""
    config.save_changes()

    win.show()


sys.exit(app.exec())
