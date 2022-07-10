import os
from configparser import ConfigParser

c = os.getcwd()

file = f"{c}\DataBase\Config.ini"
config = ConfigParser()
config.read(file)

print(config["Caixa"]["ID"])
