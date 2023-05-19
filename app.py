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

    input_value_1 = int(request.args.get('goDate'))
    input_value_2 = int(request.args.get('backDate'))
    # input_value_3 = request.args.get('peopleValue')

    if request.method == 'GET':

        conn = connect_to_database()
        cur = conn.cursor()

        # flight_gimpo_jeju 테이블에서 날짜가 goDate인 행들의 최저가 가져오기
        cur.execute("""
            SELECT MIN(price)
            FROM flight_gimpo_jeju
            WHERE date = %s
        """, (input_value_1,))
        f_min_price_1 = cur.fetchone()[0]

        # flight_jeju_gimpo 테이블에서 날짜가 backDate인 행들의 최저가 가져오기
        cur.execute("""
            SELECT MIN(price)
            FROM flight_jeju_gimpo
            WHERE date = %s
        """, (input_value_2,))
        f_min_price_2 = cur.fetchone()[0]

        # flight_gimpo_jeju 테이블에서 날짜가 goDate인 행들의 평균가 가져오기
        cur.execute("""
            SELECT AVG(price)
            FROM flight_gimpo_jeju
            WHERE date = %s
        """, (input_value_1,))
        f_avg_price_1 = cur.fetchone()[0]

        # flight_jeju_gimpo 테이블에서 날짜가 backDate인 행들의 평균가 가져오기
        cur.execute("""
            SELECT AVG(price)
            FROM flight_jeju_gimpo
            WHERE date = %s
        """, (input_value_2,))
        f_avg_price_2 = cur.fetchone()[0]

        # flight_gimpo_jeju 테이블에서 날짜가 goDate인 행들의 최고가 가져오기
        cur.execute("""
            SELECT MAX(price)
            FROM flight_gimpo_jeju
            WHERE date = %s
        """, (input_value_1,))
        f_max_price_1 = cur.fetchone()[0]

        # flight_jeju_gimpo 테이블에서 날짜가 backDate인 행들의 최고가 가져오기
        cur.execute("""
            SELECT MAX(price)
            FROM flight_jeju_gimpo
            WHERE date = %s
        """, (input_value_2,))
        f_max_price_2 = cur.fetchone()[0]

        # 최저가 더한 값
        f_total_min_price = f_min_price_1 + f_min_price_2

        # 평균가 더한 값
        f_total_avg_price = f_avg_price_1 + f_avg_price_2

        # 최고가 더한 값
        f_total_max_price = f_max_price_1 + f_max_price_2
        
        #호텔 최저가
        cur.execute("""
            SELECT MIN(price)
            FROM hotel_total
            WHERE checkout_date - checkin_date = %s - %s
        """, (input_value_2, input_value_1))
        h_min_price = cur.fetchone()[0]
        
        #호텔 평균가
        cur.execute("""
            SELECT AVG(price)
            FROM hotel_total
            WHERE checkout_date - checkin_date = %s - %s
        """, (input_value_2, input_value_1))
        h_avg_price = cur.fetchone()[0]
        
        #호텔 최고가
        cur.execute("""
            SELECT MAX(price)
            FROM hotel_total
            WHERE checkout_date - checkin_date = %s - %s
        """, (input_value_2, input_value_1))
        h_max_price = cur.fetchone()[0]
        
        #렌터카 최저가
        cur.execute("""
            SELECT MIN(price)
            FROM car_total
            WHERE return_date - rent_date = %s - %s
        """, (input_value_2, input_value_1))
        c_min_price = cur.fetchone()[0]
        
        #렌터카 평균가
        cur.execute("""
            SELECT AVG(price)
            FROM car_total
            WHERE return_date - rent_date = %s - %s
        """, (input_value_2, input_value_1))
        c_avg_price = cur.fetchone()[0]
        
        #렌터카 최고가
        cur.execute("""
            SELECT MAX(price)
            FROM car_total
            WHERE return_date - rent_date = %s - %s
            """, (input_value_2, input_value_1))
        c_max_price = cur.fetchone()[0]
        
        #항공,호텔,렌터카의 최저가,평균가,최고가 합산
        min_price= f_total_min_price+h_min_price+c_min_price
        avg_price= f_total_avg_price+h_avg_price+c_avg_price
        max_price= f_total_max_price+h_max_price+c_max_price
        
        f_total_min_price = format(int(f_total_min_price), ',')
        f_total_avg_price = format(int(f_total_avg_price), ',')
        f_total_max_price = format(int(f_total_max_price), ',')
        h_min_price = format(int(h_min_price), ',')
        h_avg_price = format(int(h_avg_price), ',')
        h_max_price = format(int(h_max_price), ',')
        c_min_price = format(int(c_min_price), ',')
        c_avg_price = format(int(c_avg_price), ',')
        c_max_price = format(int(c_max_price), ',')
        min_price = format(int(min_price), ',')
        avg_price = format(int(avg_price), ',')
        max_price = format(int(max_price), ',')


    # 연산 결과를 result.html로 전달
        return render_template('main_result.html', f_total_min_price=f_total_min_price,
                           f_total_avg_price=f_total_avg_price, f_total_max_price=f_total_max_price,
                           h_min_price=h_min_price,h_avg_price=h_avg_price,h_max_price=h_max_price,
                           c_min_price=c_min_price,c_avg_price=c_avg_price,c_max_price=c_max_price,
                           min_price=min_price,avg_price=avg_price,max_price=max_price)
    

    if request.method == 'POST':
        low_option = request.form.get('lowprice_option')
        mid_option = request.form.get('midprice_option')
        high_option = request.form.get('highprice_option')

        # 최저가
        if low_option =='항공':
            return redirect('/flight_min')
        elif low_option =='숙박':
            return redirect('/hotel_min')
        elif low_option =='렌트':
            return redirect('/rentcar_min')
        
        # 평균가
        if mid_option =='항공':
            return redirect('/flight_mid')
        elif mid_option =='숙박':
            return redirect('/hotel_mid')
        elif mid_option =='렌트':
            return redirect('/rentcar_mid')
        
        # 최고가
        if high_option =='항공':
            return redirect('/flight_max')
        elif high_option =='숙박':
            return redirect('/hotel_max')
        elif high_option =='렌트':
            return redirect('/rentcar_max')
        else:       # 아무것도 선택하지 않았을 경우
            return render_template('main_result.html')

# dashboard page    
@app.route('/dash', methods=['GET','POST'])
def dash():
    return render_template('dash.html')

######## 최저가 ########
# 항공편 추천
@app.route('/flight_min')
def flight_min():
    return render_template('min_flight.html')

# 호텔 추천
@app.route('/hotel_min')
def hotel_min():
    return render_template('min_hotel.html')

# 렌트카 추천
@app.route('/rentcar_min')
def rentcar_min():
    return render_template('min_rentcar.html')

######## 평균가 ########
# 항공편 추천
@app.route('/flight_mid')
def flight_mid():
    return render_template('avg_flight.html')

# 호텔 추천
@app.route('/hotel_mid')
def hotel_mid():
    return render_template('avg_hotel.html')

# 렌트카 추천
@app.route('/rentcar_mid')
def rentcar_mid():
    return render_template('avg_rentcar.html')

######## 최고가 ########
# 항공편 추천
@app.route('/flight_max')
def flight_max():
    return render_template('max_flight.html')

# 호텔 추천
@app.route('/hotel_max')
def hotel_max():
    return render_template('max_hotel.html')

# 렌트카 추천
@app.route('/rentcar_max')
def rentcar_max():
    return render_template('max_rentcar.html')

if __name__ == '__main__':
    app.run(debug=True)
