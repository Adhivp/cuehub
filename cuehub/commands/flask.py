import os
import click
from cuehub.utils.framework_helper import check_and_create_virtualenv, install_package, copy_template,read_project_name
import subprocess

def setup_flask():
    """Sets up a Flask environment with basic configurations."""
    project_name = read_project_name()  # Read project name from config

    if project_name is None:
        click.echo('Unable to set up Flask project. Please run "cue init" to initialize first.')
        return

    # Check and create virtual environment based on project name
    venv_name = f"{project_name}_venv"
    check_and_create_virtualenv(venv_name)

    # Install Flask inside the virtual environment
    install_package('flask', venv_name)

    # Copy Flask template files from the templates folder
    click.echo(f'Creating Flask project structure for "{project_name}"...')
    os.makedirs(project_name, exist_ok=True)
    template_path = os.path.join(os.path.dirname(__file__), '..', 'templates', 'flask_template')
    copy_template(template_path, project_name)

    click.echo(f'Flask project "{project_name}" setup complete!')

    # Guide the user on the next steps
    click.echo(f'\nNext steps to get started with your Flask project "{project_name}":')
    click.echo(f'1. Activate your virtual environment: source {venv_name}/bin/activate')
    click.echo(f'2. Change into your project directory: cd {project_name}')
    click.echo(f'3. Run the Flask app: flask run\n')
    click.echo(f'Enjoy building your Flask app!')
