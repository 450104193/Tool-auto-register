from bs4 import BeautifulSoup as bs
import requests
import time
import json

URL = 'https://dkhp.hcmue.edu.vn/'
LOGIN_ROUTE = 'Login/'
HEADERS = {'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:79.0) Gecko/20100101 Firefox/79.0',
           'origin': URL, 'referer': URL + LOGIN_ROUTE}

time_refresh_login = 1
file = open("codeclass.txt", "r")
# Mo file cai dat
username = file.readline()
password = file.readline()

s = requests.session()
login_payload = {
    'username': username,
    'password': password,
}
# Thiet lap payload cho dang nhap

number_of_courses_registered_failed = 0
# Hoc phan dang ki that bai
course_registration_failed = []
# List cac hoc phan dang ki that bai
number_of_courses_registered_success = 0
# Hoc phan dang ki thanh cong
course_registration_success = []

while True:
    login_req = s.post(URL + LOGIN_ROUTE, headers=HEADERS, data=login_payload)
    time.sleep(time_refresh_login)
    if login_req.status_code != 200:
        print("Gặp lỗi chưa đăng nhập được", login_req.status_code)
    elif not "Chưa đến thời hạn đăng ký học phần" in login_req.text:
        break
    else:
        print("Chưa đến thời hạn đăng ký học phần", login_req.status_code)
if "không đúng" in login_req.text:
    print("Sai tài khoản, mật khẩu! Vui lòng update lại trong file codeclass.txt")
    exit()
else:
    print("Đăng nhập thành công OK")
cookies = login_req.cookies
# luu cookies dang nhap

code_class = file.readline()
code_class = code_class.split("|")
type_class = file.readline()
type_class = type_class.split("|")

register_payload = {
    'Hide': '',
    'acceptConflict': 'false',
    'classStudyUnitConflictId': '',
    'RegistType': ''
}
# thiet lap payload cho dang ki

for i in range(len(code_class)):
    temp_register_payload = register_payload
    temp_register_payload["Hide"] = code_class[i][0:14] + \
        "$0.0$" + code_class[i][0:12] + "$$0|"
    while True:
        register = s.get(URL + "DangKyHocPhan/DangKy",
                         params=temp_register_payload, timeout=60)
        if register.status_code == 200:
            if "Đăng ký thành công" in register.text or "Lớp học phần này đã đăng ký" in register.text:
                print("Đăng ký thành công học phần " +
                      code_class[i][0:14] + " OK")
                number_of_courses_registered_success += 1
                course_registration_success.append(code_class[i])
                break
            elif "Trùng lịch:" in register.json()['Msg']:
                temp_register_payload['acceptConflict'] = 'true'
                temp_register_payload['classStudyUnitConflictId'] = code_class[i][0:14]
                print("Gặp lỗi đang thử lại!!", register.json()['Msg'])
            elif "đủ số lượng" in register.text:
                print(
                    "Học phần đủ số lượng, chuyển qua đăng kí học phần khác!!")
                number_of_courses_registered_failed += 1
                course_registration_failed.append(code_class[i])
                break
            else:
                print("Gặp lỗi đang thử lại!!", register.json()['Msg'])
        else:
            print("Gặp lỗi đang thử lại", register.status_code)
        time.sleep(1)

print("Đã đăng kí xong OK,", number_of_courses_registered_failed, "học phần đã full,",
      number_of_courses_registered_success, "học phần thành công")
print("Các học phần thất bại:", end=' ')
for i in course_registration_failed:
    print(i[0:14], end=' ')
print("")
print("Các học phần thành công:", end=' ')
for i in course_registration_success:
    print(i[0:14], end=' ')
