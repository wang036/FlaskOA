"""
@file: models.py
@author：wang
@time: 2020/8/14 0014 9:06
"""
from oa import db


class Base(db.Model):
    """
    直接在视图中使用以下方法即可
    例如：
    person = Person.query.get(1)
    person.delete()
    """
    __abstract__ = True  # 只能被继承，不能被创建
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)

    # 保存方法
    def save(self):
        db.session.add(self)
        db.session.commit()

    # 删除方法
    def delete(self):
        db.session.delete(self)
        db.session.commit()

    # 修改
    def update(self):
        db.session.commit()


# 职位模型类
class Position(Base):
    __tablename__ = 'position'

    # 实体属性
    name = db.Column(db.String(32), unique=True)  # 职位名称
    level = db.Column(db.Integer)  # 职位等级

    # 关系属性 ---为了查询方便，Flask提供了关系属性，不会在数据中生成相应的字段
    persons = db.relationship('Person', backref='position')
    # 当知道职位查询所有的员工时，通过职位对象.persons就可以获得所有的员工
    # 当员工查询对应的职位时，通过员工对象.position 就可以获得相应的职位

    department_id = db.Column(db.Integer, db.ForeignKey('department.id'))


# 员工模型类
class Person(Base):
    __tablename__ = 'person'  # 指定表的名称

    name = db.Column(db.String(32), nullable=False)  # 用户名
    password = db.Column(db.String(128), nullable=False)  # 密码
    nickname = db.Column(db.String(32), default='靓仔')  # 昵称
    gender = db.Column(db.String(32), default='男')  # 性别
    age = db.Column(db.Integer, default=18)  # 年龄
    jobnum = db.Column(db.String(32), unique=True, nullable=False)  # 工号不能重复，不能为空
    phone = db.Column(db.String(32), default='110')  # 电话
    email = db.Column(db.String(32), default='110@qq.com')  # 邮箱
    photo = db.Column(db.String(64), default='1.jpg')  # 照片
    address = db.Column(db.String(128), default='广州')  # 地址
    score = db.Column(db.Float, default='1.0')  # 绩效
    # 关系属性   职位和员工是一对多关系
    position_id = db.Column(db.Integer, db.ForeignKey('position.id'))  # 表名.id

    # 考勤关联属性
    attendances = db.relationship('Attendance', backref='person')


permission_position = db.Table(
    'permission_position',  # 数据库中表的名称
    db.Column('position.id', db.Integer, db.ForeignKey('position.id')),  # 关联position
    db.Column('permission.id', db.Integer, db.ForeignKey('permission.id'))  # 关联position
)


# 权限模型类
class Permission(Base):
    __tablename__ = 'permission'
    # 实体属性
    name = db.Column(db.String(32))  # 权限名称
    desc = db.Column(db.String(128))  # 权限描述

    # 关系属性
    positions = db.relationship(
        'Position',  # 和模型类进行关联
        backref='permissions',  # 反向查询使用
        secondary=permission_position  # 关联第三张表
    )


# 部门模型类
class Department(Base):
    __tablename__ = 'department'
    # 实体属性
    name = db.Column(db.String(32))  # 部门名称
    description = db.Column(db.String(128))  # 部门描述

    positions = db.relationship('Position', backref='dept')


# 考勤模型类
class Attendance(Base):
    __tablename__ = 'attendance'
    # 实体属性
    reason = db.Column(db.Text)  # 考勤原因
    atype = db.Column(db.String(32))  # 考勤类型
    adate = db.Column(db.Float)  # 考勤天数
    start_time = db.Column(db.Date)  # 开始时间
    end_time = db.Column(db.Date)  # 结束时间
    examine = db.Column(db.String(32), nullable=True, default='审核中')  # 审查员
    astatue = db.Column(db.String(32), default='申请中')  # 申请状态

    # 关系属性
    person_id = db.Column(db.Integer, db.ForeignKey('person.id'))


class News(Base):
    """
    新闻表
    """
    title = db.Column(db.String(32))  # 标题
    author = db.Column(db.String(32))  # 作者
    content = db.Column(db.Text)  # 新闻内容
    public_time = db.Column(db.Date)  # 发布日期
    picture = db.Column(db.String(128), nullable=True)  # 图片
