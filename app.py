# __init__

from flask import Flask
from flask import render_template
from flask import request

app = Flask(__name__) # flask application 생성

@app.route('/')
def index():
    return render_template('main.html')

if __name__ == '__main__':
    app.run(debug=True)

@app.route('/result', methods=['GET','POST'])
def result():
    if request.method == 'GET':
        return render_template('main_result.html')
    
    if request.method == 'POST':
        return 