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
    input_value_3 = request.args.get('peopleValue')
    
    if request.method == 'GET':
        
        if input_value_1 is None or input_value_2 is None:
            return render_template('main.html')
        
        input_value_1 = int(input_value_1)
        input_value_2 = int(input_value_2)
        
        if input_value_3 is not None:
            input_value_3 = int(input_value_3)
        
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

        # flight_gimpo_jeju 테이블에서 날짜가 goDate인 행들의 중간가 가져오기
        cur.execute("""
            SELECT price
            FROM flight_gimpo_jeju
            WHERE date = %s
            ORDER BY price
        """, (input_value_1,))
        f_prices = cur.fetchall()
        f_med_price_1 = f_prices[len(f_prices)//2][0]

        # flight_jeju_gimpo 테이블에서 날짜가 backDate인 행들의 중간가 가져오기
        cur.execute("""
            SELECT price
            FROM flight_jeju_gimpo
            WHERE date = %s
            ORDER BY price
        """, (input_value_1,))
        f_prices = cur.fetchall()
        f_med_price_2 = f_prices[len(f_prices)//2][0]

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

        # 중간가 더한 값
        f_total_med_price = f_med_price_1 + f_med_price_2

        # 최고가 더한 값
        f_total_max_price = f_max_price_1 + f_max_price_2
        
        #호텔 최저가
        if input_value_3 <= 2:
            cur.execute("""
                SELECT MIN(price)
                FROM hotel_total
                WHERE customer_num = 2 AND checkout_date - checkin_date = %s - %s
            """, (input_value_2, input_value_1))
        else:
            cur.execute("""
                SELECT MIN(price)
                FROM hotel_total
                WHERE customer_num = 4 AND checkout_date - checkin_date = %s - %s
            """, (input_value_2, input_value_1))
        h_min_price = cur.fetchone()[0]
        
        #호텔 중간가
        if input_value_3 <= 2:
            cur.execute("""
                SELECT price
                FROM hotel_total
                WHERE customer_num = 2 AND checkout_date - checkin_date = %s - %s
                ORDER BY price
            """, (input_value_2, input_value_1))
        else:
            cur.execute("""
                SELECT price
                FROM hotel_total
                WHERE customer_num = 4 AND checkout_date - checkin_date = %s - %s
                ORDER BY price
            """, (input_value_2, input_value_1))
        h_prices = cur.fetchall()
        h_med_price = h_prices[len(h_prices)//2][0]
        
        if input_value_3 <= 2:
            cur.execute("""
                SELECT MAX(price)
                FROM hotel_total
                WHERE customer_num = 2 AND checkout_date - checkin_date = %s - %s
            """, (input_value_2, input_value_1))
        else:
            cur.execute("""
                SELECT MAX(price)
                FROM hotel_total
                WHERE customer_num = 4 AND checkout_date - checkin_date = %s - %s
            """, (input_value_2, input_value_1))
        h_max_price = cur.fetchone()[0]
        
        #렌터카 최저가
        cur.execute("""
            SELECT MIN(price)
            FROM car_total
            WHERE num_seat <= %s AND return_date - rent_date = %s - %s
        """, (5 if input_value_3 <= 3 else 7, input_value_2, input_value_1))

        c_min_price = cur.fetchone()[0]
            
            
        
        #렌터카 중간가
        cur.execute("""
            SELECT price
            FROM car_total
            WHERE num_seat <= %s AND return_date - rent_date = %s - %s
            ORDER BY price
        """, (5 if input_value_3 <= 3 else 7, input_value_2, input_value_1))

        c_prices = cur.fetchall()
        c_med_price = c_prices[len(c_prices)//2][0]
        
        #렌터카 최고가
        cur.execute("""
            SELECT MAX(price)
            FROM car_total
            WHERE num_seat <= %s AND return_date - rent_date = %s - %s
        """, (5 if input_value_3 <= 3 else 7, input_value_2, input_value_1))

        c_max_price = cur.fetchone()[0]
        
        #항공,호텔,렌터카의 최저가,중간가,최고가 합산

        
        f_total_min_price = f_total_min_price * input_value_3
        f_total_med_price = f_total_med_price * input_value_3
        f_total_max_price = f_total_max_price * input_value_3

        f_total_min_price = format(int(f_total_min_price), ',')
        f_total_med_price = format(int(f_total_med_price), ',')
        f_total_max_price = format(int(f_total_max_price), ',')

        h_min_price = format(int(h_min_price), ',')
        h_med_price = format(int(h_med_price), ',')
        h_max_price = format(int(h_max_price), ',')

        c_min_price = format(int(c_min_price), ',')
        c_med_price = format(int(c_med_price), ',')
        c_max_price = format(int(c_max_price), ',')

        min_price = int(f_total_min_price.replace(',', '')) + int(h_min_price.replace(',', '')) + int(c_min_price.replace(',', ''))
        med_price = int(f_total_med_price.replace(',', '')) + int(h_med_price.replace(',', '')) + int(c_med_price.replace(',', ''))
        max_price = int(f_total_max_price.replace(',', '')) + int(h_max_price.replace(',', '')) + int(c_max_price.replace(',', ''))

        min_price = format(min_price, ',')
        med_price = format(med_price, ',')
        max_price = format(max_price, ',')


    # 연산 결과를 result.html로 전달
        return render_template('main_result.html', f_total_min_price=f_total_min_price,
                           f_total_med_price=f_total_med_price, f_total_max_price=f_total_max_price,
                           h_min_price=h_min_price,h_med_price=h_med_price,h_max_price=h_max_price,
                           c_min_price=c_min_price,c_med_price=c_med_price,c_max_price=c_max_price,
                           min_price=min_price,med_price=med_price,max_price=max_price,input_value_3=input_value_3)
    

    if request.method == 'POST':
        low_option = request.form.get('lowprice_option')
        med_option = request.form.get('medprice_option')
        high_option = request.form.get('highprice_option')

        # 최저가
        if low_option =='항공':
            return redirect('/flight_min')
        elif low_option =='숙박':
            return redirect('/hotel_min')
        elif low_option =='렌트':
            return redirect('/rentcar_min')
        
        # 중간가
        if med_option =='항공':
            return redirect('/flight_med')
        elif med_option =='숙박':
            return redirect('/hotel_med')
        elif med_option =='렌트':
            return redirect('/rentcar_med')
        
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

######## 중간가 ########
# 항공편 추천
@app.route('/flight_med')
def flight_med():
    return render_template('med_flight.html')

# 호텔 추천
@app.route('/hotel_med')
def hotel_med():
    return render_template('med_hotel.html')

# 렌트카 추천
@app.route('/rentcar_med')
def rentcar_med():
    return render_template('med_rentcar.html')

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
