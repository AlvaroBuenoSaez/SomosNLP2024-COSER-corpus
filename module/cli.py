import click
from module.example.controllers.controller import ExampleController


@click.group(invoke_without_command=True)
@click.pass_context
def main (ctx):
    pass


# Use: python3 module/cli.py call-example --name Álvaro
@main.command()
@click.option("--name",default="default",help="name string")
def call_example(name):
    controller=ExampleController()
    controller.hello_world(name)


if __name__=="__main__":
    main()