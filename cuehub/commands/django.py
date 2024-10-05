import click
from cuehub.utils.framework_helper import check_and_create_virtualenv, install_package
import subprocess


def setup_django():
    """Sets up a Django project."""
    project_name = click.prompt('Enter your Django project name', type=str)

    # Check and create virtual environment based on project name
    venv_name = f"{project_name}_venv"
    check_and_create_virtualenv(venv_name)

    # Install Django inside the virtual environment
    install_package('django', venv_name)

    # Start a new Django project inside the current directory
    click.echo(f'Starting Django project: {project_name}...')
    subprocess.run([f'{venv_name}/bin/django-admin', 'startproject', project_name])

    click.echo(f'Django project "{project_name}" setup complete!')

    # Guide the user on the next steps
    click.echo(f'\nNext steps to get started with your Django project "{project_name}":')
    click.echo(f'1. Activate your virtual environment: source {venv_name}/bin/activate')
    click.echo(f'2. Change into your project directory: cd {project_name}')
    click.echo(f'3. Run the development server: python manage.py runserver\n')
    click.echo(f'Enjoy building your Django app!')