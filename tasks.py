from invoke import task
import os
import PyInstaller.__main__


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
    ctx.run('pyuic5 -o ui/login_window_ui.py ui/login_window.ui')
    ctx.run('pyuic5 -o ui/signup_form_ui.py ui/signup_form.ui')
    ctx.run('pyuic5 -o ui/main_window_ui.py ui/main_window.ui')
    ctx.run('pyuic5 -o ui/org_join_window_ui.py ui/org_join_window.ui')
    ctx.run('pyuic5 -o ui/org_create_form_ui.py ui/org_create_form.ui')

@task
def build(ctx):
    PyInstaller.__main__.run([
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