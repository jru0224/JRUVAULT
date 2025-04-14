from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from werkzeug.security import generate_password_hash, check_password_hash
from app.models import User
from app import db

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
        if request.method == 'POST':
            username = request.form['username']
            email = request.form['email']
            password = request.form['password']

            # 檢查用戶是否已經註冊
            existing_user = User.query.filter_by(email=email).first()
            if existing_user:
                flash('此電子郵件已經被註冊過了！')
                return redirect(url_for('register'))

            # 密碼加密
            hashed_password = generate_password_hash(password)

            # 儲存用戶資料到資料庫
            try:
                new_user = User(username=username, email=email, password=hashed_password)
                db.session.add(new_user)
                db.session.commit()
                flash('註冊成功！請登入您的帳戶。')
                return redirect(url_for('login'))
            except Exception as e:
                db.session.rollback()  # 回滾事務
                flash(f'註冊失敗: {str(e)}')
                print(f"Error: {e}")  # 在控制台輸出錯誤訊息
                return redirect(url_for('register'))
        return render_template('register.html')

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        if not email or not password:
            flash('請填寫所有欄位！')
            return redirect(url_for('login'))

        # 查詢用戶資料
        user = User.query.filter_by(email=email).first()

        if user and check_password_hash(user.password, password):
            session['user_id'] = user.id
            session['username'] = user.username  # 儲存用戶名

            # 檢查是否為管理員，假設 admin@example.com 為管理員帳號
            session['is_admin'] = (user.email == 'admin@example.com')

            flash('登入成功！')
            return redirect(url_for('home'))
        else:
            flash('電子郵件或密碼錯誤')
            return redirect(url_for('login'))

    return render_template('login.html')

@auth_bp.route('/logout')
def logout():
    session.clear()
    flash('您已成功登出！')
    return redirect(url_for('auth.login'))
