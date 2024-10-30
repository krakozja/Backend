import unittest
from os import environ
from app import app, database

class Test(unittest.TestCase):

    def test_db_add_element(self):
        database.append({"name": "luka", "animal": "dog"})
        self.assertEqual({"name": "luka", "animal": "dog"}, database.__getitem__(0))

    def test_add_animal(self):
        payload = {
            "name":  "luka",
            "animal": "dog"}
        response = app.test_client().post('/', data=payload)
        print (response.text)
        assert "[BACKEND] Name: luka Animal: dog added to the database" == response.text
        assert response.status_code == 200

if __name__ == '__main__':
    unittest.main()
