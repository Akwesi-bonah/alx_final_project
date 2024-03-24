# from base64 import b64encode, b64decode
#
# import bcrypt
#
# from models import storage
# from models.staff import Staff
#
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
# staff.first_name = "Arhin"
# staff.last_name = "Kweku"
# staff.email = user_email
# staff.phone = "0243124567"
# staff.password = clear_user_pwd
# staff.role = "admin"
# staff.status = "active"
# staff.save()
# #
# student.first_name = "Arhin"
# student.last_name = "Kweku"
# student.email = "testing@gmail.com"
# student.phone = "02431234567"
# student.password = "pwd"
# student.date_of_birth = "1990-01-01"
# student.gender = "male"
# student.save()
#
# u = a.staff_object_from_credentials(None, None)
# print(u.display_name() if u is not None else "None")
#
# u = a.student_object_from_credentials(89, 98)
# print(u.display_name() if u is not None else "None")
#
# u = a.staff_object_from_credentials("email@notfound.com", "pwd")
# print(u.display_name() if u is not None else "None")
#
# u = a.student_object_from_credentials(user_email, "pwd")
# print(u.display_name() if u is not None else "None")


user_data = storage.find_by(Staff, email=user_email)
if not bcrypt.checkpw(clear_user_pwd.encode(), user_data.password.encode()):
    print("Invalid credentials")
else:
    print("Valid credentials")