# __init__

from flask import Flask
from flask import render_template
from flask import request
from flask import redirect
import psycopg2

app = Flask(__name__) # flask application 생성

def connect_to_database():
    conn = psycopg2.connect(
        host="drona.db.elephantsql.com",
        port="5432",
        database="bnwptvqk",
        user="bnwptvqk",
        password="RWLldWbYTfneg_E7-NYZ0YeUH75vKq1d"
    )
    return conn

# main page
@app.route('/')
def main():
    return render_template('main.html')

# info page
@app.route('/info')
def info():
    return render_template('info.html')



# result page
@app.route('/result', methods=['GET','POST'])
def result():

    input_value_1 = request.args.get('goDate')
    input_value_2 = request.args.get('backDate')



    conn = connect_to_database()
    cur = conn.cursor()

    # flight_gimpo_jeju 테이블에서 날짜가 goDate인 행들의 최저가 가져오기
    cur.execute("""
        SELECT MIN(price)
        FROM flight_gimpo_jeju
        WHERE date = %s
    """, (input_value_1,))
    min_price_1 = cur.fetchone()[0]

    # flight_jeju_gimpo 테이블에서 날짜가 backDate인 행들의 최저가 가져오기
    cur.execute("""
        SELECT MIN(price)
        FROM flight_jeju_gimpo
        WHERE date = %s
    """, (input_value_2,))
    min_price_2 = cur.fetchone()[0]

    # flight_gimpo_jeju 테이블에서 날짜가 goDate인 행들의 평균가 가져오기
    cur.execute("""
        SELECT AVG(price)
        FROM flight_gimpo_jeju
        WHERE date = %s
    """, (input_value_1,))
    avg_price_1 = cur.fetchone()[0]

    # flight_jeju_gimpo 테이블에서 날짜가 backDate인 행들의 평균가 가져오기
    cur.execute("""
        SELECT AVG(price)
        FROM flight_jeju_gimpo
        WHERE date = %s
    """, (input_value_2,))
    avg_price_2 = cur.fetchone()[0]

    # flight_gimpo_jeju 테이블에서 날짜가 goDate인 행들의 최고가 가져오기
    cur.execute("""
        SELECT MAX(price)
        FROM flight_gimpo_jeju
        WHERE date = %s
    """, (input_value_1,))
    max_price_1 = cur.fetchone()[0]

    # flight_jeju_gimpo 테이블에서 날짜가 backDate인 행들의 최고가 가져오기
    cur.execute("""
        SELECT MAX(price)
        FROM flight_jeju_gimpo
        WHERE date = %s
    """, (input_value_2,))
    max_price_2 = cur.fetchone()[0]

    # 최저가 더한 값
    total_min_price = min_price_1 + min_price_2

    # 평균가 더한 값
    total_avg_price = avg_price_1 + avg_price_2

    # 최고가 더한 값
    total_max_price = max_price_1 + max_price_2

    # 연산 결과를 result.html로 전달
    return render_template('main_result.html', total_min_price=total_min_price,
                           total_avg_price=total_avg_price, total_max_price=total_max_price)
    
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

if __name__ == '__main__':
    app.run(debug=True)
