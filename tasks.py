from invoke import task
import os

@task
def test(ctx):
    print("This works!")

@task
def init_db(ctx):
    ctx.run("python3 src/create_db_schema.py")

@task
def start(ctx):
    os.chdir(f'{os.getcwd()}/src') #Change the current working directory so that the UI elements are loaded correctly
    ctx.run("python3 login_form.py", pty=True)