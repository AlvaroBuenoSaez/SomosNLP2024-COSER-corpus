import os

from coser.locations.services.service import LocationService
from coser.common.services.CoserService import CoserService
from coser.common.services.VariatorOpenAi import VariatiorOAI
from coser.common.services.PromptVariations import PromptingService

from coser.common.utils import PROJECT_PATH,save_json
from coser.common.configuration.config import load_config,get_logger
logger=get_logger("locations")
from datetime import datetime
from tqdm import tqdm
import pandas as pd

class LocationController:


    def __init__(self):
        self._config=load_config().get("locations",{})
        self._service=LocationService(self._config)
        self._coser_service=CoserService(load_config().get("coser_service",{}))


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
    

    def generate_prompts_for_input_with_hf(self):
        logger.debug("Loading Prompting Service")
        config=load_config()
        promtp_config=config.get("prompt_input")
        service=PromptingService(promtp_config.get("model"),promtp_config.get("input"))
        input_prompts=config.get("locations").get("input_prompts")
        raw_result=service.variate_prompts(input_prompts)
    
        if raw_result:
            out_folder=promtp_config.get("out_folder")
            abs_out_folder=os.path.join(PROJECT_PATH,out_folder) if not out_folder.startswith("/") else out_folder
            os.makedirs(abs_out_folder,exist_ok=True)
            now = datetime.now()
            dt_string = now.strftime("{}_result_%d%m%Y_%H%M%S.json".format(promtp_config.get("model").replace(os.sep,"-")))
            save_json(os.path.join(abs_out_folder,dt_string),raw_result)

        return raw_result
    
    def generate_prompts_for_input_with_oai(self):
        logger.debug("Loading Prompting Service")
        config=load_config()
        promtp_config=config.get("prompt_input")
        service=VariatiorOAI(promtp_config.get("openai_key"),promtp_config.get("input"))
        input_prompts=config.get("locations").get("input_prompts")
        raw_result=service.variate_prompts(input_prompts)
    
        if raw_result:
            out_folder=promtp_config.get("out_folder")
            abs_out_folder=os.path.join(PROJECT_PATH,out_folder) if not out_folder.startswith("/") else out_folder
            os.makedirs(abs_out_folder,exist_ok=True)
            now = datetime.now()
            dt_string = now.strftime("openai_result_%d%m%Y_%H%M%S.json")
            save_json(os.path.join(abs_out_folder,dt_string),raw_result)

        return raw_result
    


    def generate_location_corpus(self,turn_ini=0,turn_fin=10):
        logger.debug("Loading data from local.")
        df=self._coser_service.get_dataset_from_local()
        df=self._coser_service.elegir_regionalismos(df,regionalismos=True)
        
        logger.debug("Processing interviews.")
        df_out=[]
        for filename in tqdm(df.iloc[:, 0].unique()):
            out=[]
            conv=self._coser_service.obtenerFragmentoEntrevista(df,filename,turn_ini,turn_fin)
            provincia=self._coser_service.obtenerProvincia(df,filename)
            out_prompts=self._service.get_out_prompts(provincia)
            in_prompts=self._service.get_in_prompts(conv)

            for out_prompt in out_prompts:
                for in_prompt in in_prompts:
                    out.append({"input":in_prompt,"output":out_prompt})
            df_out.extend(out)
            out_folder=os.path.join(PROJECT_PATH,self._service._config.get("out_folder"))
            os.makedirs(out_folder,exist_ok=True)
            pd.DataFrame.from_records(out).to_csv(os.path.join(out_folder,"{}.csv".format(filename)),index=False)
            

        return pd.DataFrame.from_records(df_out)
    

