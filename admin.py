#Admin 權限保護
from flask import Blueprint, render_template, request, session, redirect, url_for, flash
import json

bp = Blueprint('admin', __name__, url_prefix='/admin')

def load_products():
    with open('products.json', encoding='utf-8') as f:
        return json.load(f)

def save_products(products):
    with open('products.json', 'w', encoding='utf-8') as f:
        json.dump(products, f, ensure_ascii=False, indent=2)

def get_next_id(products):
    return max([p['id'] for p in products], default=0) + 1

def admin_required(func):
    def wrapper(*args, **kwargs):
        if not session.get('is_admin'):
            flash('您沒有權限進入此頁面')
            return redirect(url_for('auth.login'))
        return func(*args, **kwargs)
    wrapper.__name__ = func.__name__  # 避免 Flask route 裝飾器衝突
    return wrapper

@bp.route('/products')
@admin_required
def admin_products():
    products = load_products()
    return render_template('admin_products.html', products=products)

@bp.route('/add', methods=['GET', 'POST'])
@admin_required
def add_product():
    if request.method == 'POST':
        products = load_products()
        new_product = {
            'id': get_next_id(products),
            'name': request.form['name'],
            'price': request.form['price'],
            'image': request.form['image']
        }
        products.append(new_product)
        save_products(products)
        flash('商品新增成功')
        return redirect(url_for('admin.admin_products'))
    return render_template('add_product.html')
@bp.route('/edit/<int:product_id>', methods=['GET', 'POST'])
@admin_required
def edit_product(product_id):
    products = load_products()
    product = next((p for p in products if p['id'] == product_id), None)

    if not product:
        flash('找不到商品')
        return redirect(url_for('admin.admin_products'))

    if request.method == 'POST':
        product['name'] = request.form.get('name')
        product['price'] = float(request.form.get('price'))
        product['image'] = request.form.get('image')
        save_products(products)
        flash('商品已更新')
        return redirect(url_for('admin.admin_products'))

    return render_template('edit_product.html', product=product)
@bp.route('/delete/<int:product_id>', methods=['POST'])
@admin_required
def delete_product(product_id):
    products = load_products()
    products = [p for p in products if p['id'] != product_id]
    save_products(products)
    flash('商品已刪除')
    return redirect(url_for('admin.admin_products'))
