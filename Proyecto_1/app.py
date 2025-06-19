from dataclasses import dataclass, asdict
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
from bson.objectid import ObjectId #lo que convierte los objetos a id para mongo
from classes.BankAccount import BankAccount
from classes.DebitCard import DebitCard
from dotenv import load_dotenv
import os
load_dotenv()
   
def get_collection(uri, db="demo_db", col="bank"): #conecta al mongo en base a la collection
    client = MongoClient(
        uri
        , server_api = ServerApi("1")
        , tls = True #informacion segura
        , tlsAllowInvalidCertificates = True #permite accesos no validos
    )
    client.admin.command("ping") #verifique que la conexion funcione
        
    return client[db][col] #devuelve la coleccion personas de la base demo_db

def actualizar_documento(documento_id, id_tarjeta, coll):
    filtro = {"_id": ObjectId(documento_id)} #un filtro de busqueda para encontrar el documento que tenga el id del que se paso
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
    cuenta = BankAccount("839032", "0893 2032 16768", 500, "Propietario")
    tarjeta = DebitCard("5239 2227 1926 2552", "06/25", "06/27", "Propietario", 322)
    
    id_cuenta = cuenta.save(coll) #guarda la cuenta en mongoDB y recibe el ID
    tarjeta.bank_account_id = id_cuenta 
    
    id_tarjeta = tarjeta.save(coll)
    actualizar_documento(id_cuenta, id_tarjeta, coll)

    
        
if __name__ == "__main__":
    main()        
        

