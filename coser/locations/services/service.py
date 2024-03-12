from datasets import DatasetDict
import pandas as pd
from tqdm import tqdm

class LocationService:

    def __init__(self,config) -> None:
        self._config=config

    def parse_coser_to_location_dataset(self,dataset:DatasetDict,length=500):
        # to be implemented

        out=[]
        print(dataset)

        for dataset_name in tqdm(dataset,desc="Join all splits in datset"):
            for entry in dataset[dataset_name]:
                out.append({"id":entry["id"],"turno_id":entry["turno_id"],"text":entry["text"],"location":entry["provincia"]})
        
        df=pd.DataFrame.from_records(out)
        ids=list(set(df["id"].to_list()))

        out=[]
        for id_interview in tqdm(ids,desc="Processing ids"):
            df_interview=df[df["id"]==id_interview].sort_values("turno_id")
            buffer_text=""
            buffer_split=1
            for i,row in df_interview.iterrows():
                buffer_text+=row.text+"\n"
                if len(buffer_text)>=length:
                    out.append({"id":id_interview,"split":buffer_split,"text":self._process_text(buffer_text),"location":row.location})
                    buffer_split+=1
        
        out.append({"id":id_interview,"split":buffer_split,"text":buffer_text,"location":row.location})

        return pd.DataFrame.from_records(out)
    
    def _process_text(self,text:str)->str:
        #to implement
        return text