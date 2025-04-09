# -*- coding: utf-8 -*-
"""
Created on Thu Apr  3 12:22:00 2025

@author: wu
"""
import mysql.connector
from mysql.connector import Error

try:
    # 尝试连接到 MySQL 数据库
    conn = mysql.connector.connect(
        host='127.0.0.1',  # 或者 'localhost'
        port=3306,          # MySQL 默认端口
        user='root',        # 数据库用户名
        password='password', # 数据库密码
        database='shopping'  # 目标数据库名称
    )

    if conn.is_connected():
        print("成功连接到 MySQL 数据库")
    else:
        print("无法连接到 MySQL 数据库")

except Error as e:
    print(f"连接错误: {e}")

finally:
    if conn.is_connected():
        conn.close()  # 关闭连接
        print("数据库连接已关闭")
