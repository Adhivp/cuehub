import click

@click.group()
def cli():
    """Git Command Helper."""
    pass

def pull():
    """Explains the git pull command process."""
    click.echo("git pull: Fetches and merges changes from the remote repository to the current branch.")
    click.echo("\nProcess of git pull:")
    click.echo("1. git fetch origin")
    click.echo("2. git merge origin")
    click.echo("Optional step:")
    click.echo("3. git stash")
    click.echo("4. git pull origin main/master")

def push():
    """Explains the git push command process."""
    click.echo("git push: Uploads local commits to the remote repository.")
    click.echo("\nProcess of git push:")
    click.echo("1. git add .")
    click.echo("2. git commit -m 'Your message'.")
    click.echo("3. git push origin master/main.")

def revert():
    """Explains the git revert command process."""
    click.echo("git revert: Creates a new commit that undoes changes introduced by a specific commit.")
    click.echo("\nProcess of git revert:")
    click.echo("1. Identify the commit you want to revert: git log.")
    click.echo("2. Revert the changes: git revert <commit_hash>.")
    click.echo("3. Push the reverted changes: git push origin <branch_name>.")

def hard_reset():
    """Explains the git reset --hard command process."""
    click.echo("git reset --hard: Resets the working directory and index to a specific commit, discarding all changes.")
    click.echo("\nProcess of git reset --hard:")
    click.echo("1. Identify the commit you want to reset to: git log.")
    click.echo("2. Reset to that commit: git reset --hard <commit_hash>.")
    click.echo("Caution: This will discard all local changes!")

def show():
    """Lists all important Git commands with explanations."""
    click.echo("\nGit Command List:")
    click.echo("1. git pull: Fetch and merge changes from the remote repository.")
    click.echo("2. git push: Push your local commits to the remote repository.")
    click.echo("3. git revert: Create a commit that reverses the effects of an earlier commit.")
    click.echo("4. git reset --hard: Reset the working directory and index to a specific commit, discarding all changes.")
    click.echo("\nUse `git show <command>` to get more details about a specific Git command.")

@cli.command()
@click.argument('command', type=click.Choice(['pull', 'push', 'revert', 'reset'], case_sensitive=False))
def git_show(command):
    """Show details of a specific Git command."""
    if command == 'pull':
        pull()
    elif command == 'push':
        push()
    elif command == 'revert':
        revert()
    elif command == 'reset':
        hard_reset()

if __name__ == '__main__':
    cli()
