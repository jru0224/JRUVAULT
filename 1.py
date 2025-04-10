# -*- coding: utf-8 -*-
"""
Created on Thu Apr  3 12:22:00 2025

@author: wu
"""
from flask import Flask, jsonify
import mysql.connector
from mysql.connector import Error

app = Flask(__name__)

# 数据库连接函数
def create_connection():
    try:
        conn = mysql.connector.connect(
            host='127.0.0.1',  # 或者 'localhost'
            port=3306,          # MySQL 默认端口
            user='root',        # 数据库用户名
            password='password', # 数据库密码
            database='shopping'  # 目标数据库名称
        )
        if conn.is_connected():
            return conn
        else:
            return None
    except Error as e:
        print(f"连接错误: {e}")
        return None

# 首页路由
@app.route('/')
def home():
    return "Hello, World!"

# 测试数据库连接
@app.route('/db_connection')
def db_connection():
    conn = create_connection()
    if conn:
        conn.close()
        return jsonify({"status": "success", "message": "成功连接到数据库"})
    else:
        return jsonify({"status": "error", "message": "无法连接到数据库"})

# 启动 Flask 应用
if __name__ == '__main__':
    app.run(debug=True)
