from datasets import load_dataset
import pandas as pd
import re
import os
from coser.common.utils import read_text
class CoserService:


    def __init__(self,config) -> None:
        self._config=config
        self.out_prompts=self.get_prompts()

    def get_dataset_from_hf(self):
        return load_dataset(self._config.get("dataset_hf"))
    
    def get_dataset_from_local(self):
        return self._csv_to_df(self._config.get("local_dataset"))
    
    def get_prompts(self):
        promtp_folder=self._config.get("out_prompt_folder","")
        out_prompts={}
        print(promtp_folder)
        for llm in os.listdir(promtp_folder):
            for filename in os.listdir(os.path.join(promtp_folder,llm)):
                interview_name=filename.split("_")[1].split(".")[0]
                out_prompts[interview_name]=[] if interview_name not in out_prompts else out_prompts[interview_name]
                promp=read_text(os.path.join(promtp_folder,llm,filename)).strip()
                out_prompts[interview_name].append({"prompt":promp,"llm":llm})

        return out_prompts
        
    # Función para cargar un archivo CSV en un DataFrame
    def _csv_to_df(self,archivo_csv):
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

    # Función para visualizar cada x turnos de un DataFrame
    def elegir_regionalismos(self,dataframe, regionalismos):

        textos_modificados = []  # Lista para almacenar los textos modificados
        try:
            # Iterar sobre el DataFrame y visualizar una fila cada x filas
            dataframe['text']= dataframe['text'].apply(str)

            for index, row in dataframe.iterrows():
                # Extraer los valores de las columnas "text"
                text = row['text']
                fila = row.copy()  # Copiar la fila original

                if re.search(r'[a-zA-Z´¨\'`]*=', text):                    
                    if (regionalismos): # Se queda con la estándar
                        subcadenas = re.split(r'=', text)
                        # Las subcadenas antes y después del patrón
                        subcadena_anterior = subcadenas[0]
                        subcadena_posterior = subcadenas[1]
                        palabras = subcadena_posterior.split()
                        primera_palabra = palabras[0]
                        subcadena_posterior_sin_primera_palabra = ' '.join(palabras[1:])
                        if(re.search(r'[.,?!;:¿¡\-—–\'\"“”‘’()[\]{}<>«»@#\$%&*_\\/]', primera_palabra)):
                            match = re.search(r'[.,?!;:¿¡\-—–\'\"“”‘’()[\]{}<>«»@#\$%&*_\\/]', primera_palabra)
                            simbolo_puntuacion = match.group()
                            subcadena_posterior_sin_primera_palabra = simbolo_puntuacion + " " + subcadena_posterior_sin_primera_palabra

                        cadena = subcadena_anterior + " " + subcadena_posterior_sin_primera_palabra
                        fila['text'] = cadena

                    else : # Se queda con el regionalismo                           
                        subcadenas = re.split(r'=', text)
                        # Las subcadenas antes y después del patrón
                        subcadena_anterior = subcadenas[0]
                        subcadena_posterior = subcadenas[1]
                        # print(subcadena_anterior)
                        # print(subcadena_posterior)
                        palabras = subcadena_anterior.split()
                        subcadena_anterior_sin_ultima_palabra = ' '.join(palabras[:-1])
                        # print(subcadena_anterior_sin_ultima_palabra)
                        cadena = subcadena_anterior_sin_ultima_palabra + " " + subcadena_posterior
                        fila['text'] = cadena
                        
                textos_modificados.append(fila)
                        
            # Crear un nuevo DataFrame con los textos modificados
            df_modificado = pd.DataFrame(textos_modificados)
            return df_modificado  
    
        except Exception as e:
            print("Ocurrió un error al visualizar las filas:", e)  
            return None
        
    def agregar_columna_topics(self,dataframe):
        # Inicializar la nueva columna
        dataframe['topics'] = None
        current_topic = None

        # Recorrer el DataFrame
        current_file = dataframe.at[0, 'filename']
        for index, row in dataframe.iterrows():
            if row['filename'] != current_file:
                current_topic = None # Al llegar a un nuevo fichero, reiniciamos topic
            
            # Buscar la etiqueta en el texto
            match = re.search(r'\bT[1-9][0-9]?\b', row['text'])
            if match:
                current_topic = match.group()
            if current_topic is not None:
                dataframe.at[index, 'text'] = row['text'].replace(current_topic, '')
                dataframe.at[index, 'topics'] = current_topic
            else:
                dataframe.at[index, 'topics'] = 0  # Asignar 0 si no se encuentra una etiqueta válida
    
            current_file = dataframe.at[index, 'filename']

        return dataframe        
    


    def obtenerFragmentoEntrevista(self,dataframe, filename, turn_ini, turn_fin):
        df_entrevista = dataframe.loc[dataframe.filename == filename].reset_index()
        texto = ''

        for row in df_entrevista.loc[turn_ini:turn_fin, ['speaker_id', 'text']].iterrows():
            texto += f'{row[1].speaker_id} {row[1].text}'
            texto += '\n'

        return texto

    def obtenerProvincia(self,dataframe, filename):
        return dataframe.loc[dataframe.filename == filename].iloc[0].provincia
    
    def obtener_prompts(self,filename):
        return self.out_prompts.get(filename,{})