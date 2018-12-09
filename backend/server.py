from flask import Flask, request
from flask_cors import CORS
from celery import Celery

app = Flask(__name__)
CORS(app)

@app.route('/', methods=['GET'])
def fetch_midi():
    with open('current.midi', 'rb') as f:
        return f.read()