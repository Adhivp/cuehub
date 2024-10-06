import os
import json
import click
import subprocess
import shutil

CONFIG_FILE = '.cuehubconfig'

def check_existing_user():
    """Check if the config file exists and has user details."""
    return os.path.exists(CONFIG_FILE)

def save_user_details(name, email, project_name):
    """Save user details and project name to the config file."""
    user_data = {
        'name': name,
        'email': email,
        'project_name': project_name
    }
    
    with open(CONFIG_FILE, 'w') as config_file:
        json.dump(user_data, config_file)
    os.system(f'chmod 600 {CONFIG_FILE}')

def load_user_details():
    """Load the saved user details from the config file."""
    if check_existing_user():
        with open(CONFIG_FILE, 'r') as config_file:
            user_data = json.load(config_file)
        return user_data
    return None

def check_and_create_virtualenv(venv_name):
    """Check if the virtual environment exists, and create one if it doesn't."""
    if not os.path.exists(venv_name):
        click.echo(f'Creating virtual environment "{venv_name}"...')
        subprocess.run(['python3', '-m', 'venv', venv_name])
        click.echo(f'Virtual environment "{venv_name}" created successfully!')
    else:
        click.echo(f'Virtual environment "{venv_name}" already exists.')

def install_package(package_name, venv_name):
    """Install a package in the specified virtual environment."""
    click.echo(f'Installing {package_name}...')
    subprocess.run([f'{venv_name}/bin/pip', 'install', package_name])
    click.echo(f'{package_name} installed successfully!')

def copy_template(template_path, destination):
    """Copy template files from the template path to the destination."""
    if os.path.exists(template_path):
        shutil.copytree(template_path, destination, dirs_exist_ok=True)
        click.echo(f'Template files copied from {template_path} to {destination}.')
    else:
        click.echo(f'Template path {template_path} does not exist. Unable to copy template files.')

def read_project_name():
    """Read the project name from the config file."""
    if check_existing_user():
        user_data = load_user_details()
        project_name = user_data.get('project_name')
        if project_name:
            click.echo(f'Project name: {project_name}')
            return project_name
        else:
            click.echo('Project name not found in the config file.')
            return None
    else:
        click.echo('Config file does not exist. Please run "cue init" first.')
        return None
    
def list_project_contents(project_dir):
    """Return all the directories and files in the specified project directory."""
    project_contents = {}

    for root, dirs, files in os.walk(project_dir):
        project_contents[root] = {
            'directories': dirs,
            'files': files
        }

    return project_contents
