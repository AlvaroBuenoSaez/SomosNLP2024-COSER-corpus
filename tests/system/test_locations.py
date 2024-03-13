


# from coser.co.controllers.controller import ExampleController
# def test_hello_world():
#     controller=ExampleController()
#     result=controller.hello_world("Álvaro")
#     assert result

from coser.locations.controllers.controller import LocationController


def test_locations():
    con=LocationController()
    result=con.parse_original_coser("./test/assets/out_folder_locations/")