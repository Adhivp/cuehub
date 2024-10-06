import os
import json
import click
import pyfiglet
from colorama import init, Fore
from cuehub.commands import django, flask, fastapi, pyramid, tornado 
from cuehub.commands.analyze_project import GeminiAPI2
from cuehub.commands.generate_readme import GeminiAPI
from cuehub.utils.framework_helper import save_user_details, check_existing_user, list_project_contents, read_project_files
import time
from rich.console import Console
from rich.markdown import Markdown
from rich.progress import Progress, SpinnerColumn, TextColumn
from concurrent.futures import ThreadPoolExecutor
from functools import wraps
import random


CONFIG_FILE = '.cuehubconfig'
USER_DATA_FILE = os.path.join(os.path.dirname(__file__), 'user_data.json')

ads = {
    "Django": [
        "Join a thriving community with Django! Collaborate and grow together! 🌍 [Get Involved](https://www.djangoproject.com/)",
        "Protect your app with Django's built-in security features! 🔒 [Secure Your App](https://www.djangoproject.com/)",
        "Need an admin panel? Django's comes out of the box! 🖥️ [Use Django](https://www.djangoproject.com/)",
        "Simplify database interactions with Django's ORM! 💾 [Learn Django](https://www.djangoproject.com/)",
        "Get your project off the ground quickly with Django! 🚀 [Start with Django](https://www.djangoproject.com/)",
        "Use Django's built-in features to save time! ⏱️ [Try Django](https://www.djangoproject.com/)",
        "Save time with Django's out-of-the-box functionalities! ⏳ [Join Django](https://www.djangoproject.com/)",
        "Get everything you need with Django's all-in-one solution! 🏆 [Try It Out](https://www.djangoproject.com/)",
        "Learn easily with Django's comprehensive docs! 📚 [Get Started](https://www.djangoproject.com/)"
    ],
    "Flask": [
        "Say goodbye to complexity! Switch to Flask and do more with less code! 🌟 [Discover Flask](https://flask.palletsprojects.com/en/latest/api/)",
        "Need to prototype fast? Flask lets you create MVPs in record time! ⏳ [Start Prototyping](https://flask.palletsprojects.com/en/latest/api/)",
        "New to web development? Flask's simplicity makes it easy to learn! 📚 [Start Learning](https://flask.palletsprojects.com/en/latest/api/)",
        "Build lightweight applications that deliver! 🌬️ [Build with Flask](https://flask.palletsprojects.com/en/latest/api/)",
        "Integrate with third-party services effortlessly! 🌐 [Use Flask](https://flask.palletsprojects.com/en/latest/api/)",
        "Create RESTful APIs quickly with Flask! 🌟 [Start API Development](https://flask.palletsprojects.com/en/latest/api/)",
        "Perfect for personal projects that require speed! 🚀 [Start Now](https://flask.palletsprojects.com/en/latest/api/)",
        "Tap into a supportive community with Flask! 🤝 [Join Us](https://flask.palletsprojects.com/en/latest/api/)",
        "Simplify your routing with Flask's clean syntax! 🗺️ [Use Flask](https://flask.palletsprojects.com/en/latest/api/)"
    ],
    "FastAPI": [
        "Why settle for slow? FastAPI gets you results in a fraction of the time! ⚡ [Join FastAPI](https://fastapi.tiangolo.com/)",
        "Embrace modern development with FastAPI—built for async programming! 🚀 [Learn More](https://fastapi.tiangolo.com/)",
        "Generate interactive API docs automatically with FastAPI! 📄 [Explore FastAPI](https://fastapi.tiangolo.com/)",
        "Maximize performance with async support in FastAPI! ⚡ [Join FastAPI](https://fastapi.tiangolo.com/)",
        "Define flexible endpoints effortlessly with FastAPI! 🔄 [Discover FastAPI](https://fastapi.tiangolo.com/)",
        "Boost your productivity and deliver faster! 📈 [Get Started](https://fastapi.tiangolo.com/)",
        "Enhance your developer experience with FastAPI! 🌟 [Experience FastAPI](https://fastapi.tiangolo.com/)",
        "Use dependency injection for cleaner code with FastAPI! 🔗 [Join FastAPI](https://fastapi.tiangolo.com/)",
        "Create clean and modern APIs in record time! 📜 [Explore FastAPI](https://fastapi.tiangolo.com/)"
    ],
    "Pyramid": [
        "Stuck in a box? Pyramid opens doors to endless possibilities! 🏗️ [Explore Pyramid](https://trypyramid.com/)",
        "Build exactly what you need with Pyramid's customizable architecture! 🛠️ [Customize Now](https://trypyramid.com/)",
        "Perfect for scaling your large projects with ease! 📈 [Scale with Pyramid](https://trypyramid.com/)",
        "Get started quickly with Pyramid's minimal setup! 🏁 [Start Fast](https://trypyramid.com/)",
        "Tailor your application architecture with Pyramid! 🧩 [Customize Pyramid](https://trypyramid.com/)",
        "Maintain clean, readable code with Pyramid! 📝 [Explore Clean Code](https://trypyramid.com/)",
        "Design your applications modularly with Pyramid! 🧩 [Learn Pyramid](https://trypyramid.com/)",
        "Ideal for complex enterprise solutions! 🏢 [Learn More](https://trypyramid.com/)",
        "Add custom features easily with Pyramid! ✨ [Discover Pyramid](https://trypyramid.com/)"
    ],
    "Tornado": [
        "Overwhelmed by high traffic? Tornado handles thousands of requests with ease! 🔥 [Discover Tornado](https://www.tornadoweb.org/en/stable/)",
        "Build real-time applications without breaking a sweat! 🌐 [Check It Out](https://www.tornadoweb.org/en/stable/)",
        "Experience unmatched performance with Tornado! ⚡ [Discover More](https://www.tornadoweb.org/en/stable/)",
        "Seamlessly integrate WebSockets with Tornado! 💬 [Explore Tornado](https://www.tornadoweb.org/en/stable/)",
        "Create efficient APIs that handle concurrent connections! 🔗 [Discover Tornado](https://www.tornadoweb.org/en/stable/)",
        "Scale your applications to meet high demand! 📊 [Learn More](https://www.tornadoweb.org/en/stable/)",
        "Don't compromise; handle high loads effortlessly with Tornado! 🔥 [Get Started](https://www.tornadoweb.org/en/stable/)",
        "Embrace asynchronous programming with Tornado! ⚙️ [Explore Tornado](https://www.tornadoweb.org/en/stable/)",
        "Experience lightning-fast response times with Tornado! ⚡ [Learn More](https://www.tornadoweb.org/en/stable/)"
    ]
}


def load_user_data():
    """Load user data from JSON file."""
    if os.path.exists(USER_DATA_FILE):
        with open(USER_DATA_FILE, 'r') as f:
            return json.load(f)
    return {}

def save_user_data(data):
    """Save user data to JSON file."""
    with open(USER_DATA_FILE, 'w') as f:
        json.dump(data, f, indent=4)

def update_command_usage(command):
    """Update command usage in user data."""
    user_data = load_user_data()
    user_data.setdefault('commands', {})
    user_data['commands'][command] = user_data['commands'].get(command, 0) + 1
    save_user_data(user_data)

def suggest_ads():
    """Suggest ads based on user command usage."""
    user_data = load_user_data()
    commands = user_data.get('commands', {})
    
    # Suggest an alternative framework based on usage
    if 'django' in commands and commands['django'] > commands.get('flask', 0):
        return random.choice(ads['Flask'])  
    elif 'flask' in commands and commands['flask'] > commands.get('django', 0):
        return random.choice(ads['Django'])  
    # Add more ad suggestions as needed based on other commands


def check_init():
    """Check if CueHub has been initialized in the current directory."""
    return os.path.exists(CONFIG_FILE)

def require_init(f):
    @wraps(f)
    def wrapped(*args, **kwargs):
        if not check_init():
            click.echo("CueHub has not been initialized in this directory. Please run 'cue init' first.")
            return
        return f(*args, **kwargs)
    return wrapped

console = Console() 
@click.group()
def cue():
    # Create ASCII art
    ascii_art = pyfiglet.figlet_format("CueHub")

    # Center the ASCII art
    width = os.get_terminal_size().columns
    centered_ascii_art = "\n".join(line.center(width) for line in ascii_art.splitlines())

    # Print ASCII art in green
    click.echo(Fore.GREEN + centered_ascii_art)

    # Print description centered in green
    description = "CueHub is a developer tool designed to simplify project workflows and enhance productivity."
    centered_description = description.center(width)
    click.echo(Fore.GREEN + centered_description)

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
@require_init
@click.argument('framework', type=click.Choice(['django', 'flask', 'fastapi', 'pyramid', 'tornado'], case_sensitive=False), required=False)
def setup(framework):
    """Setup a project with a chosen framework."""
    if framework:
        # Directly use the specified framework
        click.echo(f'Setting up {framework}...')
        update_command_usage(framework.lower())  # Log the command usage
        if framework.lower() == 'django':
            django.setup_django()
        elif framework.lower() == 'flask':
            flask.setup_flask()
        elif framework.lower() == 'fastapi':
            fastapi.setup_fastapi()
        elif framework.lower() == 'pyramid':
            pyramid.setup_pyramid()
        elif framework.lower() == 'tornado':
            tornado.setup_tornado()
        recommended_ad = suggest_ads()
        click.echo(recommended_ad)
    else:
        # Prompt the user to choose a framework if not specified
        click.echo("Choose a framework to set up:")
        frameworks = ['Django', 'Flask', 'FastAPI', 'Pyramid', 'Tornado']
        choice = click.Choice(frameworks, case_sensitive=False)

        framework_choice = click.prompt('Enter the framework you want to setup', type=choice)

        # Call the respective setup function based on user input
        update_command_usage(framework_choice.lower())  # Log the command usage
        if framework_choice.lower() == 'django':
            django.setup_django()
        elif framework_choice.lower() == 'flask':
            flask.setup_flask()
        elif framework_choice.lower() == 'fastapi':
            fastapi.setup_fastapi()
        elif framework_choice.lower() == 'pyramid':
            pyramid.setup_pyramid()
        elif framework_choice.lower() == 'tornado':
            tornado.setup_tornado()
        else:
            click.echo('Invalid choice! Please try again.')
        recommended_ad = suggest_ads()
        click.echo(recommended_ad)

@cue.command()
@require_init
@click.argument('project_dir', type=click.Path(exists=True))
def analyze_project(project_dir):
    """Analyze the project directory and suggest improvements."""
    def analyze():
        """Function to perform the analysis."""
        contents = list_project_contents(project_dir)  # Assuming this function lists files and directories
        gemini = GeminiAPI2()
        return gemini.analyze_project_structure(contents)

    console = Console()
    
    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        transient=True,
    ) as progress:
        task = progress.add_task("Analyzing project structure...", total=None)
        
        with ThreadPoolExecutor() as executor:
            future = executor.submit(analyze)
            
            while not future.done():
                time.sleep(0.1)  # Sleep briefly to avoid busy-waiting
                progress.update(task, advance=0)  # This keeps the spinner spinning
            
            suggestions = future.result()
    
    # Render and print Markdown using rich
    markdown = Markdown(suggestions)
    console.print(markdown)
    recommended_ad = suggest_ads()
    console.print(recommended_ad,style="bold black on yellow")

@cue.command()
@require_init
@click.argument('project_dir', type=click.Path(exists=True))
def generate_readme(project_dir):
    """Generate a README file for the project."""
    console = Console()
    
    # Ask user if the project is open-source
    is_opensource = click.confirm("Is this project open-source?", default=True)
    
    def generate():
        project_structure = list_project_contents(project_dir)
        
        project_info = f"""
        Project Structure:
        {project_structure}

        Key File Contents:
        {read_project_files(project_dir)}

        This project is {"open-source" if is_opensource else "not open-source"}.
        """
        
        # Send to Gemini API
        gemini = GeminiAPI()
        return gemini.generate_readme(project_info)
    
    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        transient=True,
    ) as progress:
        task = progress.add_task("Generating README...", total=None)
        
        with ThreadPoolExecutor() as executor:
            future = executor.submit(generate)
            
            while not future.done():
                time.sleep(0.1)
                progress.update(task, advance=0)
            
            readme_content = future.result()
    
    # Write README content to file
    readme_path = os.path.join(project_dir, 'README.md')
    with open(readme_path, 'w') as f:
        f.write(readme_content)
    
    console.print(f"[green]README.md has been generated at: {readme_path}[/green]")
    
    # Preview the generated README
    markdown = Markdown(readme_content)
    console.print("\n[bold]Generated README Preview:[/bold]\n")
    console.print(markdown)
    recommended_ad = suggest_ads()
    console.print(recommended_ad,style="bold black on yellow")


if __name__ == "__main__":
    cue()
