from sqlalchemy import create_engine
from datetime import datetime,timedelta
engine = create_engine('sqlite:///database.db?check_same_thread=False', echo=True)
connection = engine.connect()
from sqlalchemy import Table, Column, Integer, String, MetaData, ForeignKey,insert,update,delete,select,and_,DateTime
metadata = MetaData()
students = Table('students',metadata,
            Column('id',String,primary_key=True),
            Column('name',String),
            Column('student_class',String),
            Column('phone_number',String))

violation = Table('violation',metadata,
            Column('id',String),
            Column('name',String),
            Column('student_class',String),
            Column('phone_number',String),
            Column('time_of_violation',DateTime,default=datetime.now()),
            Column("path_img",String))
            
account = Table('account',metadata,
            Column('username',String, primary_key=True),
            Column('password',String,))


def get_account(username, password):
    get_account = select([account]).where(account.columns.username == username,account.columns.password == password)
    query = connection.execute(get_account)
    account_id = query.fetchall()
    query.close()
    if len(account_id) > 0 :
        return True 

def get_last_time_violation(id,number_violation):
    check = select([violation]).where(violation.columns.id == id)
    query = connection.execute(check)
    last_time = query.fetchall()[number_violation-1].time_of_violation
    return last_time


def get_number_of_violation(id):
    check = select([violation]).where(violation.columns.id == id)
    query = connection.execute(check)
    number_of_violation = len(query.fetchall())
    query.close()
    return number_of_violation

def del_all_violation():
    del_all = delete(violation)
    query = connection.execute(del_all)
    query.close()
def check_true_violation(id,name_img):
    check = select([violation]).where(violation.columns.time_of_violation >= datetime.now()-timedelta(days=0,minutes=3))
    query = connection.execute(check)
    list_violation_two_min = query.fetchall()
    query.close()
    if len(list_violation_two_min) == 0:
        add_violator(id,name_img)
        return True
    list_id = []
    for students in list_violation_two_min:
        list_id.append(students[0])
    print(list_id)
    if str(id) in list_id:
        return False
    add_violator(id, name_img)
    return True
def get_violator_list():
    get_all_violator = select([violation])
    query = connection.execute(get_all_violator)
    list_violation = query.fetchall()
    query.close()
    return list_violation
def add_violator(id,name_img):
    get_one = select([students]).where(students.columns.id == id)
    query = connection.execute(get_one)
    students_array = query.fetchall()
    query.close()
    if len(students_array) == 0:
        return False
    student = students_array[0]
    name_img = "violator_images/"+name_img
    add = insert(violation).values(id=id,name=student[1],student_class=student[2],phone_number=student[3],path_img = name_img)
    query = connection.execute(add)
    query.close()
    return True


def get_one_student(id):
    get_one = select([students]).where(students.columns.id==id)
    query = connection.execute(get_one)
    student = query.fetchall()
    if len(student) == 0:
        return False
    return student[0]
def del_all_students():
    del_all = delete(students)
    query = connection.execute(del_all)
    query.close()

def get_student():
    get_student = select([students])
    query = connection.execute(get_student)
    student = query.fetchall()
    query.close()
    return student
def check_student(id):
    check_student = select([students]).where(students.columns.id==id)
    query = connection.execute(check_student)
    student_available = query.fetchall()
    query.close()
    if len(student_available) == 0:
        return False
    return True

def add_student(id,name,student_class,phone_number):
    if check_student(id) == True:
        return False
    new_student = insert(students).values(id=id,name=name,student_class=student_class,phone_number=phone_number)
    query = connection.execute(new_student)
    query.close()
    return True

def del_student(id):
    search_student = delete(students).where(students.columns.id ==id)
    query = connection.execute(search_student)
    query.close()
    
def update_student(id,name="",student_class="",phone_number=""):
    if name == "":
        if student_class == "" and phone_number == "":
            return False
        elif student_class == "" and phone_number != "":
            update_student = update(students).values(phone_number=phone_number).where(students.columns.id==id)
            query = connection.execute(update_student)
            query.close()
            return True
        elif student_class != "" and phone_number == "":
            update_student = update(students).values(student_class=student_class).where(students.columns.id == id)
            query = connection.execute(update_student)
            query.close()
            return True
        else:
            update_student = update(students).values(student_class=student_class,phone_number=phone_number).where(students.columns.id == id)
            query = connection.execute(update_student)
            query.close()
            return True
    else:
        if student_class == "" and phone_number == "":
            update_student = update(students).values(name=name).where(students.columns.id == id)
            query = connection.execute(update_student)
            query.close()
            return True
        elif student_class == "" and phone_number != "":
            update_student = update(students).values(phone_number=phone_number,name=name).where(students.columns.id == id)
            query = connection.execute(update_student)
            query.close()
        elif student_class != "" and phone_number == "":
            update_student = update(students).values(student_class=student_class,name=name).where(students.columns.id == id)
            query = connection.execute(update_student)
            query.close()
            return True
        else:
            update_student = update(students).values(student_class=student_class, phone_number=phone_number,name=name).where(students.columns.id == id)
            query = connection.execute(update_student)
            query.close()
            return True

