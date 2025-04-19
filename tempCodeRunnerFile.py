#app.py
from flask import Flask, render_template,request
from dotenv import load_dotenv
from calc import section0
import json
import os
import CoolProp.CoolProp as CP
# .env 파일 로드
load_dotenv()

# Flask 앱 생성
app = Flask(__name__)

@app.route('/') #메인 페이지
def home():
    return render_template('home.html')


# load property map once
with open('calc/property_map.json') as f:
    PROPERTY_MAP = json.load(f)
    
@app.route('/section/0',methods= ['GET','POST']) #SECTION0 물성치 확인, GET :기본요청, 페이지 열때 , POST: 사용자가 폼에 입력한 데이터를 보냈을때
def section0_route():
    result = None #계산 결과 초기화
    components = sorted(CP.FluidsList())  # 유체 리스트 생성
    
    if request.method == 'POST':
        """
        사용자가 데이터를 입력하고 [계산하기] 같은 버튼을 누르면, 
        HTML form이 POST 방식으로 전송됨
        이 조건이 계산 수행 조건임 
        """
        result = section0.section0_calculation(request.form)    
    return render_template('section0.html',result=result,components= components)
@app.route('/section/1') #SECTION 1
def section1_route():
    return render_template('section1.html')





if __name__ == '__main__':
    HOST = os.getenv("FLASK_HOST")
    PORT = int(os.getenv("FLASK_PORT"))
    DEBUG_MODE = os.getenv("FLASK_DEBUG", "True").lower() == "true"

    app.run(host=HOST, port=PORT, debug=DEBUG_MODE) 