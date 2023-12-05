from flask import Flask
import dbconnect as db
from geo import addr_to_lat_lon

import jinja2

app = Flask(__name__)


from flask import render_template,session, request, flash, jsonify, make_response,redirect,url_for
import hashlib
import jwt  #pyjwt 패키지
import datetime  # 토큰 만료시간
#import oracledb 

#con = oracledb.connect(user="system", password="2201330", dsn="localhost:1521/xe")   # DB에 연결 (호스트이름 대신 IP주소 가능)
#cursor = con.cursor()
app.secret_key = 'PANDA'  #jwt 토큰 생성 시 필요한 암호화 문자열

@app.route('/', methods=['GET'])    
def homepage():
    return render_template('main.html')


@app.route('/selectArea', methods=['GET'])    
def selectArea():
    return render_template('selectArea.j2')

# @app.route('/submit', methods=['GET', 'POST'])
# def map():
#     if request.method == 'POST':
#         # 검색어를 받아온다 (페이지 이동 및 지도에 표시하는 부분)
#         search_term = request.form.get('hosptalpharmacy')
#         return render_template('submit.html', searchTerm=search_term)

#     return render_template('submit.html')

@app.route('/submit', methods=['GET', 'POST'])
def map():
    return render_template('submit.j2', )

# 지역 선택하고, 나온 리스트에서 특정 병원 or 약국 눌렀을 때
@app.route('/target', methods=['POST'])
def target():
    selected_value = request.form['dataVal']
    print(selected_value)
    if '_hospital' in selected_value:
        # 병원 데이터 검색
        idx = selected_value.rstrip('_hospital')
        print(idx)
        temp = db.select_hhp(idx)
    else:
        # 약국 데이터 검색
        idx = selected_value.rstrip('_phamarcy')
        print(idx)
        temp = db.select_ppm(idx)
    print(temp)
    name = temp[0][0]
    addr = temp[0][1]
    number = temp[0][2]
    print(name, addr, number)
    lat, lon = addr_to_lat_lon(addr)
    print("lat: ", lat)
    print("lon: ", lon)
    return render_template('submit.j2', 
        name = name,
        addr = addr,
        number = number,
        lat=lat,
        lon=lon
    )

# 병원
@app.route('/get_data_hp',methods=['GET'])
def get_data_hp():
    fac_list = []
    # 데이터베이스에서 데이터 가져오기
    data = db.select_all_hp()
    for i in data:
        id = i[0]
        hp_type = i[1]
        hp_name = i[2]
        hp_addr = i[3]
        hp_numb = i[4]
        lat = i[5]
        git = i[6]

        fac_list.append(
            {
            "id" : id,
            "hp_type" : hp_type,
            "hp_name" : hp_name,
            "hp_addr" : hp_addr,
            "hp_numb" : hp_numb,
            "lat" : lat,
            "git" : git
            }
        )

    #print(fac_list)  
    # 데이터를 JSON 형태로 변환하여 반환
    #return {'fac_list':fac_list}
    return fac_list

# 약국 검색
@app.route('/get_data_pm',methods=['GET'])
def get_data_pm():
    fac_list = []
    # 데이터베이스에서 데이터 가져오기
    data = db.select_all_pm()
    for i in data:
        id = i[0]
        pm_name = i[1]
        pm_addr = i[3]
        pm_numb = i[4]
        lat = i[5]
        git = i[6]

        fac_list.append(
            {
            "id" : id,
            "pm_name" : pm_name,
            "pm_addr" : pm_addr,
            "pm_numb" : pm_numb,
            "lat" : lat,
            "git" : git
            }
        ) 

    #print(fac_list)  
    # 데이터를 JSON 형태로 변환하여 반환
    #return {'fac_list':fac_list}
    return fac_list

# 지역 선택하기 모드 시
@app.route('/get_data', methods=['POST'])
def get_data():
    select_area =request.form['sArea'] # 선택한 지역 받기 (군산 or 익산 or 전주)

    # DB 조회하기(선택 지역 포함된 row 추출) -> select * from table where {column} LIKE {select_area}
    hp_ = db.select_area_hp(select_area)
    pm_ = db.select_area_pm(select_area)

    # DB 조회 결과
    print("hp: ", hp_)
    print("pm: ", pm_)

    # 선택 지역에 있는 병원, 약국 보여주는 페이지 이동
    return render_template('selectArea.j2', 
        hp=hp_, 
        pm=pm_,
        enumerate=enumerate,
        str=str,
        len=len,
    )

# 직접 입력하기 모드 시
@app.route('/get_info', methods=['POST'])
def get_info():
    #data_type = request.args.get('type')  # 프론트엔드에서 type 매개변수를 전달받음
    search = request.form['search'] # 병원, 약국 전달 받음

    # DB 조회하기 -> select * from table where {column} LIKE {search}
    hp_ = db.search_hp(search)
    pm_ = db.search_pm(search)

    # DB 조회 결과
    print("hp: ", hp_)
    print("pm: ", pm_)

    # 중복 없음, 약국 or 병원 둘중 하나만 
    target_addr = ""
    target_name = ""
    target_numb = ""
    if len(hp_) > 0:
        target_addr=hp_[0][3] # 병원 주소 
        target_name=hp_[0][2]
        target_numb=hp_[0][4]
    else:
        target_addr=pm_[0][2] # 약국 주소
        target_name=pm_[0][1]
        target_numb=pm_[0][3]

    # 도로명 주소 가져오기 -> 위도, 경도 추출
    lat, lon = addr_to_lat_lon(target_addr)
    print("lat: ", lat)
    print("lon: ", lon)
    print("target_addr: ", target_addr)
    print("target_name: ", target_name)

    # 맵 보여주는 페이지 이동(위도, 경도)
    return render_template('submit.j2', 
        addr=target_addr,
        name=target_name,
        numb=target_numb,
        lat=lat,
        lon=lon
    )

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=17000, debug=True)