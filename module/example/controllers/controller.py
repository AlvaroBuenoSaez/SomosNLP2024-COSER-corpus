from module.example.services.service import ExampleService
from module.example.entities.person import Person
from module.common.configuration.config import load_config,get_logger
logger=get_logger("example")


class ExampleController:


    def __init__(self):
        self._config=load_config().get("example",{})
        self._service=ExampleService(self._config)


    def hello_world(self,name_to:str):
        logger.info("{} recived".format(name_to))
        person=Person(name_to)
        result=self._service.hello_word_from(person)
        logger.info("Result",result)
        return result