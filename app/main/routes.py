from flask import Blueprint, render_template, request, session, redirect, url_for, flash
from app.utils import load_products, save_products, get_next_product_id

admin_bp = Blueprint('admin', __name__, url_prefix='/admin')

def admin_required(func):
    def wrapper(*args, **kwargs):
        if not session.get('is_admin'):
            flash('您沒有權限進入此頁面')
            return redirect(url_for('auth.login'))
        return func(*args, **kwargs)
    wrapper.__name__ = func.__name__
    return wrapper

@admin_bp.route('/products')
@admin_required
def admin_products():
    products = load_products()
    return render_template('admin_products.html', products=products)

@admin_bp.route('/add', methods=['GET', 'POST'])
@admin_required
def add_product():
    ...
