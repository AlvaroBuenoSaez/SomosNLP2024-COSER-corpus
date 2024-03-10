# template-code

#Set-up

## Conda
Use conda to install python11:
```
conda create --name myenv -c conda-forge python=3.11
```
And use it:
```
conda activate py11
```

## venv and pdm
Create a virtual enviroment:
```
python3 -m venv venv
```
Install pdm:
```
pip install pdm
```
Use pdm as package manager:
```
pdm install -G test -G dev
```
If you have to install more libraries, f.e: pandas, you can do it with pdm as:
```
pdm add pandas
```
And pandas library will be automatically added to the pyproject.toml file

## cli
The app is implemented with click. There is an example implemented that can be called as:
'''
python3 module/cli.py call-example --name Álvaro
'''

## example

There is an example implemented to show how to implement each service. A service must to contains:
- config key: in config.yaml
- logger: in logger.yaml
- service: in services folder to add the functionalities
- entities: in entities folder. Objects which will be used by the service.
- controller: to manage services and entities. 
- test: a test to check the controler/service works properly. The more, the better!