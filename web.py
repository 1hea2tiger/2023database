# -*- coding=utf-8 -*-
from flask import Flask, render_template, request, redirect, url_for, flash
from werkzeug.utils import secure_filename
import MySQLdb
import os
import datetime
import sys
import importlib

importlib.reload(sys)

from pathlib import Path
root = Path(__file__).parent
# 用当前脚本名称实例化Flask对象，方便flask从该脚本文件中获取需要的内容
app = Flask(__name__)

# 全局变量
username = "TJU"
# TODO: username变量的赋值  方法1：全局变量实现，随登录进行修改  方法2：给每个页面传递username
userRole = "BUYER"
notFinishedNum = 0
# 上传文件要储存的目录
UPLOAD_FOLDER = '/static/images/'
# 允许上传的文件扩展名的集合
ALLOWED_EXTENSIONS = set([ 'png', 'jpg', 'jpeg'])
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS

@app.route('/')
@app.route('/index')
# 首页
def indexpage():
    return render_template('index.html')
# 注册
@app.route('/register', methods=['GET', 'POST'])
def registerPage():
    global username
    global userRole
    if request.method == 'GET':
        return render_template('register.html')
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        phone = request.form.get('phone')
        address = request.form.get('address')
        userRole = request.form.get('userRole')
        print(userRole)
        print(username)
        # 连接数据库，默认数据库用户名root，密码空
        db = MySQLdb.connect("localhost", "root", "Leepoq126", "appDB", charset='utf8')
        if userRole == 'MERCHANTS':
            cursor = db.cursor()
            try:
                cursor.execute("use appDB")
            except:
                print("Error: unable to use database!")
            sql1 = "SELECT * from merchants where name = '{}' ".format(username)
            cursor.execute(sql1)
            db.commit()
            res1 = cursor.fetchall()
            num = 0
            for row in res1:
                num = num + 1
            # 如果已经存在该商家
            if num == 1:
                print("失败!花店已注册！")
                msg = "fail1"
            else:
                sql2 = "insert into merchants (name, password, phone, address) values ('{}', '{}', '{}', '{}') ".format(username, password, phone,address)
                try:
                    cursor.execute(sql2)
                    db.commit()
                    print("花店注册成功")
                    msg = "done1"
                except ValueError as e:
                    print("--->", e)
                    print("注册出错，失败")
                    msg = "fail1"
            return render_template('register.html', messages=msg, username=username, userRole=userRole)
        elif userRole == 'BUYER':
            cursor = db.cursor()
            try:
                cursor.execute("use appDB")
            except:
                print("Error: unable to use database!")
            sql1 = "SELECT * from buyer where name = '{}'".format(username)
            cursor.execute(sql1)
            db.commit()
            res1 = cursor.fetchall()
            num = 0
            for row in res1:
                num = num + 1
            # 如果已存在该用户
            if num == 1:
                print("用户已注册！请直接登录。")
                msg = "fail2"
            else:
                sql2 = "insert into buyer (name, password, phone, address) values ('{}', '{}', '{}', '{}') ".format(username, password, phone,address)
                try:
                    cursor.execute(sql2)
                    db.commit()
                    print("用户注册成功")
                    msg = "done2"
                except ValueError as e:
                    print("--->", e)
                    print("注册出错，失败")
                    msg = "fail2"
            return render_template('register.html', messages=msg, username=username, userRole=userRole)
# 登录
@app.route('/logIn', methods=['GET', 'POST'])
def logInPage():
    global username
    global userRole
    msg = ""
    if request.method == 'GET':
        return render_template('login.html')
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        userRole = request.form.get('userRole')
        print(userRole)
        print(username)
        # 连接数据库，默认数据库用户名root，密码空
        db = MySQLdb.connect("localhost", "root", "Leepoq126", "appDB", charset='utf8')

        if userRole == 'ADMIN':
            cursor = db.cursor()
            try:
                cursor.execute("use appDB")
            except:
                print("Error: unable to use database!")
            sql = "SELECT * from admin where name = '{}' and password='{}'".format(username, password)
            cursor.execute(sql)
            db.commit()
            res = cursor.fetchall()
            num = 0
            for row in res:
                num = num + 1
            # 如果存在该管理员且密码正确
            if num == 1:
                print("登录成功！欢迎管理员！")
                msg = "done1"
            else:
                print("您没有管理员权限或登录信息出错。")
                msg = "fail1"
            return render_template('login.html', messages=msg, username=username, userRole=userRole)

        elif userRole == 'MERCHANTS':
            cursor = db.cursor()
            try:
                cursor.execute("use appDB")
            except:
                print("Error: unable to use database!")
            sql = "SELECT * from merchants where name = '{}' and password='{}'".format(username, password)
            cursor.execute(sql)
            db.commit()
            res = cursor.fetchall()
            num = 0
            for row in res:
                num = num + 1
            # 如果存在该商家且密码正确
            if num == 1:
                print("登录成功！今天卖什么花！")
                msg = "done2"
            else:
                print("您没有用户权限，未注册或登录信息出错。")
                msg = "fail2"
            return render_template('login.html', messages=msg, username=username, userRole=userRole)

        elif userRole == 'BUYER':
            cursor = db.cursor()
            try:
                cursor.execute("use appDB")
            except:
                print("Error: unable to use database!")
            sql = "SELECT * from buyer where name = '{}' and password='{}'".format(username, password)
            cursor.execute(sql)
            db.commit()
            res = cursor.fetchall()
            num = 0
            for row in res:
                num = num + 1
            # 如果存在该用户且密码正确
            if num == 1:
                print("登录成功！今天买束花吧！")
                msg = "done3"
            else:
                print("您没有用户权限，未注册或登录信息出错。")
                msg = "fail3"
            return render_template('login.html', messages=msg, username=username, userRole=userRole)

# 管理员的花店列表页面
@app.route('/AdminList', methods=['GET', 'POST'])
def AdminListPage():
    msg = ""
    if request.method == 'GET':
        msg = ""
        # 连接数据库，默认数据库用户名root，密码空
        db = MySQLdb.connect("localhost", "root", "Leepoq126", "appDB", charset='utf8')
        cursor = db.cursor()
        try:
            cursor.execute("use appDB")
        except:
            print("Error: unable to use database!")

        # 查询
        sql = "SELECT * FROM merchants"
        cursor.execute(sql)
        res = cursor.fetchall()
        # print(res)
        # print(len(res))
        if len(res) != 0:
            msg = "done"
            print(msg)
            return render_template('AdminList.html', username=username, result=res, messages=msg)
        else:
            print("NULL")
            msg = "none"
            return render_template('AdminList.html', username=username, messages=msg)
    elif request.form["action"] == "移除":
        MERName = request.form.get('MERName')
        # 连接数据库，默认数据库用户名root，密码空
        db = MySQLdb.connect("localhost", "root", "Leepoq126", "appDB", charset='utf8')
        cursor = db.cursor()
        try:
            cursor.execute("use appDB")
        except:
            print("Error: unable to use database!")
        # 更新数据库
        # 删除flower的
        sql1 = "DELETE FROM flower WHERE m_id = '{}'".format(MERName)
        cursor.execute(sql1)
        db.commit()
        # 删除订单表里的
        sql2 = "DELETE FROM record WHERE m_id = '{}'".format(MERName)
        cursor.execute(sql2)
        db.commit()
        # 删除shoppingCart的
        sql3 = "DELETE FROM shopping_new WHERE m_id = '{}'".format(MERName)
        cursor.execute(sql3)
        db.commit()
        # 删除merchant的
        sql4 = "DELETE FROM merchants WHERE name = '{}'".format(MERName)
        cursor.execute(sql4)
        db.commit()
        print(sql4)

        msg = "delete"
        print(msg)

        return render_template('AdminList.html', username=username, messages=msg)
# 管理员查看评论列表
@app.route('/AdminComment', methods=['GET', 'POST'])
def AdminCommentPage():
    msg = ""
    if request.method == 'GET':
        msg = ""
        # 连接数据库，默认数据库用户名root
        db = MySQLdb.connect("localhost", "root", "Leepoq126", "appDB", charset='utf8')
        cursor = db.cursor()
        try:
            cursor.execute("use appDB")
        except:
            print("Error: unable to use database!")

        # 查询
        sql = "SELECT * FROM record WHERE isFinished = 1 AND comment is not null"
        cursor.execute(sql)
        res = cursor.fetchall()
        # print(res)
        # print(len(res))
        if len(res) != 0:
            msg = "done"
            print(msg)
            return render_template('AdminComment.html', username=username, result=res, messages=msg)
        else:
            print("NULL")
            msg = "none"
            return render_template('AdminComment.html', username=username, messages=msg)
    elif request.form["action"] == "按评分升序排列":
        db = MySQLdb.connect("localhost", "root", "Leepoq126", "appDB", charset='utf8')
        cursor = db.cursor()
        try:
            cursor.execute("use appDB")
        except:
            print("Error: unable to use database!")

        sql = "SELECT * FROM record WHERE isFinished = 1 AND comment is not null ORDER BY score"
        cursor.execute(sql)
        res = cursor.fetchall()
        # print(res)
        print(len(res))
        if len(res):
            msg = "done"
            print(msg)
            return render_template('AdminComment.html', username=username, result=res, messages=msg)
        else:
            print("NULL")
            msg = "none"
        return render_template('AdminComment.html', username=username, messages=msg)

# 用户登录后显示花店列表
@app.route('/BuyerList',methods=['GET', 'POST'])
def BuyerListPage():
    msg = ""
    if request.method == 'GET':
        msg = ""
        # 连接数据库，默认数据库用户名root，密码空
        db = MySQLdb.connect("localhost", "root", "Leepoq126", "appDB", charset='utf8')
        cursor = db.cursor()
        try:
            cursor.execute("use appDB")
        except:
            print("Error: unable to use database!")

        # 查询
        sql = "SELECT * FROM merchants"
        cursor.execute(sql)
        res = cursor.fetchall()
        # print(res)
        # print(len(res))
        if len(res) != 0:
            msg = "done"
            print(res)
            return render_template('BuyerList.html', username=username, result=res, messages=msg)
        else:
            print("NULL")
            msg = "none"
            return render_template('BuyerList.html', username=username, messages=msg)
# 选择商家进入列表
@app.route('/Menu',methods=['GET', 'POST'])
def Menu():
    msg = ""
    global merchant
    if request.form["action"] == "进入本店":
        merchant = request.form['merchant']
        print(merchant)
        msg = ""
        # 连接数据库，默认数据库用户名root，密码空
        db = MySQLdb.connect("localhost", "root", "Leepoq126", "appDB", charset='utf8')
        cursor = db.cursor()
        try:
            cursor.execute("use appDB")
        except:
            print("Error: unable to use database!")
        # 查询
        sql = "SELECT * FROM flower natural join class WHERE m_id = '%s'" % merchant
        cursor.execute(sql)
        res = cursor.fetchall()
        # print(res)
        # print(len(res))
        if len(res) != 0:
            msg = "done"
            print(msg)
            print(len(res))
            return render_template('Menu.html', username=username, MERCHANT=merchant, result=res, messages=msg)
        else:
            print("NULL")
            msg = "none"
            return render_template('Menu.html', username=username, MERCHANT=merchant, messages=msg)
    elif request.form["action"] == "本店推荐":
        db = MySQLdb.connect("localhost", "root", "Leepoq126", "appDB", charset='utf8')
        cursor = db.cursor()
        try:
            cursor.execute("use appDB")
        except:
            print("Error: unable to use database!")
        sql = "SELECT * FROM flower natural join class WHERE m_id = '%s' AND isSpecialty = 1" % merchant
        cursor.execute(sql)
        res = cursor.fetchall()
        print(res)
        print(len(res))
        if len(res):
            msg = "done"
            print(msg)
            return render_template('Menu.html', username=username, MERCHANT=merchant, result=res, messages=msg)
        else:
            print("NULL")
            msg = "none"
            return render_template('Menu.html', username=username, MERCHANT=merchant, messages=msg)
    elif request.form["action"] == "按销量排序":
        db = MySQLdb.connect("localhost", "root", "Leepoq126", "appDB", charset='utf8')
        cursor = db.cursor()
        try:
            cursor.execute("use appDB")
        except:
            print("Error: unable to use database!")
        print(merchant, "aaa")
        sql = "SELECT * FROM flower natural join class WHERE m_id = '%s' Order BY saleNumber DESC" % merchant
        cursor.execute(sql)
        res = cursor.fetchall()
        print(res)
        print(len(res))
        if len(res):
            msg = "done"
            print(msg)
            return render_template('Menu.html', username=username, MERCHANT=merchant, result=res, messages=msg)
        else:
            print("NULL")
            msg = "none"
            return render_template('Menu.html', username=username, MERCHANT=merchant, messages=msg)
    elif request.form["action"] == "按价格排序":
        db = MySQLdb.connect("localhost", "root", "Leepoq126", "appDB", charset='utf8')
        cursor = db.cursor()
        try:
            cursor.execute("use appDB")
        except:
            print("Error: unable to use database!")

        sql = "SELECT * FROM flower natural join class WHERE m_id = '%s' Order BY price DESC" % merchant
        cursor.execute(sql)
        res = cursor.fetchall()
        print(res)
        print(len(res))
        if len(res):
            msg = "done"
            print(msg)
            return render_template('Menu.html', username=username, MERCHANT=merchant, result=res, messages=msg)
        else:
            print("NULL")
            msg = "none"
            return render_template('Menu.html', username=username, MERCHANT=merchant, messages=msg)
# 查看商家评论
@app.route('/Comment',methods=['GET','POST'])
def Comment():
    msg = ""
    global merchant
    if request.method == 'GET':
        merchant=request.args.get('MERCHANT')
    elif request.form["action"] == "查看评价":
        merchant = request.form['merchant']
    print(merchant)
    msg = ""
    # 连接数据库，默认数据库用户名root
    db = MySQLdb.connect("localhost", "root", "Leepoq126", "appDB", charset='utf8')
    cursor = db.cursor()
    try:
        cursor.execute("use appDB")
    except:
        print("Error: unable to use database!")
    # 查询
    sql = "SELECT * FROM record WHERE m_id='%s' AND comment is not null AND isFinished = 1"% merchant
    cursor.execute(sql)
    res = cursor.fetchall()
    # print(res)
    # print(len(res))
    if len(res) != 0:
        msg = "done"
        print(msg)
        print(len(res))
        return render_template('Comment.html', username=username, MERCHANT=merchant, result=res, messages=msg)
    else:
        print("NULL")
        msg = "none"
    return render_template('Comment.html', username=username, MERCHANT=merchant, messages=msg)
# 购物车
@app.route('/myOrder',methods=['GET', 'POST'])
def shoppingCartPage():
    print("!!!")
    if request.method == 'GET':
        print("myOrder-->GET")
        db = MySQLdb.connect("localhost", "root", "Leepoq126", "appDB", charset='utf8')
        cursor = db.cursor()
        try:
            cursor.execute("use appDB")
        except:
            print("Error: unable to use database!")
        # 查询
        sql = "SELECT * FROM shopping_new"
        cursor.execute(sql)
        res = cursor.fetchall()
        # print(res)
        # print(len(res))
        if len(res) != 0:
            msg = "done"
            print(msg)
            print(len(res))
            return render_template('myOrder.html', username=username, result=res, messages=msg)
        else:
            print("NULL")
            msg = "none"
            return render_template('myOrder.html', username=username, messages=msg)
    elif request.form["action"] == "加入购物车":
        print("myShopping-->加入购物车")
        merchant = request.form['merchant']
        flowername = request.form['flowername']
        price = request.form['price']
        img_res = request.form['img_res']
        # img_res=""
        db = MySQLdb.connect("localhost", "root", "Leepoq126", "appDB", charset='utf8')
        cursor = db.cursor()
        try:
            cursor.execute("use appDB")
        except:
            print("Error: unable to use database!")
        # 所有的购物车数据(更新前)
        sql_init = "SELECT * from shopping_new"
        cursor.execute(sql_init)
        res_init = cursor.fetchall()
        # 寻找是否已加入
        sql_find = "SELECT f_num from shopping_new where f_id = '{}' and m_id='{}' and b_id='{}' ".format(flowername,merchant,username)
        cursor.execute(sql_find)
        res_find = cursor.fetchall()
        count = 0
        for row in res_find:
            count = count + 1
        # 找到
        if count == 1:
            num_update=int(res_find[0][0])+1
            print("???")
            sql = "Update shopping_new SET f_num ={},price={},img_res ='{}' where f_id = '{}' and m_id = '{}' and b_id='{}' ".format(num_update,price,img_res, flowername, merchant,username)
            cursor.execute(sql)
            # res = cursor.fetchall()
            db.commit()
        # 找不到
        else:
            sql = "insert into shopping_new  values ('{}','{}','{}','{}','{}','{}') ".format(username,merchant,flowername,1,price,img_res)
            cursor.execute(sql)
            # res = cursor.fetchall()
            db.commit()
        # 该用户所有的购物车数据(更新后)
        sql_res = "SELECT * from shopping_new where b_id='{}' ".format(username)
        cursor.execute(sql_res)
        res_total = cursor.fetchall()
        print("----------------!!!!!!!!!!!!!!!!!!!!")
        print(res_total)
        # print(len(res))
        if len(res_total) != 0:
            msg = "done"
            print(msg)
            print(len(res_total))
            return render_template('myOrder.html', username=username,count=len(res_total),result=res_total, messages=msg)
        else:
            print("NULL")
            msg = "none"
        return render_template('myOrder.html', username=username, messages=msg)
    elif request.form["action"] == "删除":
        print("删除")
        merchant = request.form['merchant']
        flowername = request.form['flowername']
        db = MySQLdb.connect("localhost", "root", "Leepoq126", "appDB", charset='utf8')
        cursor = db.cursor()
        sql = "DELETE FROM shopping_new where f_id = '{}' and m_id='{}' and b_id='{}' ".format(flowername,merchant,username)
        print(sql)
        dmsg = "done"
        try:
            cursor.execute(sql)
            db.commit()
            print("鲜花删除成功")
        except ValueError as e:
            print("--->", e)
            print("鲜花删除失败")
            dmsg = "fail"
        # 该用户所有的购物车数据(更新后)
        sql_res = "SELECT * from shopping_new where b_id='{}' ".format(username)
        cursor.execute(sql_res)
        res_total = cursor.fetchall()
        print("删除后")
        print(res_total)
        # print(len(res))
        if dmsg and len(res_total) != 0:
            dmsg = "done"
            print(dmsg)
            print(len(res_total))
            return render_template('myOrder.html', username=username, count=len(res_total), result=res_total,
                                   messages=dmsg)
        else:
            print("NULL")
            dmsg = "none"
            return render_template('myOrder.html', username=username, messages=dmsg)
    elif request.form["action"] == "结算":
        print("结算啦")
        db = MySQLdb.connect("localhost", "root", "Leepoq126", "appDB", charset='utf8')
        cursor = db.cursor()
        try:
            cursor.execute("use appDB")
        except:
            print("Error: unable to use database!")
        '''
        更新订购记录
        '''
        merchant = request.form['merchant']
        flowername = request.form['flowername']
        price = float(request.form['price'])
        count=int(request.form['amountNum'])
        mode = int(request.form['mode'])
        img_res=request.form['img_res']
        print("==*==")
        print(mode)
        f_table="merchants"
        f_name=merchant
        if mode == 1:
            print("自取")
        else:
            print("外送")
            f_table="buyer"
            f_name=username
        findSQL="select address from {} where name='{}'".format(f_table,f_name)
        print(findSQL)
        cursor.execute(findSQL)
        address=cursor.fetchall()[0][0]
        now_time=datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S") #系统时间
        # 插入新订单记录
        sql="insert into record (m_id,flower_name, mode, b_id,address,img_res,t_time,price) values ('{}', '{}', {}, '{}', '{}','{}', '{}',{}) ".format(merchant,flowername, mode, username,address,img_res,now_time,price*count)
        print(sql)
        cursor.execute(sql)
        res = cursor.rowcount
        db.commit()
        # print(res)
        # print(len(res))
        # 该用户所有的购物车数据(更新后)
        sql_res = "SELECT * from shopping_new where b_id='{}' ".format(username)
        cursor.execute(sql_res)
        res_total = cursor.fetchall()
        print("----------------!!!!!!!!!!!!!!!!!!!!")
        print(res_total)
        print(res)
        if res and len(res_total) != 0:
            msg = "done"
            print(msg)
            print(len(res_total))
            return render_template('myOrder.html', username=username, count=len(res_total), result=res_total,
                                   messages=msg)
        else:
            print("NULL")
            msg = "none"
        return render_template('myOrder.html', username=username, messages=msg)
    else:
        print("NULL")
        msg = "none"
        return render_template('myOrder.html', username=username, messages=msg)

# 商家登录后显示列表
@app.route('/MerchantList')
def MerchantListpage():
    return render_template('MerchantList.html')
# 商家查看评论
@app.route('/MerchantComment', methods=['GET', 'POST'])
def MerchantComment():
    msg = ""
    # 连接数据库，默认数据库用户名root，密码空
    merchant=username
    db = MySQLdb.connect("localhost", "root", "Leepoq126", "appDB", charset='utf8')
    cursor = db.cursor()
    try:
        cursor.execute("use appDB")
    except:
        print("Error: unable to use database!")
    # 查询
    sql = "SELECT * FROM record WHERE m_id = '%s' AND isFinished = 1 AND comment is not null " % merchant
    cursor.execute(sql)
    res = cursor.fetchall()
    # print(res)
    # print(len(res))
    if len(res) != 0:
        msg = "done"
        print(msg)
        print(len(res))
        return render_template('MerchantComment.html', username=username, MERCHANT=merchant, result=res,
                                   messages=msg)
    else:
        print("NULL")
        msg = "none"
    return render_template('MerchantComment.html', username=username, MERCHANT=merchant, messages=msg)
# 商家查看鲜花
@app.route('/MerchantMenu',methods=['GET', 'POST'])
def MerchantMenu():
    msg = ""
    if request.method == 'GET':
        msg = ""
        # 连接数据库，默认数据库用户名root，密码空
        db = MySQLdb.connect("localhost", "root", "Leepoq126", "appDB", charset='utf8')
        cursor = db.cursor()
        try:
            cursor.execute("use appDB")
        except:
            print("Error: unable to use database!")
        # 查询
        sql = "SELECT * FROM flower natural join class WHERE m_id = '%s'" % username
        cursor.execute(sql)
        res = cursor.fetchall()
        # print(res)
        # print(len(res))
        if len(res) != 0:
            msg = "done"
            print(msg)
            print(len(res))
            return render_template('MerchantMenu.html', username=username, result=res, messages=msg)
        else:
            print("NULL")
            msg = "none"
            return render_template('MerchantMenu.html', username=username, messages=msg)
    if request.method == 'POST':
        if request.form["action"] == "删除":
            flowername = request.form.get('flowername')
            merchant = request.form.get('merchant')
            print(merchant)
            db = MySQLdb.connect("localhost", "root", "Leepoq126", "appDB", charset='utf8')
            cursor = db.cursor()
            try:
                cursor.execute("use appDB")
            except:
                print("Error: unable to use database!")
            sql = "DELETE FROM flower where f_id = '{}' and m_id = '{}'".format(flowername,merchant)
            print(sql)
            try:
                cursor.execute(sql)
                db.commit()
                print("鲜花删除成功")
                dmsg = "done"
            except ValueError as e:
                print("--->", e)
                print("鲜花删除失败")
                dmsg = "fail"
            return render_template('MerchantMenu.html', flowername=flowername, merchant=merchant, dmessages=dmsg)
        elif request.form["action"] == "按销量排序":
            db = MySQLdb.connect("localhost", "root", "Leepoq126", "appDB", charset='utf8')
            cursor = db.cursor()
            try:
                cursor.execute("use appDB")
            except:
                print("Error: unable to use database!")

            sql = "SELECT * FROM flower natural join class WHERE m_id = '%s' Order BY saleNumber DESC" % username
            cursor.execute(sql)
            res = cursor.fetchall()
            print(res)
            print(len(res))
            if len(res):
                msg = "done"
                print(msg)
                return render_template('MerchantMenu.html',username=username, result=res, messages=msg)
            else:
                print("NULL")
                msg = "none"
            return render_template('MerchantMenu.html', username=username, messages=msg)
        elif request.form["action"] == "按价格排序":
            db = MySQLdb.connect("localhost", "root", "Leepoq126", "appDB", charset='utf8')
            cursor = db.cursor()
            try:
                cursor.execute("use appDB")
            except:
                print("Error: unable to use database!")

            sql = "SELECT * FROM flower natural join class WHERE m_id = '%s' Order BY price DESC" % username
            cursor.execute(sql)
            res = cursor.fetchall()
            print(res)
            print(len(res))
            if len(res):
                msg = "done"
                print(msg)
                return render_template('MerchantMenu.html', username=username, result=res, messages=msg)
            else:
                print("NULL")
                msg = "none"
            return render_template('MerchantMenu.html', username=username,messages=msg)
# 商家修改鲜花信息
@app.route('/MenuModify', methods=['GET', 'POST'])
def MenuModify():
    msg = ""
    print(request.method)
    # print(request.form["action"])
    if request.form["action"] == "修改信息":
        classname = request.form['classname']  # 传递过去品种名
        flowername = request.form['flowername']  # 传递过去鲜花名
        merchant = request.form['merchant']  # 传递过去商家名
        flowerinfo = request.form['flowerinfo']
        price = request.form.get('price')
        isSpecialty = request.form.get('isSpecialty')
        # imagesrc = request.form['imagesrc']
        print(flowername)
        print(isSpecialty)
        return render_template('MenuModify.html', flowername=flowername, merchant=merchant, flowerinfo=flowerinfo,
                                price=price, username=username, messages=msg,classname=classname, isSpecialty=isSpecialty)
    elif request.form["action"] == "提交修改":
        classname = request.form.get('classname')
        flowername = request.form.get('flowername')
        merchant = request.form.get('merchant')
        flowerinfo = request.form['flowerinfo']
        price = float(request.form.get('price'))
        isSpecialty = int(request.form.get('isSpecialty'))
        f = request.files['imagesrc']
        filename = ''
        if f != '' and allowed_file(f.filename):
            filename = secure_filename(f.filename)
        if filename != '':
            f.save('static/images/' + filename)
        imgsrc = 'static/images/' + filename
        print(isSpecialty)
        print(type(isSpecialty))
        db = MySQLdb.connect("localhost", "root", "Leepoq126", "appDB", charset='utf8')
        cursor = db.cursor()
        try:
            cursor.execute("use appDB")
        except:
            print("Error: unable to use database!")
        if filename == '':
            sql = "Update flower SET classname ='{}', isSpecialty = {}, price = {}  where f_id = '{}' and m_id = '{}'".format(
                classname, isSpecialty, price, flowername, merchant)
        else:
            sql = "Update flower SET classname ='{}', img_res ='{}',isSpecialty = {}, price = {}  where f_id = '{}' and m_id = '{}'".format(
                classname,imgsrc,isSpecialty, price, flowername, merchant)
        print(sql)
        try:
            cursor.execute(sql)
            db.commit()
            print("信息修改成功")
            msg = "done"
        except ValueError as e:
            print("--->", e)
            print("信息修改失败")
            msg = "fail"
        sql="Update class SET intro ='{}' where classname = '{}'".format(flowerinfo,classname)
        try:
            cursor.execute(sql)
            db.commit()
            print("品种信息修改成功")
            msg = "done"
        except ValueError as e:
            print("--->", e)
            print("品种信息修改失败")
            msg = "fail"
        return render_template('MenuModify.html', flowername=flowername, merchant=merchant, username=username, messages=msg)
    return render_template('MenuModify.html', username=username, messages="init")
@app.route('/MenuAdd', methods=['GET', 'POST'])
def MenuAdd():
    msg = ""
    merchant = ""
    print(request.method)
    # print(request.form["action"])
    if request.form["action"] == "增加信息":
        merchant= request.form['merchant']  # 传递过去商家名
        return render_template('MenuAdd.html', messages=msg, merchant=merchant)
    elif request.form["action"] == "确认增加":
        classname = request.form.get('classname')
        flowerinfo = request.form.get('flowerinfo')
        flowername = request.form.get('flowername')
        merchant = request.form.get('merchant')
        price = float(request.form.get('price'))
        isSpecialty = int(request.form.get('isSpecialty'))
        f = request.files['imagesrc']
        print(f)
        if f and allowed_file(f.filename):
            filename = secure_filename(f.filename)
            f.save('static/images/' + filename)
            imgsrc = 'static/images/' + filename
        else:
            imgsrc=""
        db = MySQLdb.connect("localhost", "root", "Leepoq126", "appDB", charset='utf8')
        cursor = db.cursor()
        try:
            cursor.execute("use appDB")
        except:
            print("Error: unable to use database!")
        sql1 = "SELECT * from flower where f_id = '{}' and m_id='{}' ".format(flowername,username)
        cursor.execute(sql1)
        db.commit()
        res1 = cursor.fetchall()
        num = 0
        for row in res1:
            num = num + 1
        # 如果已经存在
        if num == 1:
            print("失败！该鲜花已经添加过！")
            msg = "fail1"
        else:
            sql2 = "insert into flower values ('{}', '{}','{}', {},'{}', {},{}) ".format(flowername, username,
                                                                                               classname, 0, imgsrc,
                                                                                                isSpecialty,price)
            print(sql2)
            try:
                cursor.execute(sql2)
                db.commit()
                print("鲜花添加成功")
                msg = "done"
            except ValueError as e:
                print("--->", e)
                print("鲜花添加失败")
                msg = "fail"
            if msg=="done":#添加成功鲜花 更新品种 若品种不存在则添加 存在则不管,但要给出提示
                sqlc = "SELECT * from class where classname = '{}' ".format(classname)
                cursor.execute(sqlc)
                db.commit()
                res1 = cursor.fetchall()
                num = 0
                for row in res1:
                    num = num + 1
                # 如果已经存在
                if num == 1:
                    print("该品种已经添加过！")
                    msg = "fail2"
                else:
                    sql2 = "insert into class values ('{}', '{}') ".format(classname,flowerinfo)
                    print(sql2)
                    try:
                        cursor.execute(sql2)
                        db.commit()
                        print("品种添加成功")
                        msg = "done"
                    except ValueError as e:
                        print("--->", e)
                        print("品种添加失败")
                        msg = "fail"
    return render_template('MenuAdd.html', messages=msg, merchant=username)
# 商家查看订单
@app.route('/MerchantOrderPage', methods=['GET', 'POST'])
def MerchantOrderPage():
    msg = ""
    global notFinishedNum
    if request.method == 'GET':
        msg = ""
        # 连接数据库，默认数据库用户名root，密码空
        db = MySQLdb.connect("localhost", "root", "Leepoq126", "appDB", charset='utf8')
        cursor = db.cursor()
        try:
            cursor.execute("use appDB")
        except:
            print("Error: unable to use database!")
        # 查询未完成订单数量
        presql = "SELECT * FROM record WHERE m_id = '%s' AND isFinished = 0" % username
        cursor.execute(presql)
        res1 = cursor.fetchall()
        notFinishedNum = len(res1)
        # 查询其他信息
        sql = "SELECT * FROM record WHERE m_id = '%s'" % username
        cursor.execute(sql)
        res = cursor.fetchall()
        # print(res)
        # print(len(res))
        if len(res):
            msg = "done"
            print(msg)
            return render_template('MerchantOrderPage.html', username=username, result=res, messages=msg,
                                   notFinishedNum=notFinishedNum)
        else:
            print("NULL")
            msg = "none"
            return render_template('MerchantOrderPage.html', username=username, messages=msg)
    elif request.form["action"] == "按时间排序":
        db = MySQLdb.connect("localhost", "root", "Leepoq126", "appDB", charset='utf8')
        cursor = db.cursor()
        try:
            cursor.execute("use appDB")
        except:
            print("Error: unable to use database!")
        sql = "SELECT * FROM record WHERE m_id = '%s' Order BY t_time DESC" % username
        cursor.execute(sql)
        res = cursor.fetchall()
        print(res)
        print(len(res))
        if len(res):
            msg = "done"
            print(msg)
            return render_template('MerchantOrderPage.html', username=username, result=res, messages=msg,
                                   notFinishedNum=notFinishedNum)
        else:
            print("NULL")
            msg = "none"
        return render_template('MerchantOrderPage.html', username=username, messages=msg)
    elif request.form["action"] == "按价格排序":
        db = MySQLdb.connect("localhost", "root", "Leepoq126", "appDB", charset='utf8')
        cursor = db.cursor()
        try:
            cursor.execute("use appDB")
        except:
            print("Error: unable to use database!")
        sql = "SELECT * FROM record WHERE m_id = '%s' Order BY price ASC" % username
        cursor.execute(sql)
        res = cursor.fetchall()
        print(res)
        print(len(res))
        if len(res):
            msg = "done"
            print(msg)
            return render_template('MerchantOrderPage.html', username=username, result=res, messages=msg,
                                   notFinishedNum=notFinishedNum)
        else:
            print("NULL")
            msg = "none"
        return render_template('MerchantOrderPage.html', username=username, messages=msg, notFinishedNum=notFinishedNum)
    elif request.form["action"] == "未完成订单":
        db = MySQLdb.connect("localhost", "root", "Leepoq126", "appDB", charset='utf8')
        cursor = db.cursor()
        try:
            cursor.execute("use appDB")
        except:
            print("Error: unable to use database!")
        sql = "SELECT * FROM record WHERE m_id = '%s' AND isFinished = 0 " % username
        cursor.execute(sql)
        res = cursor.fetchall()
        print(res)
        print(len(res))
        if len(res):
            msg = "done"
            print(msg)
            return render_template('MerchantOrderPage.html', username=username, result=res, messages=msg,
                                   notFinishedNum=len(res))
        else:
            print("NULL")
            msg = "none"
        return render_template('MerchantOrderPage.html', username=username, messages=msg, notFinishedNum=notFinishedNum)
    else:
        return render_template('MerchantOrderPage.html', username=username, messages=msg)

# 操作
# 个人中心页面 花店和顾客都导向同一个页面
@app.route('/Personal')
def PersonalPage():
    if userRole == 'MERCHANTS':
        return render_template('MerchantPersonal.html')
    else:
        return render_template('Personal.html')
# 修改个人信息页面  花店和顾客共用此函数
@app.route('/ModifyPersonalInfo', methods=['GET', 'POST'])
def ModifyPersonalInfo():
    msg = ""
    if request.method == 'GET':
        if userRole=="MERCHANTS":
            return render_template('MerchantModifyPerInfo.html', username=username)
        else:
            return render_template('ModifyPersonalInfo.html', username=username)
    if request.method == 'POST':
        # username = request.form['username']
        address = request.form['address']
        phonenum = request.form['phonenum']
        f=""
        imgsrc=""
        if userRole=="MERCHANTS":
            f = request.files['imagesrc']
            filename = ''
            if f != '' and allowed_file(f.filename):
                filename = secure_filename(f.filename)
            if filename != '':
                f.save('static/images/' + filename)
            imgsrc = 'static/images/' + filename
        # 连接数据库，默认数据库用户名root，密码空
        db = MySQLdb.connect("localhost", "root", "Leepoq126", "appDB", charset='utf8')
        cursor = db.cursor()
        try:
            cursor.execute("use appDB")
        except:
            print("Error: unable to use database!")

        if userRole=="MERCHANTS" and filename == '':
            sql = "Update {} SET address = '{}', phone = '{}' where name = '{}'".format(userRole, address, phonenum,username)
        elif userRole=="MERCHANTS":
            sql = "Update {} SET address = '{}', phone = '{}',imageRes = '{}' where name = '{}'".format(userRole,address,phonenum,imgsrc,username)
        else:
            sql = "Update {} SET address = '{}', phone = '{}' where name = '{}'".format(userRole,address,phonenum,username)
        try:
            cursor.execute(sql)
            db.commit()
            print("修改个人信息成功")
            msg = "done"
        except ValueError as e:
            print("--->", e)
            print("修改个人信息失败")
            msg = "fail"
        if userRole == "MERCHANTS":
            return render_template('MerchantModifyPerInfo.html', messages=msg, username=username)
        else:
            return render_template('ModifyPersonalInfo.html', messages=msg, username=username)
# 修改密码页面 花店和顾客共用此函数
@app.route('/ModifyPassword', methods=['GET', 'POST'])
def ModifyPassword():
    msg = ""
    if request.method == 'GET':
        if userRole == 'MERCHANTS':
            return render_template('MerchantModifyPwd.html', username=username)
        else:
            return render_template('ModifyPassword.html', username=username)
    if request.method == 'POST':
        # username = request.form['username']
        psw1 = request.form['psw1']
        psw2 = request.form['psw2']
        # 两次输入密码是否相同
        if psw1 == psw2:
            # 连接数据库，默认数据库用户名root，密码空
            db = MySQLdb.connect("localhost", "root", "Leepoq126", "appDB", charset='utf8')
            cursor = db.cursor()
            try:
                cursor.execute("use appDB")
            except:
                print("Error: unable to use database!")
            sql = "Update {} SET password = '{}' where name = '{}'".format(userRole, psw1, username)
            try:
                cursor.execute(sql)
                db.commit()
                # print("修改密码成功")
                msg = "done"
            except ValueError as e:
                print("--->", e)
                print("修改密码失败")
                msg = "fail"
            if userRole=='MERCHANTS':
                return render_template('MerchantModifyPwd.html', messages=msg, username=username)
            else:
                return render_template('ModifyPassword.html', messages=msg, username=username)
        else:
            msg = "not equal"
            if userRole == 'MERCHANTS':
                return render_template('MerchantModifyPwd.html', messages=msg, username=username)
            else:
                return render_template('ModifyPassword.html', messages=msg, username=username)
# 订单
@app.route('/OrderPage', methods=['GET', 'POST'])
def OrderPage():
    msg = ""
    global notFinishedNum
    if request.method == 'GET':
        msg = ""
        # 连接数据库，默认数据库用户名root，密码空
        db = MySQLdb.connect("localhost", "root", "Leepoq126", "appDB", charset='utf8')
        cursor = db.cursor()
        try:
            cursor.execute("use appDB")
        except:
            print("Error: unable to use database!")
        # 查询未完成订单数量
        presql = "SELECT * FROM record WHERE b_id = '%s' AND isFinished = 0" % username
        cursor.execute(presql)
        res1 = cursor.fetchall()
        notFinishedNum = len(res1)
        # 查询其他信息
        sql = "SELECT * FROM record WHERE b_id = '%s'" % username
        cursor.execute(sql)
        res = cursor.fetchall()
        # print(res)
        # print(len(res))
        if len(res):
            msg = "done"
            print(msg)
            return render_template('OrderPage.html', username=username, result=res, messages=msg,
                                   notFinishedNum=notFinishedNum)
        else:
            print("NULL")
            msg = "none"
            return render_template('OrderPage.html', username=username, messages=msg)
    elif request.form["action"] == "按时间排序":
        db = MySQLdb.connect("localhost", "root", "Leepoq126", "appDB", charset='utf8')
        cursor = db.cursor()
        try:
            cursor.execute("use appDB")
        except:
            print("Error: unable to use database!")

        sql = "SELECT * FROM record WHERE b_id = '%s' Order BY t_time DESC" % username
        cursor.execute(sql)
        res = cursor.fetchall()
        print(res)
        print(len(res))
        if len(res):
            msg = "done"
            print(msg)
            return render_template('OrderPage.html', username=username, result=res, messages=msg,
                                   notFinishedNum=notFinishedNum)
        else:
            print("NULL")
            msg = "none"
        return render_template('OrderPage.html', username=username, messages=msg)
    elif request.form["action"] == "按价格排序":
        db = MySQLdb.connect("localhost", "root", "Leepoq126", "appDB", charset='utf8')
        cursor = db.cursor()
        try:
            cursor.execute("use appDB")
        except:
            print("Error: unable to use database!")

        sql = "SELECT * FROM record WHERE b_id = '%s' Order BY price ASC" % username
        cursor.execute(sql)
        res = cursor.fetchall()
        print(res)
        print(len(res))
        if len(res):
            msg = "done"
            print(msg)
            return render_template('OrderPage.html', username=username, result=res, messages=msg,
                                   notFinishedNum=notFinishedNum)
        else:
            print("NULL")
            msg = "none"
        return render_template('OrderPage.html', username=username, messages=msg, notFinishedNum=notFinishedNum)
    elif request.form["action"] == "未完成订单":
        db = MySQLdb.connect("localhost", "root", "Leepoq126", "appDB", charset='utf8')
        cursor = db.cursor()
        try:
            cursor.execute("use appDB")
        except:
            print("Error: unable to use database!")

        sql = "SELECT * FROM record WHERE b_id = '%s' AND isFinished = 0 " % username
        cursor.execute(sql)
        res = cursor.fetchall()
        print(res)
        print(len(res))
        if len(res):
            msg = "done"
            print(msg)
            return render_template('OrderPage.html', username=username, result=res, messages=msg,
                                   notFinishedNum=len(res))
        else:
            print("NULL")
            msg = "none"
        return render_template('OrderPage.html', username=username, messages=msg, notFinishedNum=notFinishedNum)
    elif request.form["action"] == "确认收货":
        db = MySQLdb.connect("localhost", "root", "Leepoq126", "appDB", charset='utf8')
        cursor = db.cursor()
        try:
            cursor.execute("use appDB")
        except:
            print("Error: unable to use database!")
        print("用户要确认收货啦")
        orderID = request.form['orderID']
        print(orderID)
        now_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")  # 系统时间
        sql1 = "Update record SET isFinished = 1, a_time='{}' WHERE id = '{}' ".format(now_time,orderID)
        print(sql1)
        cursor.execute(sql1)
        db.commit()

        sql2 = "select * from record WHERE id = '%s' " % orderID
        cursor.execute(sql2)
        res1 = cursor.fetchone()
        merchant = res1[1]
        flowername = res1[2]
        print("{} {} 销量+1".format(flowername, merchant))
        sql = "Update flower SET saleNumber = saleNumber+1 WHERE f_id = '{}' AND m_id = '{}'" .format(flowername, merchant)
        print(sql)
        cursor.execute(sql)
        db.commit()
        res = cursor.fetchall()
        print(res)
        msg = "UpdateSucceed"
        return render_template('OrderPage.html', username=username, messages=msg)
    else:
        return render_template('OrderPage.html', username=username, messages=msg)
# 用户评论
@app.route('/MyComments', methods=['GET', 'POST'])
def MyCommentsPage():
    msg = ""
    global notFinishedNum

    if request.method == 'GET':
        msg = ""
        # 连接数据库，默认数据库用户名root，密码空
        db = MySQLdb.connect("localhost", "root", "Leepoq126", "appDB", charset='utf8')
        cursor = db.cursor()
        try:
            cursor.execute("use appDB")
        except:
            print("Error: unable to use database!")
        # 查询未评论订单数量
        presql = "SELECT * FROM record WHERE b_id = '%s' AND isFinished = 1 AND comment is null" % username
        cursor.execute(presql)
        res1 = cursor.fetchall()
        notFinishedNum = len(res1)
        # 查询其他信息
        sql = "SELECT * FROM record WHERE b_id = '%s' AND isFinished = 1 AND comment is not null " % username
        cursor.execute(sql)
        res = cursor.fetchall()
        # print(res)
        # print(len(res))
        if len(res):
            msg = "done"
            print(msg)
            return render_template('MyComments.html', username=username, result=res, messages=msg,
                                   notFinishedNum=notFinishedNum)
        else:
            print("NULL")
            msg = "none"
            return render_template('MyComments.html', username=username, messages=msg)
    elif request.form["action"] == "按时间排序":
        db = MySQLdb.connect("localhost", "root", "Leepoq126", "appDB", charset='utf8')
        cursor = db.cursor()
        try:
            cursor.execute("use appDB")
        except:
            print("Error: unable to use database!")

        sql = "SELECT * FROM record WHERE b_id = '%s' AND isFinished = 1 AND comment is not null Order BY t_time DESC" % username
        cursor.execute(sql)
        res = cursor.fetchall()
        print(res)
        print(len(res))
        if len(res):
            msg = "done"
            print(msg)
            return render_template('MyComments.html', username=username, result=res, messages=msg,
                                   notFinishedNum=notFinishedNum)
        else:
            print("NULL")
            msg = "none"
        return render_template('MyComments.html', username=username, messages=msg)
    elif request.form["action"] == "按价格排序":
        db = MySQLdb.connect("localhost", "root", "Leepoq126", "appDB", charset='utf8')
        cursor = db.cursor()
        try:
            cursor.execute("use appDB")
        except:
            print("Error: unable to use database!")
        sql = "SELECT * FROM record WHERE b_id = '%s' AND isFinished = 1 AND comment is not null Order BY price ASC" % username
        cursor.execute(sql)
        res = cursor.fetchall()
        print(res)
        print(len(res))
        if len(res):
            msg = "done"
            print(msg)
            return render_template('MyComments.html', username=username, result=res, messages=msg,
                                   notFinishedNum=notFinishedNum)
        else:
            print("NULL")
            msg = "none"
        return render_template('MyComments.html', username=username, messages=msg, notFinishedNum=notFinishedNum)
    elif request.form["action"] == "待评价订单":
        # 未评价订单跳转到写评论中
        db = MySQLdb.connect("localhost", "root", "Leepoq126", "appDB", charset='utf8')
        cursor = db.cursor()
        try:
            cursor.execute("use appDB")
        except:
            print("Error: unable to use database!")
        sql = "SELECT * FROM record WHERE b_id = '%s' AND isFinished = 1 AND comment is null" % username
        cursor.execute(sql)
        res = cursor.fetchall()
        print(res)
        print("MyCommentsPage - 未评价订单: {}".format(len(res)))
        print(len(res))
        if len(res):
            msg = "done"
            print(msg)
            return render_template('WriteComments.html', username=username, result=res, messages=msg,
                                   notFinishedNum=len(res))
        else:
            print("MyCommentsPage - 待评价订单 - NULL")
            msg = "none"
            return render_template('WriteComments.html', username=username, messages=msg, notFinishedNum=len(res))
    else:
        return render_template('MyComments.html', username=username, messages=msg)
@app.route('/WriteComments', methods=['GET', 'POST'])
def WriteCommentsPage():
    msg=""
    if request.method == 'GET':
        # 连接数据库，默认数据库用户名root，密码空
        db = MySQLdb.connect("localhost", "root", "Leepoq126", "appDB", charset='utf8')
        cursor = db.cursor()
        try:
            cursor.execute("use appDB")
        except:
            print("Error: unable to use database!")
        # 查询未完成订单数量
        # presql = "SELECT * FROM record WHERE b_id = '%s' AND isFinished = 0" % username
        # cursor.execute(presql)
        # res1 = cursor.fetchall()
        # notFinishedNum = len(res1)
        # 查询其他信息
        sql = "SELECT * FROM record WHERE b_id = '%s' AND isFinished = 1 AND comment is null " % username
        cursor.execute(sql)
        res = cursor.fetchall()
        # print(res)
        # print(len(res))
        if len(res):
            msg = "done"
            print(msg)
            return render_template('WriteComments.html', username=username, result=res, messages=msg)
        else:
            print("WriteCommentsPage - GET - NULL")
            msg = "none"
            return render_template('WriteComments.html', username=username, messages=msg)
    elif request.form["action"] == "按交易时间排序":
        # TODO: 排序之后显示的是空的，不显示的问题没有解决
        db = MySQLdb.connect("localhost", "root", "Leepoq126", "appDB", charset='utf8')
        cursor = db.cursor()
        try:
            cursor.execute("use appDB")
        except:
            print("Error: unable to use database!")
        print(username)
        sql = "SELECT * FROM record WHERE b_id = '%s' AND isFinished = 1 AND comment is null Order BY t_time DESC" % username
        cursor.execute(sql)
        res = cursor.fetchall()
        print(res)
        print(len(res))
        if len(res):
            msg = "done"
            print(msg)
            return render_template('WriteComments.html', username=username, result=res, messages=msg)
        else:
            print("WriteCommentsPage - 按交易时间排序 -NULL")
            msg = "none"
        return render_template('WriteComments.html', username=username, messages=msg)
    elif request.form["action"] == "按价格排序":
        db = MySQLdb.connect("localhost", "root", "Leepoq126", "appDB", charset='utf8')
        cursor = db.cursor()
        try:
            cursor.execute("use appDB")
        except:
            print("Error: unable to use database!")

        sql = "SELECT * FROM record WHERE b_id = '%s' AND isFinished = 1 AND comment is null Order BY price ASC" % username
        cursor.execute(sql)
        res = cursor.fetchall()
        print(res)
        print(len(res))
        if len(res):
            msg = "done"
            print(msg)
            return render_template('WriteComments.html', username=username, result=res, messages=msg,
                                   notFinishedNum=notFinishedNum)
        else:
            print("WriteCommentsPage - 按价格排序 - NULL")
            msg = "none"
        return render_template('WriteComments.html', username=username, messages=msg, notFinishedNum=notFinishedNum)
    elif request.form["action"] == "未完成订单":
        db = MySQLdb.connect("localhost", "root", "Leepoq126", "appDB", charset='utf8')
        cursor = db.cursor()
        try:
            cursor.execute("use appDB")
        except:
            print("Error: unable to use database!")

        sql = "SELECT * FROM record WHERE b_id = '%s' AND isFinished = 0 AND comment is null " % username
        cursor.execute(sql)
        res = cursor.fetchall()
        print(res)
        print(len(res))
        if len(res):
            msg = "done"
            print(msg)
            return render_template('WriteComments.html', username=username, result=res, messages=msg,
                                   notFinishedNum=len(res))
        else:
            print("WriteCommentsPage - 未完成订单 - NULL")
            msg = "none"
        return render_template('WriteComments.html', username=username, messages=msg, notFinishedNum=notFinishedNum)
    else:
        return render_template('WriteComments.html', username=username, messages=msg)
@app.route('/CommentForm', methods=['GET', 'POST'])
def CommentFormPage():
    msg = ""
    print(request.method)
    # print(request.form["action"])
    if request.form["action"] == "写评论":
        orderID = request.form['orderID']
        print(orderID)
        msg = "WriteRequest"
        print(msg)
        return render_template('CommentForm.html', username=username, orderID=orderID, messages=msg)
    elif request.form["action"] == "提交评论":
        print("提交评论!")
        orderID = request.form.get('orderID')
        c_rank = int(request.form.get('rank'))
        text = request.form.get('text')
        db = MySQLdb.connect("localhost", "root", "Leepoq126", "appDB", charset='utf8')
        cursor = db.cursor()
        try:
            cursor.execute("use appDB")
        except:
            print("Error: unable to use database!")
        now_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")  # 系统时间
        if c_rank<0:
            c_rank=0
        elif c_rank>5:
            c_rank=5
        sql = "Update record SET comment = '{}', score = {}, c_time='{}' where id = '{}'".format(text, c_rank,now_time, orderID)
        print(sql)
        try:
            cursor.execute(sql)
            db.commit()
            print("用户评论成功")
            msg = "done"
        except ValueError as e:
            print("--->", e)
            print("用户评论失败")
            msg = "fail"
        return render_template('CommentForm.html', messages = msg, username=username)


if __name__ == '__main__':
    app.run(debug=True)