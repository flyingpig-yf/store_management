from flask import Flask, request, jsonify, render_template
#from ngrok_flask_cart import run_with_ngrok
import sqlite3

app = Flask(__name__)
#run_with_ngrok(app=app, auth_token='2UjzavhqznEK77WyxOIHXWZZKav_7yNfhDCU3iwLvj6LmYTKk')  # 使用ngrok创建隧道

# 初始化数据库
def init_db():
    with sqlite3.connect('store.db') as conn:
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS products (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                barcode TEXT UNIQUE,
                name TEXT,
                purchase_price REAL,
                selling_price REAL,
                stock INTEGER
            )
        ''')
        # 插入一些示例数据
        cursor.execute('''
            INSERT OR IGNORE INTO products (barcode, name, purchase_price, selling_price, stock)
            VALUES
            ('123456', '可乐', 2.0, 3.0, 100),
            ('654321', '零食', 1.5, 2.5, 150),
            ('100021942249', '电子计数跳绳', 1.5, 2.5, 150)
        ''')
        conn.commit()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/scan', methods=['POST'])
def scan_product():
    barcode = request.json.get('barcode')
    with sqlite3.connect('store.db') as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM products WHERE barcode=?", (barcode,))
        product = cursor.fetchone()
    if product:
        product_info = {
            'barcode': product[1],
            'name': product[2],
            'purchase_price': product[3],
            'selling_price': product[4],
            'stock': product[5]
        }
        return jsonify(product_info)
    else:
        return jsonify({"error": "未找到商品"}), 404

if __name__ == '__main__':
    init_db()
    app.run(debug=True, host='0.0.0.0')
