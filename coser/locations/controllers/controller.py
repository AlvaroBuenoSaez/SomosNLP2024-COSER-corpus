from coser.common.configuration.config import load_config,get_logger
from coser.locations.services.service import LocationService
from coser.common.services.CoserService import CoserService

logger=get_logger("locations")


class LocationController:


    def __init__(self):
        self._config=load_config().get("locations",{})
        self._service=LocationService(self._config)
        self._coser_service=CoserService(self._config)


    def parse_original_coser(self):
        logger.debug("Downloading dataset from hf...")
        dataset=self._coser_service.get_dataset_from_hf()
        logger.debug("Parsing dataset...")
        result=self._service.parse_coser_to_location_dataset(dataset)
        logger.debug("End!")
        return result