# -*- coding: utf-8 -*-
"""
Created on Thu Apr  3 12:18:05 2025

@author: wu
"""

from flask import Flask, request, jsonify
import mysql.connector

app = Flask(__name__)

# MySQL 連線設定
conn = mysql.connector.connect(
   host='127.0.0.1',  # 使用主机名
    port=3306, 
    user='root',       # 你的 MySQL 使用者
    password='880224',  # 你的 MySQL 密碼
    database='shopping'   # 你的資料庫名稱
)
cursor = conn.cursor()

# 新增商品
@app.route('/products', methods=['POST'])
def add_product():
    data = request.json
    sql = "INSERT INTO products (name, price, stock) VALUES (%s, %s, %s)"
    values = (data['name'], data['price'], data['stock'])
    cursor.execute(sql, values)
    conn.commit()
    return jsonify({'message': '商品新增成功'}), 201

# 查詢所有商品
@app.route('/products', methods=['GET'])
def get_products():
    cursor.execute("SELECT * FROM products")
    products = cursor.fetchall()
    return jsonify(products)

# 查詢單一商品
@app.route('/products/<int:id>', methods=['GET'])
def get_product(id):
    cursor.execute("SELECT * FROM products WHERE id = %s", (id,))
    product = cursor.fetchone()
    if product:
        return jsonify(product)
    return jsonify({'error': '商品不存在'}), 404

# 刪除商品
@app.route('/products/<int:id>', methods=['DELETE'])
def delete_product(id):
    cursor.execute("DELETE FROM products WHERE id = %s", (id,))
    conn.commit()
    return jsonify({'message': '商品刪除成功'})

if __name__ == '__main__':
    app.run(debug=True)