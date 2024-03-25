from coser.common.services.CoserService import CoserService
from coser.common.configuration.config import load_config

from coser.common.services.CoserService import CoserService
from coser.common.configuration.config import load_config
from tqdm import tqdm

def test_parse_out():
    service=CoserService(load_config().get("coser_service"))

    df=service.get_dataset_from_local()
    prompts=[]
    for filename in tqdm(df.iloc[:, 0].unique()):
        provincia=service.obtenerProvincia(df,filename)
        
        interview_name=filename.split(".")[0]
        out_prompt=service.obtener_prompts(interview_name)
        
        if out_prompt:
            for entry in out_prompt:
                text=entry["prompt"]
                if provincia in text:
                    prompt=text.replace(provincia,"{}")
                    prompts.append(prompt) if prompt not in prompts else None
                else:   
                    print(provincia,out_prompt)

    print("PROMPTS")
    for p in prompts:
        print("- \"{}\"".format(p))

def test_read_data_csv():
    config=load_config()
    service=CoserService(config.get("coser-service"))
    df=service.get_dataset_from_local()
    print(df.head())
    print(df.columns)
    assert not df.empty


def test_read_dataset():
    config=load_config()
    service=CoserService(config.get("coser-service"))
    dataset=service.get_dataset_from_hf()
    print(dataset)
    assert dataset