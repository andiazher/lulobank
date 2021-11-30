import json
import sys

from flask import Flask, request, make_response
from flask_restful import Resource, Api

from exceptions.on_exceptions import ApiException, LambdaException
from services.service import TransactionAuthorizerService

application = Flask(__name__)
api = Api(application)


class TransactionAuthorizerHandler(Resource):
    handler = TransactionAuthorizerService()

    @api.representation('application/json')
    def post(self):
        try:
            json_data = request.get_json(force=True)
            data_response = self.handler.process(json_data)
            return self.output_json(data_response, 200)
        except ApiException as ex:
            return self.output_json_error(ex)
        except BaseException as ex:
            exception = LambdaException('SERVICE_UNAVAILABLE', 503, 'LBGR001')
            return self.output_json_error(exception)

    @staticmethod
    def output_json(data, code):
        resp = make_response(data, code)
        resp.headers['content-type'] = 'application/json'
        return resp

    def output_json_error(self, exception):
        data = json.dumps(exception.message)
        return self.output_json(data, exception.status)


api.add_resource(TransactionAuthorizerHandler, "/")

if __name__ == '__main__':
    if len(sys.argv) > 1 and str(sys.argv[1]) == "debug":
        print("Running in Debug")
        application.run(host='0.0.0.0', debug=True)
    else:
        from waitress import serve
        serve(application, host='0.0.0.0', port='8081', threads='10')
