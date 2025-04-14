from app import app, db, User

# 在應用程式上下文中執行資料庫查詢
with app.app_context():
    user = User.query.first()
    print(user)

# 這段程式碼可以用來檢查資料庫資料

with app.app_context():
    user = User.query.first()
    print(f"User ID: {user.id}, Username: {user.username}, Email: {user.email}")
