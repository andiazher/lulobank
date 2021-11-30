from datetime import datetime

from exceptions.on_exceptions import ClientException
from infrastructure.db_service.local_storage import LocalStorage

local_storage = LocalStorage()


class TransactionAuthorizerService:

    def __init__(self):
        self.db = local_storage

    def process(self, event):
        try:
            if "account" in event and event['account']:
                return self.create_account(event['account'])
            if "transaction" in event and event["transaction"]:
                return self.process_transaction(event['transaction'])
        except BaseException as e:
            print(e)

    def create_account(self, account):
        try:
            account = self.db.create_account(account)
            if account:
                account['violations'] = []
                return {"account": account}
        except ClientException:
            account = self.db.get_account(account['id'])
            if account:
                account['violations'] = ['account-already-initialized']
                return {"account": account}

    def process_transaction(self, transaction):
        try:
            account_id = transaction['id']
            if self.__validate_limit_transaction(transaction):
                return {"account": {"violations": ['high-frequency-small-interval']}}
            if self.__validate_double_transaction(transaction):
                return {"account": {"violations": ['doubled-transaction']}}
            self.__create_transaction(transaction)
            account = self.db.get_account(account_id)

            if account:

                if not account['active-card']:
                    account['violations'] = ['card-not-active']
                    return {"account": account}
                if account['available-limit'] >= transaction['amount']:
                    account['available-limit'] = account["available-limit"] - transaction['amount']
                    account['violations'] = []
                else:
                    account['violations'] = ['insufficient-limit']
                return {"account": account}
            return {"account": {"violations": ['account-not-initialized']}}
        except ClientException:
            return {"account": {"violations": ['account-not-initialized']}}

    def __create_transaction(self, transaction):
        timestamp = self.__get_timestamp(transaction)
        transaction['time'] = int(timestamp)
        self.db.create_transaction(transaction)

    def __validate_limit_transaction(self, transaction):
        timestamp = self.__get_timestamp(transaction)
        transactions = self.db.get_transactions()
        counter = 0
        for key in transactions:
            if transactions[key]['time'] > timestamp - 120:
                counter = counter + 1
        if counter >= 3:
            return True
        return False

    def __validate_double_transaction(self, transaction):
        timestamp = self.__get_timestamp(transaction)
        transactions = self.db.get_transactions()
        for key in transactions:
            if transactions[key]['time'] > timestamp - 120 and transactions[key]['amount'] == transaction['amount'] and \
                    transactions[key]['merchant'] == transaction['merchant']:
                return True

    @staticmethod
    def __get_timestamp(transaction):
        date_time = datetime.strptime(transaction['time'], '%Y-%m-%dT%H:%M:%S.%fZ')
        return datetime.timestamp(date_time)
