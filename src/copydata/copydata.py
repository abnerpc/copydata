import json
import click


class Config:
    config = None
    valid_sources = ("html-source",)
    valid_targets = ("database-target",)

    def __init__(self, path):
        with open(path, "r") as config_file:
            config = json.loads(config_file.read())

    def validate(self):
        pass


@click.command()
@click.argument('f', type=click.Path(exists=True))
def run(f):
    config = Config(f)
    config.validate()
    click.echo(f"loaded config: {config.config}")
