from flask import Flask, request, Response
import pymongo
import json
from flask_ngrok import run_with_ngrok
import datetime

with open('config.json') as file:
    params = json.load(file)['params']

mng_client = pymongo.MongoClient(params['con_url_Str'])
mng_db = mng_client[params['db']]

app = Flask(__name__)
run_with_ngrok(app)

@app.route('/webhook', methods = ['POST', 'GET'])
def webhook():
    req = request.get_json(force = True)
    session = req["session"]
    query = req["queryResult"]["queryText"]
    result = req["queryResult"]["fulfillmentText"]

    ########## Insertion in Database ################

    data = {"timestamp": datetime.datetime.now(), 
        "Query": query,
            "Result": result}
    my_col = mng_db['chatbot_req']
    my_col.insert_one(data)

    return Response(status = 200)


if __name__ == '__main__':
    app.run()