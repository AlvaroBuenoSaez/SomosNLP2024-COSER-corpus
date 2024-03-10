import os

from coser.locations.services.service import LocationService
from coser.common.services.CoserService import CoserService

from coser.common.utils import PROJECT_PATH
from coser.common.configuration.config import load_config,get_logger
logger=get_logger("locations")


class LocationController:


    def __init__(self):
        self._config=load_config().get("locations",{})
        self._service=LocationService(self._config)
        self._coser_service=CoserService(self._config)


    def parse_original_coser(self,out_folder,length=200):
        logger.debug("Downloading dataset from hf...")
        dataset=self._coser_service.get_dataset_from_hf()
        logger.debug("Parsing dataset...")
        result=self._service.parse_coser_to_location_dataset(dataset)
        logger.debug("Result len {}".format(len(result)))
        logger.debug("Saving new dataset in {}".format(out_folder))
        os.makedirs(os.path.join(PROJECT_PATH,out_folder))
        result.to_csv(os.path.join(PROJECT_PATH,out_folder,"coser_dataset_len_{}.csv".format(length)),index=False)
        logger.debug("End!")
        return result