import unittest
from classes.BankAccount import BankAccount
from classes.DebitCard import DebitCard
from app import get_collection, actualizar_documento
from bson.objectid import ObjectId
from dotenv import load_dotenv
import os
load_dotenv()

URI = os.getenv("URI")
COLL = get_collection(URI, db="demo_db", col="bank_test")  
class TestRelacionUnoAUno(unittest.TestCase):
    
    def setUp(self):
        ""

    def test_tarjeta_tiene_id_cuenta(self):
        cuenta = BankAccount("12345", "010203", 500.0, "Test User")
        id_cuenta = cuenta.save(COLL)

        tarjeta = DebitCard("1111 2222 3333 4444", "01/24", "01/27", "Test User", 123)
        tarjeta.bank_account_id = id_cuenta
        id_tarjeta = tarjeta.save(COLL)

        # Convertimos id en ObjectId para búsqueda
        tarjeta_guardada = COLL.find_one({"_id": ObjectId(id_tarjeta)})
        self.assertEqual(tarjeta_guardada["bank_account_id"], id_cuenta)

    def test_cuenta_actualizada_con_id_tarjeta(self):
        cuenta = BankAccount("67890", "040506", 1000.0, "Test User 2")
        id_cuenta = cuenta.save(COLL)

        tarjeta = DebitCard("9999 8888 7777 6666", "02/24", "02/28", "Test User 2", 456)
        tarjeta.bank_account_id = id_cuenta
        id_tarjeta = tarjeta.save(COLL)

        # Actualizar cuenta con ID de tarjeta
        actualizar_documento(id_cuenta, id_tarjeta, COLL)

        cuenta_actualizada = COLL.find_one({"_id": ObjectId(id_cuenta)})
        self.assertEqual(str(cuenta_actualizada["debit_card_id"]), id_tarjeta)
        
    def tearDown(self):
        ""

if __name__ == '__main__':
    unittest.main()
