import os
import click
from cuehub.commands import django, flask
from cuehub.utils.framework_helper import save_user_details, check_existing_user

@click.group()
def cue():
    """CueHub CLI - Setup frameworks like Django, Flask, etc."""
    pass

@cue.command()
def init():
    """Initializes CueHub in the current folder."""
    
    # Check if user details exist, if not prompt for user details
    if not check_existing_user():
        click.echo('Welcome to CueHub! Let\'s set things up.')

        name = click.prompt('Enter your name', type=str)
        email = click.prompt('Enter your email', type=str)
        project_name = click.prompt('Enter your project name', type=str)

        save_user_details(name, email, project_name)
        click.echo(f'Project "{project_name}" initialized successfully with your details!')

    else:
        click.echo('CueHub is already initialized with your details.')

@cue.command()
def setup_django():
    """Sets up a Django project."""
    django.setup_django()

@cue.command()
def setup_flask():
    """Sets up a Flask project."""
    flask.setup_flask()
