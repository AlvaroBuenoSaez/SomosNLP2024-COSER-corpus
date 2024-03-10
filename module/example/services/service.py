
from module.example.entities.person import Person
class ExampleService:

    def __init__(self,config) -> None:
        self._config=config

    def hello_word_from(self,person:Person):
        return "{} from {}".format(self._config.get("msg"),person.name)