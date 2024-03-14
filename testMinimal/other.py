import json

from flask import Flask, jsonify, request
from flask_restful import Api, Resource, reqparse

app = Flask(__name__)
api = Api(app)

# parser = reqparse.RequestParser()
# parser.add_argument('list', type=list)

@app.route('/coucou',methods = ['POST', 'GET'])
def get():
    arg = request.args.to_dict()
    re = json.loads(arg["arg2"])

    return (re["name"])
    #ABC = parser.parse_args()

   # return jsonify("whatever")

if __name__ == "__main__":
    app.run(debug=True)