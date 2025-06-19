from dataclasses import dataclass, asdict
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
from bson.objectid import ObjectId 
from classes.BankAccount import BankAccount
from classes.DebitCard import DebitCard
from dotenv import load_dotenv
import os
load_dotenv()
   
def get_collection(uri, db="demo_db", col="bank"):
    client = MongoClient(
        uri
        , server_api = ServerApi("1")
        , tls = True #informacion segura
        , tlsAllowInvalidCertificates = True 
    )
    client.admin.command("ping") 
        
    return client[db][col] #d

def actualizar_documento(documento_id, id_tarjeta, coll):
    filtro = {"_id": ObjectId(documento_id)} 
    nuevos_valores = {"$set": {"debit_card_id": ObjectId(id_tarjeta)}}
    resultado = coll.update_one(filtro, nuevos_valores)
    if resultado.matched_count > 0:
        print("Documento encontrado y actualizado correctamente.")
    else:
        print("No se encontró ningún documento con ese ID.")
    return resultado

    
def main():
        
    uri = os.getenv("URI")
    coll = get_collection(uri)
    cuenta = BankAccount("7839202", "0893 2032 16768", 500, "María Fernanda Rodríguez")
    tarjeta = DebitCard("5239 2227 1926 2552", "06/25", "06/27", "María Fernanda Rodríguez", 322)
    
    id_cuenta = cuenta.save(coll) 
    tarjeta.bank_account_id = id_cuenta 
    
    id_tarjeta = tarjeta.save(coll)
    actualizar_documento(id_cuenta, id_tarjeta, coll)

    
        
if __name__ == "__main__":
    main()        
        

