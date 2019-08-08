import click
import sys

from .config import Config


@click.command()
@click.argument('file_path', type=click.Path(exists=True))
def run(file_path):
    config = Config(file_path)
    error = config.validate()
    if error:
        click.echo(f"Error loading config: {error}")
        sys.exit(1)

    # continue the process
    click.echo(f"Starting to copy the data...")
