


from module.example.controllers.controller import ExampleController
def test_hello_world():
    controller=ExampleController()
    result=controller.hello_world("Álvaro")
    assert result