from flask import Flask, jsonify
from flask_cors import CORS
import pymysql
from flask import request

app=Flask(__name__)
app.config['JSON_AS_ASCII'] = False  # 解决中文乱码问题
CORS(app)

def get_db():
    return pymysql.connect(
        host='localhost',
        user='root',
        password='123456',
        database='stock_system',
        charset='utf8mb4'
    )
    
@app.route('/api/login',methods=['POST'])
def login():
    data=request.json
    
    conn=get_db()
    cursor=conn.cursor(pymysql.cursors.DictCursor)
    
    cursor.execute('SELECT * FROM users WHERE username=%s AND password=%s',
                   (data['username'],data['password']))
    user=cursor.fetchone()
    
    cursor.close()
    conn.close()
    
    if user:
        return jsonify({
            'success':True,
            'message':'登录成功'})
    else:
        return jsonify({
            'success':False,
            'message':'用户名或密码错误'
        })
    
@app.route('/api/products')
def get_goods():
    keyword=request.args.get('keyword','')
    
    conn=get_db()
    cursor=conn.cursor(pymysql.cursors.DictCursor)
    
    sql='SELECT * FROM goods WHERE name LIKE %s'
    cursor.execute(sql,(f"%{keyword}%",))
    data=cursor.fetchall()
    
    cursor.close()
    conn.close()
    
    return jsonify(data)

@app.route('/api/products/<int:good_id>',methods=['DELETE'])
def delete_good(good_id):
    conn=get_db()
    cursor=conn.cursor()
    
    cursor.execute('DELETE FROM goods WHERE id=%s',(good_id,))
    conn.commit()
    
    cursor.close()
    conn.close()
    
    return jsonify({'message':'删除成功'})

@app.route('/api/products/<int:good_id>',methods=['PUT'])
def update_goods(good_id):
    data=request.json
    
    conn=get_db()
    cursor=conn.cursor()
    
    cursor.execute(
    """UPDATE goods
    SET name=%s,stock=%s,cost_price=%s,sell_price=%s
    WHERE id=%s
    """,(
        data['name'],
        data['stock'],
        data['cost_price'],
        data['sell_price'],
        good_id
    )
    )
    conn.commit()
    cursor.close()
    conn.close()
    return jsonify({'message':'更新成功'})

@app.route('/api/products',methods=['POST'])
def add_product():
    data=request.json
    
    conn=get_db()
    cursor=conn.cursor()
    
    cursor.execute("""
                   INSERT INTO goods(name,stock,cost_price,sell_price)
                   VALUES(%s,%s,%s,%s)
                   """,(
                       data['name'],
                       data['stock'],
                       data['cost_price'],
                       data['sell_price']
                   ))
    conn.commit()
    cursor.close()
    conn.close()
    return jsonify({'message':'新增成功'})

if __name__ == '__main__':
    app.run(debug=True)