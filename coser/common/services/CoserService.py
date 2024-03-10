from datasets import load_dataset


class CoserService:


    def __init__(self,config) -> None:
        self._config=config

    def get_dataset_from_hf(self):
        return load_dataset(self._config.get("dataset_hf"))