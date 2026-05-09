from flask import Flask, jsonify
from flask_cors import CORS
import pymysql
from flask import request
import os
import uuid
import datetime
from werkzeug.utils import secure_filename
from flask import send_from_directory

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
    name=request.form.get('name')
    stock=request.form.get('stock')
    cost_price=request.form.get('cost_price')
    sell_price=request.form.get('sell_price')
    file=request.files.get('file')
    
    image_url=''
    if file:
        upload_path=create_upload_path()
        filename=generate_filename(name,file.filename)
        filepath=os.path.join(upload_path,filename)
        file.save(os.path.join(upload_path,filename))
        relative_path=filepath.replace(BASE_DIR,'').replace('\\','/')
        image_url=f"http://localhost:5000{relative_path}"
        
        
    conn=get_db()
    cursor=conn.cursor()
    
    cursor.execute("""
                   INSERT INTO goods(name,stock,cost_price,sell_price,image)
                   VALUES(%s,%s,%s,%s,%s)
                   """,(
                       name,
                       stock,
                       cost_price,
                       sell_price,
                       image_url
                   ))
    conn.commit()
    cursor.close()
    conn.close()
    return jsonify({'message':'新增成功'})

@app.route('/uploads/<path:filename>')
def get_file(filename):
    return send_from_directory('uploads',filename)

BASE_DIR =os.path.dirname(os.path.abspath(__file__))
UPLOAD_FOLDER=os.path.join(BASE_DIR,'uploads')

app.config['UPLOAD_FOLDER']=UPLOAD_FOLDER

def create_upload_path():
    now= datetime.datetime.now()
    
    path=os.path.join(
        app.config['UPLOAD_FOLDER'],
        'products',
        str(now.year),
        str(now.month),
        str(now.day)
    )
    os.makedirs(path,exist_ok=True)
    return path

def generate_filename(productr_name,original_filename):
    ext=original_filename.split('.')[-1]
    
    safe_name=secure_filename(productr_name)
    unique_id=uuid.uuid4().hex[:6]
    return f"{safe_name}_{unique_id}.{ext}"

if __name__ == '__main__':
    app.run(debug=True)