# __init__

from flask import Flask
from flask import render_template
from flask import request
from flask import redirect
import psycopg2

app = Flask(__name__) # flask application 생성
f_min_reco_1, f_min_reco_2 = None, None
f_max_reco_1, f_max_reco_2 = None, None
f_avg_reco_1, f_avg_reco_2 = None, None
c_min_reco, c_avg_reco, c_max_reco = None, None, None

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
    global f_min_reco_1, f_min_reco_2
    global f_max_reco_1, f_max_reco_2
    global f_avg_reco_1, f_avg_reco_2
    global c_min_reco, c_avg_reco, c_max_reco
    global h_min_reco, h_avg_reco, h_max_reco


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
            SELECT *
            FROM flight_gimpo_jeju
            WHERE date = %s
            ORDER BY price ASC
        """, (input_value_1,))
        f_min_reco_1 = [cur.fetchone() for _ in range(5)]
        f_min_price_1 = f_min_reco_1[0][-2]

        # flight_jeju_gimpo 테이블에서 날짜가 backDte인 행들의 최저가 가져오기
        cur.execute("""
            SELECT *
            FROM flight_jeju_gimpo
            WHERE date = %s
            ORDER BY price ASC
        """, (input_value_2,))
        f_min_reco_2 = [cur.fetchone() for _ in range(5)]
        f_min_price_2 = f_min_reco_2[0][-2]

        # flight_gimpo_jeju 테이블에서 날짜가 goDate인 행들의 평균가 가져오기
        cur.execute("""
        SELECT *
        FROM flight_gimpo_jeju
        WHERE date = %s
        ORDER BY ABS(price - (SELECT AVG(price) FROM flight_gimpo_jeju WHERE date = %s))
        """, (input_value_1, input_value_1))
        f_avg_reco_1 = [cur.fetchone() for _ in range(5)]
        f_avg_price_1 = f_avg_reco_1[0][-2]

        # flight_jeju_gimpo 테이블에서 날짜가 backDate인 행들의 평균가 가져오기
        cur.execute("""
        SELECT *
        FROM flight_jeju_gimpo
        WHERE date = %s
        ORDER BY ABS(price - (SELECT AVG(price) FROM flight_jeju_gimpo WHERE date = %s))
        """, (input_value_2, input_value_2))
        f_avg_reco_2 = [cur.fetchone() for _ in range(5)]
        f_avg_price_2 = f_avg_reco_2[0][-2]

        # flight_gimpo_jeju 테이블에서 날짜가 goDate인 행들의 최고가 가져오기
        cur.execute("""
            SELECT *
            FROM flight_gimpo_jeju
            WHERE date = %s
            ORDER BY price DESC
        """, (input_value_1,))
        f_max_reco_1 = [cur.fetchone() for _ in range(5)]
        f_max_price_1 = f_max_reco_1[0][-2]
        # flight_jeju_gimpo 테이블에서 날짜가 backDate인 행들의 최고가 가져오기
        cur.execute("""
            SELECT *
            FROM flight_jeju_gimpo
            WHERE date = %s
            ORDER BY price DESC
        """, (input_value_2,))
        f_max_reco_2 = [cur.fetchone() for _ in range(5)]
        f_max_price_2 = f_max_reco_2[0][-2]

        # 최저가 더한 값
        f_total_min_price = f_min_price_1 + f_min_price_2

        # 중간가 더한 값
        f_total_avg_price = f_avg_price_1 + f_avg_price_2

        # 최고가 더한 값
        f_total_max_price = f_max_price_1 + f_max_price_2
        
        #호텔 최저가
        
        # feature 0 : checkin_date 1 : checkin_day 2 : checkout_date 3 : checkout_day
        #         4 : hotel_name   5 : location    6 : grade         7 : score
        #         8 : customer_num 9 : price      10 : stay_period
        
        if input_value_3 <= 2:
            customer_num = 2
        elif input_value_3 == 3:
            customer_num = 3
        elif input_value_3 == 4:
            customer_num = 4
            
        
        cur.execute("""
            SELECT *
            FROM hotel_total
            WHERE customer_num = %s AND checkin_date = %s AND checkout_date = %s
            ORDER BY price ASC
        """, (customer_num, input_value_1, input_value_2))

        h_min_reco = [cur.fetchone() for _ in range(5)]
        h_min_price = h_min_reco[0][-2]
        # 호텔 평균가

        # feature 0: checkin_date 1: checkin_day 2: checkout_date 3: checkout_day
        # 4: hotel_name 5: location 6: grade 7: score
        # 8: customer_num 9: price 10: stay_period

        cur.execute("""
        SELECT *
        FROM hotel_total
        WHERE customer_num = %s AND checkin_date = %s AND checkout_date = %s AND price <= 3000000
        ORDER BY ABS(price - (SELECT AVG(price) FROM hotel_total
        WHERE customer_num = %s AND checkin_date = %s AND checkout_date = %s AND price <= 3000000))
        LIMIT 5
        """, (customer_num, input_value_1, input_value_2,customer_num, input_value_1, input_value_2))

        h_avg_reco = [cur.fetchone() for _ in range(5)]
        h_avg_price = h_avg_reco[0][-2]
        #호텔 최고가
        
        # feature 0 : checkin_date 1 : checkin_day 2 : checkout_date 3 : checkout_day
        #         4 : hotel_name   5 : location    6 : grade         7 : score
        #         8 : customer_num 9 : price      10 : stay_period
        
        cur.execute("""
            SELECT *
            FROM hotel_total
            WHERE customer_num = %s AND checkin_date = %s AND checkout_date = %s AND price <= 3000000
            ORDER BY price DESC
        """, (customer_num, input_value_1, input_value_2))

        h_max_reco = [cur.fetchone() for _ in range(5)]
        h_max_price = h_max_reco[0][-2]
        
        # if input_value_3 <= 3:
        #     num_seat= 5
        # elif input_value_3 == 4:
        #     num_seat= 7

        
        #렌터카 최저가
        # feature : rent_date,rent_day,return_date,return_day,car_name,oiltype,num_seat,price,reserve_avail, rent_period, img_url
        cur.execute("""
            SELECT *
            FROM car_total
            WHERE num_seat <= %s AND rent_date = %s AND return_date = %s AND reserve_avail = 1
            ORDER BY price
        """, (5 if input_value_3 <= 3 else 7, input_value_1, input_value_2))
        c_min_reco = [cur.fetchone() for _ in range(5)]
        c_min_price = c_min_reco[0][-4]
        
        #렌터카 평균가
        cur.execute("""
        SELECT *
        FROM car_total
        WHERE num_seat <= %s AND rent_date = %s AND return_date = %s 
        ORDER BY ABS(price - (SELECT AVG(price) FROM car_total
        WHERE num_seat <= %s AND rent_date = %s AND return_date = %s ))
        LIMIT 5
        """, (5 if input_value_3 <= 3 else 7, input_value_1, input_value_2,5 if input_value_3 <= 3 else 7, input_value_1, input_value_2))

        c_avg_reco = [cur.fetchone() for _ in range(5)]
        c_avg_price = c_avg_reco[0][-4]
        
        #렌터카 최고가
        cur.execute("""
            SELECT *
            FROM car_total
            WHERE num_seat <= %s AND rent_date = %s AND return_date = %s AND reserve_avail = 1
            ORDER BY price DESC
        """, (5 if input_value_3 <= 3 else 7, input_value_1, input_value_2))
        c_max_reco = [cur.fetchone() for _ in range(5)]
        c_max_price = c_max_reco[0][-4]
        
        #항공,호텔,렌터카의 최저가,평균가,최고가 합산

        
        f_total_min_price = f_total_min_price * input_value_3
        f_total_avg_price = f_total_avg_price * input_value_3
        f_total_max_price = f_total_max_price * input_value_3

        f_total_min_price = format(int(f_total_min_price), ',')
        f_total_avg_price = format(int(f_total_avg_price), ',')
        f_total_max_price = format(int(f_total_max_price), ',')

        h_min_price = format(int(h_min_price), ',')
        h_avg_price = format(int(h_avg_price), ',')
        h_max_price = format(int(h_max_price), ',')

        c_min_price = format(int(c_min_price), ',')
        c_avg_price = format(int(c_avg_price), ',')
        c_max_price = format(int(c_max_price), ',')

        min_price = int(f_total_min_price.replace(',', '')) + int(h_min_price.replace(',', '')) + int(c_min_price.replace(',', ''))
        avg_price = int(f_total_avg_price.replace(',', '')) + int(h_avg_price.replace(',', '')) + int(c_avg_price.replace(',', ''))
        max_price = int(f_total_max_price.replace(',', '')) + int(h_max_price.replace(',', '')) + int(c_max_price.replace(',', ''))

        min_price = format(min_price, ',')
        avg_price = format(avg_price, ',')
        max_price = format(max_price, ',')


    # 연산 결과를 result.html로 전달
        return render_template('main_result.html', f_total_min_price=f_total_min_price,
                           f_total_avg_price=f_total_avg_price, f_total_max_price=f_total_max_price,
                           h_min_price=h_min_price,h_avg_price=h_avg_price,h_max_price=h_max_price,
                           c_min_price=c_min_price,c_avg_price=c_avg_price,c_max_price=c_max_price,
                           min_price=min_price,avg_price=avg_price,max_price=max_price,input_value_3=input_value_3,
                           num_seat_min=c_min_reco[0][-5],num_seat_avg=c_avg_reco[0][-5],num_seat_max=c_max_reco[0][-5],
                           customer_num=customer_num)
    

    if request.method == 'POST':
        low_option = request.form.get('lowprice_option')
        avg_option = request.form.get('avgprice_option')
        high_option = request.form.get('highprice_option')

        # 최저가
        if low_option =='항공':
            return redirect('/flight_min')
        elif low_option =='숙박':
            return redirect('/hotel_min')
        elif low_option =='렌트':
            return redirect('/rentcar_min')
        
        # 중간가
        if avg_option =='항공':
            return redirect('/flight_avg')
        elif avg_option =='숙박':
            return redirect('/hotel_avg')
        elif avg_option =='렌트':
            return redirect('/rentcar_avg')
        
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

@app.route('/dash_flight', methods=['GET','POST'])
def dash_flight():
    return render_template('dash_flight.html')

@app.route('/dash_hotel', methods=['GET','POST'])
def dash_hotel():
    return render_template('dash_hotel.html')

@app.route('/dash_rentcar', methods=['GET','POST'])
def dash_rentcar():
    return render_template('dash_rentcar.html')





# 항공편 데이터 dict로 만들기
# dict의 key [0 - date, 1 - day, 2 - start_time, 3 - arrival_time, 4 - airline, 5 - flight_time, 6 - seat, 7 - price, 8 - mark_url]
def f_make_dict(data):
    dict_ = {}
    for i in range(1, len(data[0])):
        temp = []
        for reco in data:
            if reco == None:
                break
            temp.append(reco[i])
        
        dict_[i] = temp

    # 날짜, 가격, 시간 포멧 설정
    dict_[0] = ('0' + str(data[0][0])[0] + '.' + str(data[0][0])[1:])
    dict_[1] = dict_[1][0]
    dict_[2] = ['0' + str(time)[0] + '시 ' + str(time)[1:] + '분' if len(str(time)) == 3 else str(time)[:2] + '시 ' + str(time)[2:] + '분' for time in dict_[2]]
    dict_[3] = ['0' + str(time)[0] + '시 ' + str(time)[1:] + '분' if len(str(time)) == 3 else str(time)[:2] + '시 ' + str(time)[2:] + '분' for time in dict_[3]]
    dict_[7] = [format(price, ',') for price in dict_[7]]
    return dict_

# 렌터카 데이터 dict로 만들기
# dict의 키 [0 - rent_date, 1 - rent_day, 2 - return_date, 3 - return_day, 4 - car_name, 5 - oiltype, 6 - num_seat, 7 - price, 8 - reserve_avail, 9 - rent_period, 10 - img_url]
def c_make_dict(data):
    dict_ = {}
    for i in range(4, len(data[0])):
        temp = []
        for reco in data:
            if reco == None:
                break
            temp.append(reco[i])
        
        dict_[i] = temp

    # 날짜, 가격, 시간 포멧 설정
    dict_[0] = ('0' + str(data[0][0])[0] + '.' + str(data[0][0])[1:])
    dict_[2] = ('0' + str(data[0][2])[0] + '.' + str(data[0][2])[1:])
    dict_[1] = data[0][1]
    dict_[3] = data[0][3]

    dict_[7] = [format(price, ',') for price in dict_[7]]
    dict_[9] = data[0][9]
    return dict_

def h_make_dict(data):
    dict_ = {}
    for i in range(4, len(data[0])-1):
        temp = []
        for reco in data:
            if reco == None:
                break
            temp.append(reco[i])
        
        dict_[i] = temp

    # 날짜, 가격, 시간 포멧 설정 6: grade 7: score
    dict_[0] = ('0' + str(data[0][0])[0] + '.' + str(data[0][0])[1:])
    dict_[2] = ('0' + str(data[0][2])[0] + '.' + str(data[0][2])[1:])
    dict_[1] = data[0][1]
    dict_[3] = data[0][3]
    dict_[6] = ['정보없음' if dict_[6][i] == 0 else str(dict_[6][i]) + '성급' for i in range(len(dict_[6]))]
    dict_[7] = ['정보없음' if dict_[7][i] == 0 else dict_[7][i] for i in range(len(dict_[7]))]
    dict_[9] = [format(price, ',') for price in dict_[9]]
    dict_[10] = data[0][10]
    return dict_

def h_avg_make_dict(data):
    dict_ = {}
    for i in range(3, len(data[0])-1):
        temp = []
        for reco in data:
            if reco == None:
                break
            temp.append(reco[i])
        
        dict_[i] = temp

    # 날짜, 가격, 시간 포멧 설정
    dict_[0] = ('0' + str(data[0][0])[0] + '.' + str(data[0][0])[1:])
    dict_[2] = ('0' + str(data[0][2])[0] + '.' + str(data[0][2])[1:])
    dict_[1] = data[0][1]
    dict_[3] = data[0][3]

    dict_[9] = [format(price, ',') for price in dict_[9]]
    dict_[10] = data[0][10]
    return dict_


######## 최저가 ########
@app.route('/flight_min')

# 항공편 추천
def flight_min():
    global f_min_reco_1, f_min_reco_2
    f_min_dict_1 = f_make_dict(f_min_reco_1)
    f_min_dict_2 = f_make_dict(f_min_reco_2)
    show_num = min(len(f_min_dict_1[2]), len(f_min_dict_2[2])) - 1
    repeat = range(1, show_num + 1)
    schedule = str(int(f_min_dict_2[0][-2:]) - int(f_min_dict_1[0][-2:])) + '박 ' + str(int(f_min_dict_2[0][-2:]) - int(f_min_dict_1[0][-2:]) + 1) + '일'
    return render_template('min_flight.html', f_min_dict_1=f_min_dict_1, f_min_dict_2=f_min_dict_2, show_num=show_num, repeat = repeat, schedule=schedule)

# 호텔 추천
@app.route('/hotel_min')
def hotel_min():
    global h_min_reco
    h_min_dict = h_make_dict(h_min_reco)
    show_num = len(h_min_dict[5]) - 1
    repeat = range(1, show_num + 1)
    schedule = h_min_dict[10][:2]
    return render_template('min_hotel.html', h_min_dict=h_min_dict, show_num=show_num, repeat=repeat, schedule=schedule)

# 렌트카 추천
@app.route('/rentcar_min')
def rentcar_min():
    global c_min_reco
    c_min_dict = c_make_dict(c_min_reco)
    show_num = len(c_min_dict[5]) - 1
    repeat = range(1, show_num + 1)
    schedule = c_min_dict[9][0] + '일'
    return render_template('min_rentcar.html', c_min_dict=c_min_dict, show_num=show_num, repeat=repeat, schedule=schedule)

######## 평균가 ########
# 항공편 추천
@app.route('/flight_avg')
def flight_avg():
    global f_avg_reco_1, f_avg_reco_2
    f_avg_dict_1 = f_make_dict(f_avg_reco_1)
    f_avg_dict_2 = f_make_dict(f_avg_reco_2)
    show_num = min(len(f_avg_dict_1[2]), len(f_avg_dict_2[2])) - 1
    repeat = range(1, show_num + 1)
    schedule = str(int(f_avg_dict_2[0][-2:]) - int(f_avg_dict_1[0][-2:])) + '박 ' + str(int(f_avg_dict_2[0][-2:]) - int(f_avg_dict_1[0][-2:]) + 1) + '일'
    return render_template('avg_flight.html', f_avg_dict_1=f_avg_dict_1, f_avg_dict_2=f_avg_dict_2, show_num=show_num, repeat=repeat, schedule=schedule)

# 호텔 추천
@app.route('/hotel_avg')
def hotel_avg():
    global h_avg_reco
    h_avg_dict = h_make_dict(h_avg_reco)
    show_num = len(h_avg_dict[5]) - 1
    repeat = range(1, show_num + 1)
    schedule = h_avg_dict[10][:2]
    return render_template('avg_hotel.html', h_avg_dict=h_avg_dict, show_num=show_num, repeat=repeat, schedule=schedule)

# 렌트카 추천
@app.route('/rentcar_avg')
def rentcar_avg():
    global c_avg_reco
    c_avg_dict = c_make_dict(c_avg_reco)
    show_num = len(c_avg_dict[5]) - 1
    repeat = range(1, show_num + 1)
    schedule = c_avg_dict[9][0] + '일'
    return render_template('avg_rentcar.html', c_avg_dict=c_avg_dict, show_num=show_num, repeat=repeat, schedule=schedule)   

######## 최고가 ########
# 항공편 추천
@app.route('/flight_max')
def flight_max():
    global f_max_reco_1, f_max_reco_2
    f_max_dict_1 = f_make_dict(f_max_reco_1)
    f_max_dict_2 = f_make_dict(f_max_reco_2)
    show_num = min(len(f_max_dict_1[2]), len(f_max_dict_2[2])) - 1
    repeat = range(1, show_num + 1)
    schedule = str(int(f_max_dict_2[0][-2:]) - int(f_max_dict_1[0][-2:])) + '박 ' + str(int(f_max_dict_2[0][-2:]) - int(f_max_dict_1[0][-2:]) + 1) + '일'
    return render_template('max_flight.html', f_max_dict_1=f_max_dict_1, f_max_dict_2=f_max_dict_2, show_num=show_num, repeat = repeat, schedule=schedule)

# 호텔 추천
@app.route('/hotel_max')
def hotel_max():
    global h_max_reco
    h_max_dict = h_make_dict(h_max_reco)
    show_num = len(h_max_dict[5]) - 1
    repeat = range(1, show_num + 1)
    schedule = h_max_dict[10][:2]
    return render_template('max_hotel.html', h_max_dict=h_max_dict, show_num=show_num, repeat=repeat, schedule=schedule)

# 렌트카 추천
@app.route('/rentcar_max')
def rentcar_max():
    global c_max_reco
    c_max_dict = c_make_dict(c_max_reco)
    show_num = len(c_max_dict[5]) - 1
    repeat = range(1, show_num + 1)
    schedule = c_max_dict[9][0] + '일'
    return render_template('max_rentcar.html', c_max_dict=c_max_dict, show_num=show_num, repeat=repeat, schedule=schedule)

if __name__ == '__main__':
    app.run(debug=True)
