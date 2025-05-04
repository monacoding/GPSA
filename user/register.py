from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify
from werkzeug.security import generate_password_hash
from db import get_db
import pymysql  # ✅ 추가: DictCursor 사용을 위해

user = Blueprint('user', __name__, template_folder='templates/user')


@user.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        user_id = request.form['user_id']
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        print(f"[DEBUG] 수신된 값: user_id={user_id}, username={username}, email={email}")

        password_hash = generate_password_hash(password)
        print(f"[DEBUG] 비밀번호 해시 생성 완료")
        try:
            conn = get_db()
            cur = conn.cursor()
            cur.execute("""
                INSERT INTO users (user_id, username, email, password_hash)
                VALUES (%s, %s, %s, %s)
            """, (user_id, username, email, password_hash))
            conn.commit()
            print("[DEBUG] DB 삽입 및 커밋 성공")
            flash("회원가입이 완료되었습니다.")
            return redirect(url_for('user.register_success'))
        except Exception as e:
            conn.rollback()
            flash(f"에러 발생: {str(e)}")
            return redirect(url_for('user.register'))

    return render_template('register.html')


@user.route('/check_userid')
def check_userid():
    user_id = request.args.get('user_id')
    if not user_id:
        return jsonify({'exists': True})
    
    conn = get_db()
    cur = conn.cursor(pymysql.cursors.DictCursor)  # ✅ 수정
    cur.execute("SELECT id FROM users WHERE user_id = %s", (user_id,))
    result = cur.fetchone()
    return jsonify({'exists': bool(result)})


@user.route('/check_email')
def check_email():
    email = request.args.get('email')
    if not email:
        return jsonify({'exists': True})
    
    conn = get_db()
    cur = conn.cursor(pymysql.cursors.DictCursor)  # ✅ 수정
    cur.execute("SELECT id FROM users WHERE email = %s", (email,))
    result = cur.fetchone()
    return jsonify({'exists': bool(result)})


@user.route('/register/success')
def register_success():
    return render_template('register_success.html')