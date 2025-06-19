from dataclasses import dataclass, asdict #dataclass simplifica la creacion de clases con atributos, asdict convierte una instancia de dataclass en un diccionario
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi

@dataclass
class BankAccount:
    account_num : str
    id_person : str
    balance : float
    client_name : str
    debit_card_id : str = "" #string vacio por defecto para luego relacionar con la tarjeta
    
    def save(self, coll): #save es el metodo para guardar la instancia en mongodb
       return str(coll.insert_one(asdict(self)).inserted_id) #retorna el id insertado como cadena y lo convierte a string 