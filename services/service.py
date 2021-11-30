class TransactionAuthorizerService:

    def process(self, event):
        try:
            if "account" in event and event['account']:
                self.create_account(event['account'])
            if "transaction" in event and event["transaction"]:
                self.process_transaction(event['account'])
        except BaseException as e:
            print(e)

    def create_account(self, param):
        pass

    def process_transaction(self, param):
        pass