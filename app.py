# __init__

from flask import Flask
from flask import render_template
from flask import request

app = Flask(__name__) # flask application 생성

@app.route('/')
def index():
    return render_template('main.html')

# info page
@app.route('/info')
def info():
    return render_template('info.html')

if __name__ == '__main__':
    app.run(debug=True)

@app.route('/result', methods=['GET','POST'])
def result():
    go_date = request.args.get('goDate')
    back_date = request.args.get('backDate')
    if request.method == 'GET':
        return render_template('main_result.html', go_date=go_date, back_date=back_date)
    
    if request.method == 'POST':
        return 
    
@app.route('/dash', methods=['GET','POST'])
def dash():
    return render_template('dash.html')