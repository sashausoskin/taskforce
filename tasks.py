from invoke import task
import os
import PyInstaller.__main__
import platform


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