import unittest

from services.service import TransactionAuthorizerService


class AccountsTest(unittest.TestCase):
    def test_create_account(self):
        handler = TransactionAuthorizerService()
        event = {
            "account": {
                "id": 2,
                "active-card": True,
                "available-limit": 5000
            }
        }

        response = handler.process(event)

        dictionary = {
            "account": {
                "id": 2,
                "active-card": True,
                "available-limit": 5000,
                "violations": []
            }
        }

        self.assertEqual(dictionary, response)

    def test_create_account_already_initialized(self):
        handler = TransactionAuthorizerService()
        event = {
            "account": {
                "id": 2,
                "active-card": True,
                "available-limit": 5000
            }
        }
        handler.process(event)

        event = {
            "account": {
                "id": 2,
                "active-card": True,
                "available-limit": 300
            }
        }

        response = handler.process(event)

        dictionary = {
            "account": {
                "id": 2,
                "active-card": True,
                "available-limit": 5000,
                "violations": ['account-already-initialized']
            }
        }

        self.assertEqual(dictionary, response)


if __name__ == '__main__':
    unittest.main()
