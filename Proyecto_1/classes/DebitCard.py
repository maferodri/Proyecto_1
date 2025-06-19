from dataclasses import dataclass, asdict
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi

@dataclass
class DebitCard:
    card_num : str
    emision_date : str
    expiration_date : str
    client_name : str 
    security_code : int
    bank_account_id : str = ""
    
    def save(self, coll):
       return str(coll.insert_one(asdict(self)).inserted_id)