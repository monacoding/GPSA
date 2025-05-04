import os
import json
import math
import pymysql
import CoolProp.CoolProp as CP
from flask import Flask, render_template
from dotenv import load_dotenv
from werkzeug.utils import secure_filename

# 사용자 정의 모듈
from db import get_db, close_db
from board.routes import board
from section.routes import section
from user.register import user
from calc import section0, section3

# PyMySQL을 MySQLdb처럼 사용
pymysql.install_as_MySQLdb()

# .env 환경 변수 로드
load_dotenv()

# Flask 앱 인스턴스 생성
app = Flask(__name__)
app.secret_key = os.getenv('SECRET_KEY')

# 파일 업로드 폴더
app.config['UPLOAD_FOLDER'] = 'static/uploads'
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

# 블루프린트 등록
app.register_blueprint(board)
app.register_blueprint(section)
app.register_blueprint(user, url_prefix='/user')

# DB 종료 함수 등록
app.teardown_appcontext(close_db)

# 홈 라우트
@app.route('/')
def home():
    return render_template('home.html')

# 전역에서 property map 로드
with open('calc/property_map.json') as f:
    PROPERTY_MAP = json.load(f)

# 실행
if __name__ == '__main__':
    HOST = os.getenv("FLASK_HOST", "127.0.0.1")
    PORT = int(os.getenv("FLASK_PORT", 5000))
    DEBUG_MODE = os.getenv("FLASK_DEBUG", "True").lower() == "true"
    app.run(host=HOST, port=PORT, debug=DEBUG_MODE)