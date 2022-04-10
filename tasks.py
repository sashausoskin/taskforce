from posixpath import abspath
from invoke import task
import os
import PyInstaller.__main__
import platform
from tempfile import mkstemp
from shutil import move, copyfile
from dotenv import load_dotenv
from time import sleep


@task
def init_db(ctx):
    ctx.run("python3 src/create_db_schema.py")

@task
def start(ctx):
    os.chdir(f'{os.getcwd()}/src') #Change the current working directory so that the UI elements are loaded correctly
    ctx.run("python3 index.py", pty=True)

@task
def compile_ui(ctx):
    os.chdir(f'{os.getcwd()}/src')
    ctx.run('pyuic5 -o ui/login_window_ui.py ui/ui_files/login_window.ui')
    ctx.run('pyuic5 -o ui/signup_form_ui.py ui/ui_files/signup_form.ui')
    ctx.run('pyuic5 -o ui/main_window_ui.py ui/ui_files/main_window.ui')
    ctx.run('pyuic5 -o ui/org_join_window_ui.py ui/ui_files/org_join_window.ui')
    ctx.run('pyuic5 -o ui/org_create_form_ui.py ui/ui_files/org_create_form.ui')
    ctx.run('pyuic5 -o ui/new_task_form_ui.py ui/ui_files/new_task_form.ui')

@task
def build(ctx):
    print("Starting build... Please let the task finish or else the program may no longer work")
    sleep(2)

    load_dotenv(".env") #Hardcode the database URL into the code
    DATABASE_URL = os.getenv('DATABASE_URL')
    if not DATABASE_URL:
        print("DATABASE_URL not found!")

    copyfile("src/database_con.py", "src/database_con_backup.py")
    with open("src/database_con_new.py", "w") as new:
        with open("src/database_con.py", "r") as original:
            for line in original:
                new.write(line.replace("DATABASE_URL = os.getenv('DATABASE_URL')", f"DATABASE_URL = '{DATABASE_URL}'"))
    
    os.remove("src/database_con.py")
    move("src/database_con_new.py", "src/database_con.py")

    if platform.system()=="Windows":
        separator=";"
    else:
        separator=":"

    PyInstaller.__main__.run([
        "--windowed",
        "--noconfirm",
        "--icon=src/img/icon.ico",
        "--name=taskforce",
        f'--add-data=src/img/icon.ico{separator}img',
        f'--add-data=src/img/icon.svg{separator}img',
        f'--add-data=src/img/icon.png{separator}img',
        "--hidden-import=plyer.platforms.linux.notification",
        "--hidden-import=plyer.platforms.win.notification",
        "--hidden-import=plyer.platforms.macosx.notification",
        'src/index.py',
    ])

    os.remove("src/database_con.py")
    move("src/database_con_backup.py", "src/database_con.py")


@task
def coverage(ctx):
    ctx.run("coverage run --branch -m pytest src", pty=True)

@task(coverage)
def coverage_report(ctx):
    ctx.run("coverage html", pty=True)

@task
def test(ctx):
    ctx.run("pytest src", pty=True)

@task
def lint(ctx):
    ctx.run("pylint src", pty=True)

@task
def format(ctx):
    ctx.run("autopep8 --in-place --recursive src", pty=True)