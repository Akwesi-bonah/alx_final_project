# from base64 import b64encode, b64decode
#
# import bcrypt
#
# from models import storage
# from models.staff import Staff
#
import base64

import bcrypt
from sqlalchemy import Date

from api.v1.auth.basic_auth import BasicAuth
from models import storage
from models.staff import Staff
from models.student import Student

username = "arhin"
password = "pwd"
#
# data = f"{username}:{password}"
# data = b64encode(data.encode('utf-8'))
#
# # # new_instance = Staff(first_name="Arhin", last_name="Kweku", email="test1@gmail.com", phone="02431234567", password=password, role="admin", status="active")
# # # new_instance.save()
# # user = storage.find_by(Staff, email="test1@gmail.com")
# # print(user)
# # print(user.is_valid_password(password))
# # print(bcrypt.checkpw(password.encode(), user.password.encode()))
# # # print(user)

""" Retreive this user via the class BasicAuth """

a = BasicAuth()

staff = Staff()
student = Student()
user_email = "user@gmail.com"
clear_user_pwd = "pwd"

staff.campus = "North"
staff.name = "Arhin"
staff.email = user_email
staff.phone = "0243124567"
staff.password = clear_user_pwd
staff.role = "admin"
staff.status = "active"
staff.save()

student.first_name = "Arhin"
student.last_name = "Kweku"
student.email = user_email
student.phone = "02431234567"
student.password = clear_user_pwd
student.date_of_birth = "1990-01-01"
student.gender = "male"
student.student_number = "12345678"
student.address = "Top town 123"
student.disability = "No"
student.level = "200"
student.save()

