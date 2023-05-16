# __init__

from flask import Flask

app = Flask(__name__) # flask application 생성

@app.route('/')
def index():
    return 'Hello world'*2