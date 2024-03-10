import click
from coser.locations.controllers.controller import LocationController


@click.group(invoke_without_command=True)
@click.pass_context
def main (ctx):
    pass


# Use: python3 coser/cli.py parser-location
@main.command()
# @click.option("--name",default="default",help="name string")
def parser_location():
    controller=LocationController()
    controller.parse_original_coser()


if __name__=="__main__":
    main()