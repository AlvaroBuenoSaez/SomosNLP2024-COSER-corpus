import json,os,yaml
import pandas as pd



CURRENT_PATH = os.path.dirname(os.path.abspath(__file__))
MODULE_PATH = os.sep.join(CURRENT_PATH.split(os.sep)[0:-1])
PROJECT_PATH = os.sep.join(CURRENT_PATH.split(os.sep)[0:-2])


def config_file(filename="config.yml"):
    
    config_vars = read_yaml(
        os.path.join(CURRENT_PATH, filename)
    )
    return config_vars

def read_yaml(_path):

    with open(_path, "r") as f_stream:
        config = yaml.load(f_stream, Loader=yaml.FullLoader)

    return config

def read_text(file_path:str):
    with open(file_path,"r") as input_text:
        return input_text.read()

def read_json(file_path:str):
    with open(file_path,"r",encoding="utf8") as json_in:
        return json.load(json_in)

def read_jsonl(file_path:str):
    
    with open(file_path,"r",encoding="utf8") as json_in:
        out=[]
        
        for line in json_in:
            try:
                entry=json.loads(line)
                out.append(entry)
            except:
                continue
        
        return  out

def save_json(file_path:str,data:dict):
    with open(file_path,"w+", encoding="utf8") as json_out:
        json.dump(data, json_out,ensure_ascii=False)   

def save_jsonl(file_path:str,data:list): 
    with open(file_path,"w+", encoding="utf8") as json_out:
        for entry in data:
            json.dump(entry, json_out,ensure_ascii=False)
            json_out.write('\n')
            

FILETYPES={
    "JSON":(".json"),
    "JSONL":(".jsonl",".ndjson"),
    "CSV":(".csv"),
    "EXCEL":(".xls",".xlsx")
}
            
def read_folder(path,*args, **kwargs):
    path=path if not path.startswith(os.sep) else os.path.join(CURRENT_PATH,path)
    for file in os.listdir(path):
        if not file.startswith("."):
            file_path=os.path.join(os.path.join(CURRENT_PATH,path,file))
            if file.endswith(FILETYPES["EXCEL"]):
                yield (file,pd.read_excel(file_path,engine='openpyxl'))
            elif file.endswith(FILETYPES["CSV"]):
                yield (file,pd.read_csv(file_path,**kwargs))
            elif file.endswith(FILETYPES["JSONL"]):
                yield (file,read_jsonl(os.path.join(CURRENT_PATH,path,file)))
            elif file.endswith(FILETYPES["JSON"]):
                yield (file,read_json(os.path.join(CURRENT_PATH,path,file)))
                
import time
def measure(function, *args):
    init = time.time()
    result = function(*args)
    return result, time.time() - init


def read_jsonl_as_df(path):
    return pd.read_json(path,lines=True)