from flask import Flask, jsonify,send_file,request
from flask_cors import CORS
from werkzeug.utils import secure_filename
from flask import send_from_directory
from flask import request
from functools import wraps
import os
import uuid
import datetime
import pymysql
import csv
import jwt

app=Flask(__name__)
app.config['JSON_AS_ASCII'] = False  # 解决中文乱码问题
CORS(app)
SECRET_KEY='stock_system_2026'

def get_db():
    return pymysql.connect(
        host='localhost',
        user='root',
        password='123456',
        database='stock_system',
        charset='utf8mb4'
    )
    
def login_required(f):
    @wraps(f)
    def decorated(*args,**kwargs):
        print(request.headers)
        token=request.headers.get('Authorization')
        if not token:
            return jsonify({
                'success':False,
                'message':'缺少Token'
            }),401
        try:
            jwt.decode(
                token,
                SECRET_KEY,
                algorithms=['HS256']
            )
        except:
            return jsonify({
                'success':False,
                'message':'登录已失效'
            }),401
        return f(*args,**kwargs)
    return decorated
    

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
        token=jwt.encode(
            {
                'id':user['id'],
                'username':user['username'],
                'exp':datetime.datetime.utcnow()+datetime.timedelta(hours=12)
            },
            SECRET_KEY,
            algorithm='HS256'
        )
        
        return jsonify({
            'success':True,
            'message':'登录成功',
            'token':token
        })
    return jsonify({
            'success':False,
            'message':'用户名或密码错误'
        })
        
    
@app.route('/api/products')
@login_required
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
    #获得表单数据
    name=request.form.get('name')
    stock=request.form.get('stock')
    cost_price=request.form.get('cost_price')
    sell_price=request.form.get('sell_price')
    #获取上传文件
    file=request.files.get('file')
    conn=get_db()
    cursor=conn.cursor(pymysql.cursors.DictCursor)
    #查询原有商品
    cursor.execute(
        'SELECT * FROM goods WHERE id=%s',(good_id,)
    )
    old_good=cursor.fetchone()
    #默认使用旧图片
    image_url=old_good['image']
    #如果上传了新图片，处理上传
    if file:
        #创建目录
        upload_path=create_upload_path()
        #生成文件名
        filename=generate_filename(name,file.filename)
        #完整路径
        filepath=os.path.join(upload_path,filename)
        #保存文件
        file.save(filepath)
        #生成访问URL
        relative_path=filepath.replace(BASE_DIR,'').replace('\\','/')
        image_url=f"http://localhost:5000{relative_path}"
    #更新数据库
    cursor.execute("""
                   UPDATE goods
                   SET name=%s,stock=%s,cost_price=%s,sell_price=%s,image=%s
                     WHERE id=%s
                     """,
                     (
                         name,stock,cost_price,sell_price,image_url,good_id
                     )
                    )
    conn.commit()
    cursor.close()
    conn.close()
    return jsonify({'message':'更新成功'})

@app.route('/api/products',methods=['POST'])
@login_required
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


@app.route('/api/stock/in',methods=['POST'])

def stock_in():
    
    conn=get_db()
    cursor=conn.cursor(pymysql.cursors.DictCursor)
    
    try:
        data =request.json
        goods_id=data.get('goods_id')
        quantity=int(data.get('quantity'))
        remark=data.get('remark','')
        
        #查询商品
        cursor.execute(
            'SELECT * FROM goods WHERE id=%s',
            (goods_id,)
        )
        goods=cursor.fetchone()
        if not goods:
            cursor.close()
            conn.close()
            return jsonify({
                'success':False,
                'message':'商品不存在'
            })
            
        #原库存
        before_stock=goods['stock']
        #新库存
        after_stock=before_stock+quantity
        #更新库存
        cursor.execute(
            '''
            UPDATE goods
            SET stock=%s
            WHERE id=%s
            ''',
            (
                after_stock,
                goods_id
            )
        )
        #写入库存流水
        cursor.execute(
            '''
            INSERT INTO stock_records(
                goods_id,
                goods_name,
                type,
                quantity,
                before_stock,
                after_stock,
                cost_price,
                sell_price,
                remark
            )
            VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s)
            ''',
            (
                goods_id,
                goods['name'],
                'in',
                quantity,
                before_stock,
                after_stock,
                goods['cost_price'],
                goods['sell_price'],
                remark
            )
            
        )
        conn.commit()
        return jsonify({
            'success':True,
            'message':'入库成功'
        })
    except Exception as e:
        conn.rollback()
        
        return jsonify({
            'success':False,
            'message':str(e)
        })
    finally:
        cursor.close()
        conn.close()
    
    
@app.route('/api/stock/out', methods=['POST'])

def stock_out():

    data = request.json

    goods_id = data.get('goods_id')
    quantity = int(data.get('quantity'))
    remark = data.get('remark', '')

    conn = get_db()

    cursor = conn.cursor(pymysql.cursors.DictCursor)

    # 查询商品
    cursor.execute(
        'SELECT * FROM goods WHERE id=%s',
        (goods_id,)
    )

    goods = cursor.fetchone()

    if not goods:

        cursor.close()
        conn.close()

        return jsonify({
            'success': False,
            'message': '商品不存在'
        })

    # 当前库存
    before_stock = goods['stock']

    # 库存不足
    if quantity > before_stock:

        cursor.close()
        conn.close()

        return jsonify({
            'success': False,
            'message': '库存不足'
        })

    # 新库存
    after_stock = before_stock - quantity

    # 更新库存
    cursor.execute(
        '''
        UPDATE goods
        SET stock=%s
        WHERE id=%s
        ''',
        (
            after_stock,
            goods_id
        )
    )

    # 写入流水
    cursor.execute(
        '''
        INSERT INTO stock_records(
            goods_id,
            goods_name,
            type,
            quantity,
            before_stock,
            after_stock,
            cost_price,
            sell_price,
            remark
        )
        VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s)
        ''',
        (
            goods['id'],
            goods['name'],
            'out',
            quantity,
            before_stock,
            after_stock,
            goods['cost_price'],
            goods['sell_price'],
            remark
        )
    )

    conn.commit()

    cursor.close()
    conn.close()

    return jsonify({
        'success': True,
        'message': '出库成功'
    })
    

@app.route('/api/export/products')
@login_required
def export_products():
    conn =get_db()
    cursor=conn.cursor(pymysql.cursors.DictCursor)
    cursor.execute('SELECT * FROM goods')
    data=cursor.fetchall()
    cursor.close()
    conn.close()
    #创建exports文件夹
    export_dir=os.path.join(BASE_DIR,'exports')
    os.makedirs(export_dir,exist_ok=True)
    
    #文件名
    filename=f"products_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
    filepath=os.path.join(export_dir,filename)
    
    #写入csv
    with open(
        filepath,
        mode='w',
        newline='',
        encoding='utf-8-sig'
    ) as f:
        writer=csv.writer(f)
        #表头
        writer.writerow([
            'ID',
            '名称',
            '库存',
            '成本价',
            '售价'            
        ])
        #数据
        for item in data:
            writer.writerow([
                item['id'],
                item['name'],
                item['stock'],
                item['cost_price'],
                item['sell_price']
            ])
    #返回下载
    return send_file(
        filepath,
        as_attachment=True
    )
    
@app.route('/api/stock/records')
@login_required
def get_stock_records():

    keyword = request.args.get('keyword', '')

    conn = get_db()

    cursor = conn.cursor(pymysql.cursors.DictCursor)

    # 查询商品
    cursor.execute(
        '''
        SELECT * FROM goods
        WHERE name LIKE %s
        ORDER BY id DESC
        ''',
        (f"%{keyword}%",)
    )

    goods_list = cursor.fetchall()

    result = []

    # 查询每个商品的库存流水
    for goods in goods_list:

        cursor.execute(
            '''
            SELECT * FROM stock_records
            WHERE goods_id=%s
            ORDER BY create_time DESC
            ''',
            (goods['id'],)
        )

        records = cursor.fetchall()

        result.append({
            'goods': goods,
            'records': records
        })

    # 注意：
    # 这里必须在 for 循环结束后

    cursor.close()

    conn.close()

    return jsonify(result)

if __name__ == '__main__':
    app.run(host='0.0.0.0',port=5000)