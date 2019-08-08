import sys

import click

from .config import build_config


@click.command()
@click.argument('file_path', type=click.Path(exists=True))
def run(file_path):
    config, error = build_config(file_path)
    if error:
        click.echo(f"Error loading config: {error}")
        sys.exit(1)

    # continue the process
    click.echo(f"Starting to copy the data...")
