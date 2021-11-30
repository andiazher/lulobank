from exceptions.on_exceptions import ApiException, ClientException
from infrastructure.db_service.db_service import DBService


class LocalStorage(DBService):

    def __init__(self):
        self.accounts = {}
        self.transactions = {}

    def create_account(self, account):
        if account['id'] in self.accounts and self.accounts[account['id']]:
            raise ClientException("ALREADY-INITIALIZED", 400, '')
        self.accounts[account['id']] = account
        return self.get_account(account_id=account['id'])

    def get_account(self, account_id):
        if account_id in self.accounts and self.accounts[account_id]:
            return self.accounts[account_id]
        else:
            raise ClientException("NOT_FOUND", 404, 'LBGR003')

    def create_transaction(self, transaction):
        key = str(transaction['time']) + transaction['merchant'] + str(transaction['amount'])
        self.transactions[key] = transaction

    def get_transactions(self):
        return self.transactions
