import os
import sys
from argparse import ArgumentParser

from flask import Flask, request, abort, jsonify
from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage,
)
from pyngrok import ngrok
from pymongo import MongoClient
from datetime import datetime

# database code
#mongoClient = MongoClient(os.environ["MONGODB_URI"], 27017)
#mongoClient = MongoClient("localhost", 27017)
mongoClient = MongoClient("mongodb://127.0.0.1:27017/?compressors=disabled&gssapiServiceName=mongodb")
#if os.environ["PHASE"] == "DEVELOPMENT":
#    app_db = mongoClient.blecollector_test # Database
#if os.environ["PHASE"] == "PRODUCTION":
#    app_db = mongoClient.blecollector # Database
app_db = mongoClient.blecollector_test # Database

app = Flask(__name__, static_url_path='/ui', static_folder='web/')


@app.route("/", methods=['GET'])
def hello_world():
    return "Hello, World!"

@app.route("/api/inject_logging", methods=['POST'])
def inject_logging():
    #if os.environ["PHASE"] == "DEVELOPMENT":
    data = request.get_json()
    data['timestamp'] = datetime.now()
    logging_col = app_db.logging # Collection
    logging_col.insert_one(data)
    print(data)
    return jsonify({"status": "OK"})
    #return jsonify({"status": "ERROR"})


if __name__ == "__main__":
    arg_parser = ArgumentParser(
        usage='Usage: python ' + __file__ + ' [--port <port>] [--help]'
    )
    arg_parser.add_argument('-p', '--port', default=8000, help='port')
    arg_parser.add_argument('-d', '--debug', default=False, help='debug')
    options = arg_parser.parse_args()

    app.run(debug=options.debug, port=options.port)
