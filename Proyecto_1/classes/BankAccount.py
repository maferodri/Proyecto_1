from dataclasses import dataclass, asdict 
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi

@dataclass
class BankAccount:
    account_num : str
    id_person : str
    balance : float
    client_name : str
    debit_card_id : str = "" 
    
    def save(self, coll): 
       return str(coll.insert_one(asdict(self)).inserted_id) 