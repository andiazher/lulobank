import unittest

from services.service import TransactionAuthorizerService


class TransactionTests(unittest.TestCase):
    def test_create_transaction(self):
        handler = TransactionAuthorizerService()
        account_id = 1
        self.__crater_account(handler, account_id)

        event = {
            "transaction": {
                "id": account_id,
                "merchant": "Burger King",
                "amount": 2000,
                "time": "2021-02-13T11:00:00.00Z"
            }
        }

        response = handler.process(event)

        dictionary = {
            "account": {
                "id": 1,
                "active-card": True,
                "available-limit": 3000,
                "violations": []
            }
        }
        self.assertEqual(dictionary, response)

    def test_create_transaction_insufficient_limit(self):
        handler = TransactionAuthorizerService()
        account_id = 1
        self.__crater_account(handler, account_id)

        event = {
            "transaction": {
                "id": account_id,
                "merchant": "Burger King",
                "amount": 5000,
                "time": "2021-11-13T09:00:00.00Z"
            }
        }

        response = handler.process(event)

        dictionary = {
            "account": {
                "id": 1,
                "active-card": True,
                "available-limit": 5000,
                "violations": ['insufficient-limit']
            }
        }
        self.assertEqual(dictionary, response)

    def test_create_transaction_account_not_initialized(self):
        handler = TransactionAuthorizerService()
        account_id = 4

        event = {
            "transaction": {
                "id": account_id,
                "merchant": "Burger King",
                "amount": 200,
                "time": "2021-11-13T17:00:00.00Z"
            }
        }

        response = handler.process(event)

        dictionary = {
            "account": {
                "violations": ['account-not-initialized']
            }
        }
        self.assertEqual(dictionary, response)

    def test_create_transaction_card_not_active(self):
        handler = TransactionAuthorizerService()
        account_id = 10
        event = {
            "account": {
                "id": account_id,
                "active-card": False,
                "available-limit": 5000
            }
        }
        handler.process(event)

        event = {
            "transaction": {
                "id": account_id,
                "merchant": "Burger King",
                "amount": 2000,
                "time": "2021-11-13T12:00:00.00Z"
            }
        }

        response = handler.process(event)

        dictionary = {
            "account": {
                "id": 10,
                "active-card": False,
                "available-limit": 5000,
                "violations": ['card-not-active']
            }
        }
        self.assertEqual(dictionary, response)

    def test_create_transaction_small_interval(self):
        handler = TransactionAuthorizerService()
        account_id = 1
        self.__crater_account(handler, account_id)

        event = {
            "transaction": {
                "id": account_id,
                "merchant": "Burger King",
                "amount": 100,
                "time": "2021-02-16T10:00:00.00Z"
            }
        }
        handler.process(event)

        event = {
            "transaction": {
                "id": account_id,
                "merchant": "Burger King",
                "amount": 200,
                "time": "2021-02-16T10:01:00.00Z"
            }
        }
        handler.process(event)

        event = {
            "transaction": {
                "id": account_id,
                "merchant": "Burger King",
                "amount": 300,
                "time": "2021-02-16T10:01:10.00Z"
            }
        }

        handler.process(event)

        event = {
            "transaction": {
                "id": account_id,
                "merchant": "Burger King",
                "amount": 400,
                "time": "2021-02-16T10:01:40.00Z"
            }
        }

        response = handler.process(event)

        dictionary = {
            "account": {
                "violations": ['high-frequency-small-interval']
            }
        }
        self.assertEqual(dictionary, response)

    def test_create_transaction_doubled_transaction(self):
        handler = TransactionAuthorizerService()
        account_id = 1
        self.__crater_account(handler, account_id)

        event = {
            "transaction": {
                "id": account_id,
                "merchant": "Burger King",
                "amount": 100,
                "time": "2021-12-12T10:00:00.00Z"
            }
        }
        handler.process(event)

        event = {
            "transaction": {
                "id": account_id,
                "merchant": "Burger King",
                "amount": 100,
                "time": "2021-12-12T10:01:00.00Z"
            }
        }
        handler.process(event)

        event = {
            "transaction": {
                "id": account_id,
                "merchant": "Burger King",
                "amount": 100,
                "time": "2021-12-12T10:01:10.00Z"
            }
        }

        response = handler.process(event)

        dictionary = {
            "account": {
                "violations": ['doubled-transaction']
            }
        }
        self.assertEqual(dictionary, response)

    @staticmethod
    def __crater_account(handler, account_id):
        event = {
            "account": {
                "id": account_id,
                "active-card": True,
                "available-limit": 5000
            }
        }
        handler.process(event)


if __name__ == '__main__':
    unittest.main()
