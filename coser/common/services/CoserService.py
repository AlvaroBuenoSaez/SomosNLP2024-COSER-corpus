from datasets import load_dataset
import pandas as pd

class CoserService:


    def __init__(self,config) -> None:
        self._config=config

    def get_dataset_from_hf(self):
        return load_dataset(self._config.get("dataset_hf"))
    
    def get_dataset_from_local(self):
        return self._csv2Df(self._config.get("local_dataset"))
    
    # Función para cargar un archivo CSV en un DataFrame
    def _csv2Df(self,archivo_csv):
        try:
            # Cargar el archivo CSV en un DataFrame
            df = pd.read_csv(archivo_csv, sep=',', encoding='utf-8', on_bad_lines='warn')
            return df
        except FileNotFoundError:
            print("El archivo CSV no fue encontrado.")
            return None
        except Exception as e:
            print("Ocurrió un error al cargar el archivo CSV:", e)
            return None