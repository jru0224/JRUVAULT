from flask import Flask, render_template, request, redirect, url_for, flash, session
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
import json
import os

app = Flask(__name__, static_folder='static')
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'  # 設定 SQLite 資料庫
app.config['SECRET_KEY'] = 'your_secret_key'
db = SQLAlchemy(app)

# 用戶模型
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(120), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)

# 創建資料庫
with app.app_context():
    db.create_all()


# 載入商品資料
def load_products():
    with open('products.json', encoding='utf-8') as f:
        return json.load(f)

# 首頁
@app.route("/")
def index():
    products = load_products()
    print(products)
    return render_template("index.html", products=products)

# 商品詳細頁
@app.route("/product/<int:product_id>")
def product_detail(product_id):
    products = load_products()
    product = next((p for p in products if p["id"] == product_id), None)
    if not product:
        return "找不到商品", 404
    return render_template("product_detail.html", product=product)

@app.route('/admin/add-product', methods=['GET', 'POST'])
def add_product():
    if request.method == 'POST':
        new_product = {
            "id": get_next_product_id(),
            "name": request.form['name'],
            "price": request.form['price'],
            "image": request.form['image']
        }
        products = load_products()
        products.append(new_product)
        with open('products.json', 'w', encoding='utf-8') as f:
            json.dump(products, f, ensure_ascii=False, indent=2)
        return redirect('/')
    return render_template('add_product.html')

def get_next_product_id():
    products = load_products()
    if not products:
        return 1
    return max(p["id"] for p in products) + 1

@app.route('/admin/products')
def admin_products():
    products = load_products()
    return render_template('admin_products.html', products=products)



# 其他頁面
@app.route('/products')
def products():
    return render_template('products.html', cart_count=cart_count)


@app.route('/products/shoes')
def shoes():
    return render_template('shoes.html')

@app.route('/products/服裝')
def clothing():
    return render_template('clothing.html')

@app.route('/products/配件')
def fitting():
    return render_template('fitting.html')

@app.route('/products/玩具公仔')
def toys():
    return render_template('toys.html')

@app.route('/how_it_works')
def how_it_works():
    return render_template('how_it_works.html')

@app.route('/faq')
def faq():
    return render_template('faq.html')

@app.route('/contact', methods=['GET', 'POST'])
def contact():
    if request.method == 'POST':
        # 处理表单数据
        name = request.form['name']
        email = request.form['email']
        message = request.form['message']
        # 你可以在这里处理表单信息，比如保存到数据库或发送电子邮件等
        return f"感谢您的留言，{name}！我们会尽快与您联系。"

    # 如果是 GET 请求，渲染联络页面模板
    return render_template('contact.html')



    
@app.route('/register', methods=['GET', 'POST'])
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
        new_user = User(username=username, email=email, password=hashed_password)
        db.session.add(new_user)
        db.session.commit()

        flash('註冊成功！請登入您的帳戶。')
        return redirect(url_for('login'))
    
    return render_template('register.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        # 查詢用戶
        user = User.query.filter_by(email=email).first()

        if user and check_password_hash(user.password, password):
            # 登入成功，將用戶資料儲存至 session
            session['user_id'] = user.id
            flash('登入成功！')
            return redirect(url_for('home'))  # 登入後跳轉至主頁
        else:
            flash('電子郵件或密碼錯誤')

    return render_template('login.html')
@app.route('/home')
def home():
    if 'user_id' not in session:
        return redirect(url_for('login'))  # 如果沒有登入則重定向到登入頁面
    return render_template('home.html')

@app.route('/logout')
def logout():
    session.pop('user_id', None)  # 清除用戶資料
    flash('您已成功登出！')
    return redirect(url_for('login'))  # 登出後重定向到登入頁面
# 顯示購物車內容
@app.route('/cart')
def cart():
    cart = session.get('cart', [])
    return render_template('cart.html', cart=cart)
@app.context_processor
def cart_count():
    cart = session.get('cart', [])
    print(f"cart: {cart}, type of cart: {type(cart)}")  # 輸出 cart 的內容和類型
    return dict(cart_count=len(cart))  # 確保是列表並計算長度


# 加入商品到購物車
@app.route('/add-to-cart/<int:product_id>', methods=['POST'])
def add_to_cart(product_id):
    products = load_products()
    product = next((p for p in products if p["id"] == product_id), None)
    
    if product:
        # 如果購物車不存在，先初始化它
        if 'cart' not in session:
            session['cart'] = []
        
        # 檢查商品是否已經在購物車中
        cart = session['cart']
        existing_item = next((item for item in cart if item['id'] == product_id), None)
        
        if existing_item:
            # 如果商品已經存在，增加數量
            existing_item['quantity'] += 1
        else:
            # 如果商品不存在，將它加入購物車
            cart.append({'id': product_id, 'name': product['name'], 'price': product['price'], 'quantity': 1})

        session['cart'] = cart
        flash(f"已將 {product['name']} 加入購物車！")
        return redirect(url_for('cart'))

    flash("找不到該商品")
    return redirect(url_for('products'))
@app.route('/remove_from_cart/<int:product_id>')
def remove_from_cart(product_id):
    cart = session.get('cart', [])
    cart = [p for p in cart if p['id'] != product_id]
    session['cart'] = cart
    flash('商品已從購物車中移除')
    return redirect(url_for('cart'))


if __name__ == '__main__':
    app.run(debug=True,host='0.0.0.0', port=5002, use_reloader=False)
    