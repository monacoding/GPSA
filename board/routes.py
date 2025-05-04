#board/routes.py
from flask import Blueprint, render_template, request, redirect, url_for, jsonify
from werkzeug.utils import secure_filename
from datetime import datetime
from db import mysql
import os

board = Blueprint('board', __name__, template_folder='../templates')

UPLOAD_FOLDER = 'static/uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
@board.route('/board')
def board_home():
    query = request.args.get('q')  # 검색어
    cur = mysql.connection.cursor()

    if query:
        search_query = f"%{query}%"
        cur.execute("""
            SELECT * FROM posts 
            WHERE title LIKE %s OR content LIKE %s 
            ORDER BY id DESC
        """, (search_query, search_query))
    else:
        cur.execute("SELECT * FROM posts ORDER BY id DESC")

    posts = cur.fetchall()
    return render_template('board_list.html', posts=posts)


@board.route('/board/write', methods=['GET', 'POST'])
def write_post():
    if request.method == 'POST':
        category = request.form['category']
        title = request.form['title']
        content = request.form['content']
        attachment = request.files.get('attachment')

        filename = None
        if attachment and attachment.filename:
            filename = secure_filename(attachment.filename)
            attachment.save(os.path.join(UPLOAD_FOLDER, filename))

        cur = mysql.connection.cursor()
        cur.execute("""
            INSERT INTO posts (category, title, content, attachment)
            VALUES (%s, %s, %s, %s)
        """, (category, title, content, filename))
        mysql.connection.commit()

        return redirect(url_for('board.board_home'))

    return render_template('board_form.html')

@board.route('/board/post/<int:post_id>')
def view_post(post_id):
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM posts WHERE id = %s", (post_id,))
    post = cur.fetchone()
    if not post:
        return "게시글을 찾을 수 없습니다.", 404
    return render_template('board_post.html', post=post)

@board.route('/board/upload_image', methods=['POST'])
def upload_image():
    image = request.files.get('image')
    if image and image.filename:
        filename = secure_filename(image.filename)
        save_path = os.path.join(UPLOAD_FOLDER, filename)
        image.save(save_path)
        return jsonify({'url': url_for('static', filename=f'uploads/{filename}')})
    return jsonify({'error': 'No file'}), 400