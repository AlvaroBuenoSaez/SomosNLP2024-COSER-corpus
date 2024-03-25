from coser.common.services.CoserService import CoserService
from coser.common.configuration.config import load_config
from tqdm import tqdm

service=CoserService(load_config().get("coser_service"))

df=service.get_dataset_from_local()

for filename in tqdm(df.iloc[:, 0].unique()):
    provincia=service.obtenerProvincia(df,filename)

    out_prompt=service.obtener_prompts(filename)
    if out_prompt:
        print(provincia,out_prompt)