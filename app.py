# __init__

from flask import Flask
from flask import render_template
from flask import request
from flask import redirect

app = Flask(__name__) # flask application 생성

# main page
@app.route('/')
def main():
    return render_template('main.html')

# info page
@app.route('/info')
def info():
    return render_template('info.html')

if __name__ == '__main__':
    app.run(debug=True)

# result page
@app.route('/result', methods=['GET','POST'])
def result():
    go_date = request.args.get('goDate')
    back_date = request.args.get('backDate')
    if request.method == 'GET':
        return render_template('main_result.html', go_date=go_date, back_date=back_date)
    
    # 각각의 select값을 받아왔을때
    if request.method == 'POST':
        low_option = request.form.get('lowprice_option')
        mid_option = request.form.get('midprice_option')
        high_option = request.form.get('highprice_option')
        
        if low_option =='항공' or mid_option=='항공' or high_option=='항공':
            return redirect('/flight')
        elif low_option =='숙박' or mid_option=='숙박' or high_option=='숙박':
            return redirect('/hotel')
        elif low_option =='렌트' or mid_option=='렌트' or high_option=='렌트':
            return redirect('/rentcar')
        else:       # 아무것도 선택하지 않았을 경우
            return render_template('main_result.html')

# dashboard page    
@app.route('/dash', methods=['GET','POST'])
def dash():
    return render_template('dash.html')

# 항공편 추천
@app.route('/flight')
def flight():
    return render_template('flight.html')

# 호텔 추천
@app.route('/hotel')
def hotel():
    return render_template('hotel.html')

# 렌트카 추천
@app.route('/rentcar')
def rentcar():
    return render_template('rentcar.html')
