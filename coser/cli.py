import click
from coser.locations.controllers.controller import LocationController


@click.group(invoke_without_command=True)
@click.pass_context
def main (ctx):
    pass


# Use: python3 coser/cli.py parser-location
@main.command()
@click.option("--out_folder",default="out_locations",help="folder to save the result")
def parser_location(out_folder):
    controller=LocationController()
    controller.parse_original_coser(out_folder)


if __name__=="__main__":
    main()