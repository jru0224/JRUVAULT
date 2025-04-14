#登入邏輯加上 admin 儲存
from flask import Blueprint, render_template, request, redirect, session, flash, url_for
from werkzeug.security import generate_password_hash, check_password_hash
from app.models import User, db

bp = Blueprint('auth', __name__)

@bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        user = User.query.filter_by(email=email).first()

        if user and check_password_hash(user.password, password):
            session['user_id'] = user.id
            session['username'] = user.username
            session['is_admin'] = user.is_admin  # ✅ 儲存是否為 admin
            flash("登入成功")
            return redirect('/')
        flash("帳號或密碼錯誤")
    return render_template('login.html')

@bp.route('/logout')
def logout():
    session.clear()
    flash("已登出")
    return redirect(url_for('auth.login'))
