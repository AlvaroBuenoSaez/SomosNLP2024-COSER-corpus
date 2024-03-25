import os
from langchain_community.llms import Ollama
from langchain.prompts import PromptTemplate
import coser
import pandas as pd

# first run "ollama pull <model>"

model = "gemma:7b-instruct"

output_folder = 'outputs/'+model

####################################

os.makedirs(output_folder, exist_ok=True)

df = coser.csv2Df('CLEAN_df_hack_full.csv')
df = coser.elegirRegionalismos(df, regionalismos = True)
df = coser.agregar_columna_topics(df)

####################################

llm = Ollama(model=model, temperature=1.0)
print(f"--- Modelo: {model} ---\n")

prompt = PromptTemplate(
    template="""Acabas de leer una entrevista para la cual te han pedido determinar la provincia española a la que pertenecen los informadores, basándote en los rasgos lingüísticos que muestran durante la conversación. Redacta una respuesta breve y cordial para esta pregunta, sabiendo que la respuesta correcta es {provincia}. No incluyas ningún tipo de razonamiento posterior, ni ninguna hipótesis sobre los rasgos lingüísticos utilizados.
    """,
    input_variables=["provincia"],
)

chain = prompt | llm 

####################################

file_list = list(df.filename.unique())

####################################


for i,file in enumerate(file_list[:10]):
    print(f'Processing File {file} [{i+1}/{len(file_list)}]')
    provincia = coser.obtenerProvincia(df, file)

    r = chain.invoke(
        {
        'provincia': provincia,
        }
    )

    filename = 'provincia_'+file+'.txt'

    with open(os.path.join(output_folder, filename), 'w') as f:
        f.write(r)