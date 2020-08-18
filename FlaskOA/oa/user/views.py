"""
@file: views.py
@author：wang
@time: 2020/8/14 0014 9:06
"""
import datetime
import os
import time
import hashlib
from oa.user import ubp
from oa.user.models import *
from flask import request, redirect, url_for, jsonify
from flask import render_template
from functools import wraps


# 密码加密
def setPassword(password):
    md5 = hashlib.md5()
    md5.update(password.encode())
    return md5.hexdigest()


# 登录校验装饰器
def login_decorator(func):
    @wraps(func)
    def inner():
        person_name = request.cookies.get('person_name')
        if person_name:
            return func()
        else:
            return redirect('/login/')

    return inner


# 登录页面
@ubp.route('/')
@ubp.route('/login/', methods=['GET', 'POST'])
def login():
    msg = ''
    if request.method == 'POST':
        # 1、获取用户名和密码
        username = request.form.get('username')
        password = request.form.get('password')

        # 2、查询数据库（用户名和密码）
        user = Person.query.filter(Person.name == username, Person.password == setPassword(password)).first()
        # 3、判断
        if user:
            # 正确  重定向到首页
            response = redirect('/index/')
            response.set_cookie('person_name', user.name)
            response.set_cookie('person_password', user.password)
            response.set_cookie('id', str(user.id))
            return response
        msg = '用户名或者密码错误'
    return render_template('login.html', **locals())


@ubp.route('/register/', methods=['GET', 'POST'])
def register():
    msg = ''
    if request.method == "POST":
        # 1、获取表单内容
        name = request.form.get('username')
        password = request.form.get('password')
        jobnum = request.form.get('jobnum')
        peron_obj = Person.query.filter(Person.name == name).first()
        if not peron_obj:
            per_obj = Person()
            per_obj.name = name
            per_obj.password = setPassword(password)
            per_obj.jobnum = jobnum
            per_obj.position_id = 1
            per_obj.save()
            return redirect('/login/')
        msg = '用户名重复'
    return render_template('register.html', **locals())


@ubp.route('/logout/')
@login_decorator
def logout():
    # 1、清除所有cookie
    response = redirect('/login/')
    response.delete_cookie('person_name')
    response.delete_cookie('person_password')
    response.delete_cookie('id')
    # 2、重定向到登录页面
    return response


# 添加员工
@ubp.route('/test/')
def test():
    # 创建部门
    dept_obj = Department()
    dept_obj.name = '研发部'
    dept_obj.description = '这个部门都是大牛'
    dept_obj.save()

    # 创建职位
    pos_obj = Position()
    pos_obj.name = '开发工程师'
    pos_obj.level = 1
    pos_obj.department_id = dept_obj.id
    pos_obj.save()

    # 创建员工
    per_obj = Person()
    per_obj.name = 'zs'
    per_obj.password = '123'
    per_obj.jobnum = 'zs123'
    per_obj.position_id = pos_obj.id
    per_obj.save()

    return 'success'


# 首页
@ubp.route('/index/')
@login_decorator
def index():
    news_list = News.query.all()
    attendance_list = Attendance.query.all()
    return render_template('index.html', **locals())


@ubp.route('/index_ajax/')
@login_decorator
def index_ajax():
    # 1、部门情况
    dept_obj_list = Department.query.all()
    dept_list = []
    for dept_obj in dept_obj_list:
        dept_dic = {}
        dept_name = dept_obj.name  # 部门名称

        dept_num = 0  # 部门下所有的员工
        # 查询职位，从而查询职员
        for pos_obj in dept_obj.positions:
            dept_num += len(pos_obj.persons)  # 查询所有的人员

        dept_dic['dept_name'] = dept_name
        dept_dic['dept_num'] = dept_num
        dept_list.append(dept_dic)
    return jsonify(dept_list)


@ubp.route('/person/')
@login_decorator
def person():
    page = int(request.args.get('page', 1))  # 默认为一页

    per_page = Person.query.paginate(page, 2)  # 每页2条数据
    # print(per_page.pages)  # 获取总共的页码数

    # 判断页码范围
    # 点击前3页时，页码不动
    if page <= 3:
        start = 0
        end = 5
    elif page > per_page.pages - 3:  # 后3页
        start = per_page.pages - 5
        end = per_page.pages
    else:
        start = page - 3
        end = page + 2

    iter_pages = range(1, per_page.pages + 1)[start:end]

    return render_template('person.html', **locals())


# 添加员工
@ubp.route('/add_person/', methods=['GET', 'POST'])
@login_decorator
def add_person():
    if request.method == 'GET':
        # 1、查询所有的职位
        position_obj_list = Position.query.all()
        return render_template('add_person.html', **locals())
    else:
        # POST 方式提交
        # 1、获取表单提交内容
        name = request.form.get('username')
        pwd = request.form.get('password')
        jobnum = request.form.get('jobnum')
        position_id = request.form.get('position_id')
        # 2、保存到数据库
        person = Person()
        person.name = name
        person.password = setPassword(pwd)
        person.jobnum = jobnum
        person.position_id = position_id
        person.save()
        # 3、重定向到员工列表页面
        return redirect('/person/')


# 删除操作
@ubp.route('/delete_person/')
@login_decorator
def delete_person():
    # 1、获取提交过来的id
    person_id = request.args.get('id')
    print(person_id)
    # 2、查询数据库并删除
    per_obj = Person.query.get(person_id)
    per_obj.delete()
    # 3、重定向到员工列表页面
    return redirect('/person/')


# 编辑操作
@ubp.route('/edit_person/', methods=['GET', 'POST'])
@login_decorator
def edit_person():
    if request.method == 'GET':
        # 1、获取id
        id = request.args.get('id')

        # 2、查询数据库
        per_obj = Person.query.get(id)

        # 获取所有的职位
        pos_obj_list = Position.query.all()

        # 3、返回页面
        return render_template('edit_person.html', **locals())
    else:
        # 1、获取修改的对象id
        id = request.form.get('id')  # 需要在前端自己添加一个input标签，设置为hidden
        name = request.form.get('username')
        password = request.form.get('password')
        nickname = request.form.get('nickname')
        jobnum = request.form.get('jobnum')
        gender = request.form.get('gender')
        age = request.form.get('age')
        phone = request.form.get('phone')
        # 获取图片
        photo = request.files.get('photo')
        email = request.form.get('email')
        address = request.form.get('address')
        position_id = request.form.get('position_id')

        # 保存上传文件 获取路径
        photo_file = str(time.time()).split('.')[1] + '_' + photo.filename

        base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir))
        path = os.path.join(base_dir, 'static\\img\\', photo_file)  # 保证文件名的唯一性
        photo.save(path)  # 保存文件

        # 2、查询数据库重新赋值
        per = Person.query.get(id)
        """修改图片使之前的图片删除"""
        if per.photo.startswith('static/'):
            os.remove(os.path.join(base_dir, per.photo))
        per.name = name
        per.password = password
        per.nickname = nickname
        per.jobnum = jobnum
        per.gender = gender
        per.age = age
        # 将图片保存到数据库中
        per.photo = 'static/img/' + photo_file
        per.phone = phone
        per.email = email
        per.address = address
        per.position_id = position_id
        per.update()
        # 3、重定向到person页面
        return redirect('/person/')


# 人物详情
@ubp.route('/detail_person/')
@login_decorator
def detail_person():
    # 1、获取点击id
    id = request.args.get('id')
    # 2、查询职员
    person_obj = Person.query.get(id)
    return render_template('detail_person.html', **locals())


#  职员的模糊查询
@ubp.route('/vague_search/')
@login_decorator
def vague_search():
    name = request.args.get('person_username')
    person_obj = Person.query.filter(Person.name.like(f'{name}%')).all()
    print(person_obj)
    return render_template('search_person.html', **locals())


"""部门管理"""


# 部门展示
@ubp.route('/department/')
@login_decorator
def department():
    department_obj = Department.query.all()
    return render_template('department.html', **locals())


# 编辑部门
@ubp.route('/edit_department/', methods=['GET', 'POST'])
@login_decorator
def edit_department():
    if request.method == "GET":
        id = request.args.get('id')
        department_obj = Department.query.get(id)
        return render_template('edit_department.html', **locals())
    else:
        # 1、获取对象id
        id = request.form.get('id')
        # 2、获取表单内容
        name = request.form.get('name')
        description = request.form.get('description')
        # 3、重新赋值
        depart_obj = Department.query.get(id)
        depart_obj.name = name
        depart_obj.description = description
        depart_obj.update()
        return redirect('/department/')


# 删除部门
@ubp.route('/delete_department/')
@login_decorator
def delete_department():
    # 1、获取id
    id = request.args.get('id')
    # 2、查询数据库并进行删除
    depart_obj = Department.query.get(id)
    # 3、将职位和人都删除
    depart_obj.delete()
    pos_obj = depart_obj.positions
    for pos in pos_obj:
        pos.delete()  # 将部门删除
        person_obj = pos.persons
        for per in person_obj:
            per.delete()  # 将人员删除
            return redirect('/department/')
    return render_template('department.html', **locals())


# 增加部门
@ubp.route('/add_department/', methods=['GET', 'POST'])
@login_decorator
def add_department():
    if request.method == 'GET':
        return render_template('add_department.html')
    else:
        name = request.form.get('name')
        description = request.form.get('description')
        depart = Department()
        depart.name = name
        depart.description = description
        depart.save()
        return redirect('/department/')


# 部门管理查看职位
@ubp.route('/position/', methods=['GET', 'POST'])
@login_decorator
def position():
    if request.method == 'GET':
        id = request.args.get('id')
        department_obj = Department.query.get(id)
        position_list = department_obj.positions
        return render_template('position.html', **locals())
    else:
        id = request.form.get('id')
        name = request.form.get('name')
        level = request.form.get('level')
        position_obj = Position()
        position_obj.name = name
        position_obj.level = level
        position_obj.department_id = id
        position_obj.save()
        return redirect(url_for('ubp.position', id=id))


# 编辑职位
@ubp.route('/edit_position/', methods=['GET', 'POST'])
@login_decorator
def edit_position():
    if request.method == "GET":
        depart_id = request.args.get('id')
        print(depart_id)
    return 'hello'


# 删除职位
@ubp.route('/delete_position/')
@login_decorator
def delete_position():
    id = request.args.get('id')
    position_list = Position.query.get(id)
    depart_id = position_list.dept.id  # 查询到对应的部门id
    position_list.delete()
    return redirect(url_for('ubp.position', id=depart_id))


"""考勤管理"""


# 个人考勤
@ubp.route('/attendance_me/')
@login_decorator
def attendance_me():
    person_id = request.cookies.get('id')
    # 根据id 查询数据库
    kq_obj_list = Attendance.query.filter(Attendance.person_id == person_id).all()
    return render_template('attendance_me.html', **locals())


@ubp.route('/add_attendance_me/', methods=['GET', 'POST'])
@login_decorator
def add_attendance_me():
    # 1、获取表单数据
    reason = request.form.get('reason')
    type = request.form.get('type')
    day = request.form.get('day')
    start_time = request.form.get('start')
    end_time = request.form.get('end')
    person_id = request.cookies.get('id')
    # 保存数据库
    attendance_obj = Attendance()
    attendance_obj.reason = reason
    attendance_obj.atype = type
    attendance_obj.adate = day
    attendance_obj.start_time = datetime.datetime.strptime(start_time, '%Y-%m-%d')
    attendance_obj.end_time = datetime.datetime.strptime(end_time, '%Y-%m-%d')
    attendance_obj.person_id = person_id
    attendance_obj.save()
    return redirect('/attendance_me/')


# 下属考勤
@ubp.route('/attendance_sub/')
@login_decorator
def attendance_sub():
    # 思路，获取当前下属，根据部门和职级
    person_id = request.cookies.get('id')
    person_obj = Person.query.get(person_id)
    pos_obj = person_obj.position  # 职位对象
    level = pos_obj.level  # 职级
    dept_id = pos_obj.department_id  # 部门id
    # 查询出当前部门下比自己低的职位
    position_obj_list = Position.query.filter(Position.department_id == dept_id, Position.level < level).all()

    persons_list = []  # 保存所有的人
    for position_obj in position_obj_list:
        # 遍历出每一个职位
        person_obj_list = position_obj.persons  # 每一个职位对应的所有的人
        persons_list += person_obj_list

    # 查询所有人对应的考勤
    atts_obj_list = []  # 保存所有的考勤
    for person in persons_list:
        att_obj_list = person.attendances
        atts_obj_list += att_obj_list

    return render_template('attendance_subordinate.html', **locals())


# 修改下属考勤属性
@ubp.route('/edit_att_sub/', methods=['GET', "POST"])
@login_decorator
def edit_att_sub():
    # 1、获取传递过来的id
    id = request.args.get('id')
    flag = request.args.get("flag")
    # 2、根据id查询数据库
    att_obj = Attendance.query.get(id)
    att_obj.examine = request.cookies.get('person_name')  # 重新赋值给审核人字段
    # 3、根据判断修改内容
    if flag == 'true':  # 通过
        att_obj.astatue = '通过'
    else:  # 驳回
        att_obj.astatue = '驳回'
    att_obj.update()
    # 4、重定向到下属考勤列表
    return redirect('/attendance_sub/')


"""权限管理"""


# 权限列表
@ubp.route('/permission_list/', methods=['GET', 'POST'])
def permission_list():
    per_obj_list = Permission.query.all()
    return render_template('permission.html', **locals())


# 添加权限功能
@ubp.route('/add_permission/', methods=['GET', 'POST'])
@login_decorator
def add_permission():
    if request.method == 'POST':
        name = request.form.get('name')
        desc = request.form.get('description')
        per_obj = Permission()
        per_obj.name = name
        per_obj.desc = desc
        per_obj.save()
        return redirect('/permission_list/')
    return render_template('add_permission.html')


# 修改权限
@ubp.route('/edit_permission/', methods=['GET', 'POST'])
@login_decorator
def edit_permission():
    if request.method == 'GET':
        id = request.args.get('id')
        per_obj_list = Permission.query.get(id)
    else:
        id = request.form.get('id')
        name = request.form.get('name')
        desc = request.form.get('description')
        per_obj = Permission.query.get(id)
        per_obj.name = name
        per_obj.desc = desc
        per_obj.update()
        return redirect('/permission_list/')
    return render_template('edit_permission.html', **locals())


# 删除权限
@ubp.route('/delete_permission/')
@login_decorator
def delete_permission():
    id = request.args.get('id')
    permission_obj = Permission.query.get(id)
    permission_obj.delete()
    return redirect('/permission_list/')


# 关联职位
@ubp.route('/position_permission/', methods=["GET", "POST"])
@login_decorator
def position_permission():
    if request.method == 'POST':
        # 1、获取表单提交的id列表
        position_ids = request.form.getlist('position_ids')  # 获取选择框的id值
        # print(position_ids)  # ['1', '2']
        permission_id = request.form.get('permission_id')

        # 2、获取权限和职位对象
        per_obj = Permission.query.get(permission_id)

        pos_obj_list = []
        for position_id in position_ids:
            pos_obj = Position.query.get(position_id)
            pos_obj_list.append(pos_obj)
        # 3、设置关系
        per_obj.positions = pos_obj_list
        per_obj.save()
        return redirect('/permission_list/')
    else:
        # 1、获取id
        permission_id = request.args.get('permission_id')
        # 2、查询所有职位
        pos_obj_list = Position.query.all()

        # 3、查询权限对应的职位
        per_obj = Permission.query.get(permission_id)
        # print(per_obj.id)

        # 查询职位
        per_position_obj_list = per_obj.positions  # 职位
        per_positions_ids = []
        for per_position in per_position_obj_list:
            per_positions_ids.append(per_position.id)
    return render_template('position_permission.html', **locals())


# 中间件权限判断
@ubp.add_app_template_global
def permission_control():
    # 前端使用{% if permission_control().权限名 == True %}
    result = {
        'news': False,  # 对新闻权限控制
        'attendance': False,  # 考勤权限
        'person': False,  # 人事管理
        'permission': False  # 权限管理
    }
    # 判断当前用户是否有相关权限，如果有则修改默认值为True
    person_id = request.cookies.get('id')
    person_obj = Person.query.get(person_id)
    pos_obj = person_obj.position  # 职位对象
    permission_obj_list = pos_obj.permissions  # 所有的权限

    for permission_obj in permission_obj_list:
        if permission_obj.name == '新闻管理':
            result['news'] = True
        if permission_obj.name == '人事管理':
            result['person'] = True
        if permission_obj.name == '权限管理':
            result['permission'] = True
    # 下属考勤权限
    person_id = request.cookies.get('id')
    person_obj = Person.query.get(person_id)
    pos_obj = person_obj.position  # 职位对象
    level = pos_obj.level  # 职级
    dept_id = pos_obj.department_id  # 部门id
    # 查询出当前部门下比自己低的职位
    ret = Position.query.filter(Position.department_id == dept_id, Position.level < level).all()
    if ret:
        result['attendance'] = True
    return result


"""新闻"""


# 新闻展示
@ubp.route('/news/')
@login_decorator
def news():
    news_list = News.query.all()
    return render_template('news.html', **locals())


# 新闻添加
@ubp.route('/add_news/', methods=['GET', 'POST'])
@login_decorator
def add_news():
    if request.method == 'POST':
        title = request.form.get('title')
        author = request.form.get('author')
        content = request.form.get('content')
        picture = request.files.get('picture')
        public_time = datetime.datetime.now()
        # 保存上传文件 获取路径
        photo_file = str(time.time()).split('.')[1] + '_' + picture.filename

        base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir))
        path = os.path.join(base_dir, 'static\\img\\', photo_file)  # 保证文件名的唯一性
        picture.save(path)  # 保存文件

        new = News()
        new.title = title
        new.author = author
        new.content = content
        new.picture = 'static\\img\\' + photo_file
        new.public_time = public_time
        new.save()
        return redirect('/news/')
    return render_template('add_news.html')


# 删除新闻
@ubp.route('/delete_news/')
@login_decorator
def delete_news():
    atten_id = request.args.get('id')
    atten_list = News.query.get(atten_id)
    atten_list.delete()
    return redirect('/news/')


@ubp.route('/detail_news/')
@login_decorator
def detail_news():
    atten_id = request.args.get('id')
    atten = News.query.get(atten_id)
    return render_template('detail_news.html', **locals())


@ubp.route('/edit_news/', methods=['GET', "POST"])
@login_decorator
def edit_news():
    if request.method == 'POST':
        id = request.form.get('id')

        title = request.form.get('title')
        author = request.form.get('author')
        content = request.form.get('content')
        picture = request.files.get('picture')
        # 保存上传文件 获取路径
        pic_file = str(time.time()).split('.')[1] + '_' + picture.filename

        base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir))
        path = os.path.join(base_dir, 'static\\img\\', pic_file)  # 保证文件名的唯一性
        picture.save(path)  # 保存文件

        news_obj = News.query.get(id)
        """修改图片使之前的图片删除"""
        if news_obj.picture.startswith('static/'):
            os.remove(os.path.join(base_dir, news_obj.picture))
        news_obj.title = title
        news_obj.author = author
        news_obj.content = content
        news_obj.picture = 'static\\img\\' + pic_file

        news_obj.update()
        return redirect('/news/')
    else:
        id = request.args.get('id')
        new_obj = News.query.get(id)
    return render_template('edit_news.html', **locals())
