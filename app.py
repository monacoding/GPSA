from flask import Flask, render_template
from dotenv import load_dotenv
import os

# .env 파일 로드
load_dotenv()

# Flask 앱 생성
app = Flask(__name__)

@app.route('/')
def home():
    return render_template('home.html')

if __name__ == '__main__':
    HOST = os.getenv("FLASK_HOST")
    PORT = int(os.getenv("FLASK_PORT"))
    DEBUG_MODE = os.getenv("FLASK_DEBUG", "True").lower() == "true"

    app.run(host=HOST, port=PORT, debug=DEBUG_MODE) 