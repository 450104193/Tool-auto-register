from bs4 import BeautifulSoup as bs
import requests
import time
import json

URL = 'https://dkhp.hcmue.edu.vn/'
LOGIN_ROUTE = 'Login/'
HEADERS = {'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:79.0) Gecko/20100101 Firefox/79.0',
           'origin': URL, 'referer': URL + LOGIN_ROUTE}

time_refresh_login = 1
f = open("codeclass.txt", "r")
username = f.readline()
password = f.readline()

s = requests.session()
login_payload = {
    'username': username,
    'password': password,
}

while True:
    login_req = s.post(URL + LOGIN_ROUTE, headers=HEADERS, data=login_payload)
    time.sleep(time_refresh_login)
    if login_req.status_code != 200:
        print("Gặp lỗi chưa đăng nhập được", login_req.status_code)
    elif not "Chưa đến thời hạn đăng ký học phần" in login_req.text:
        break
    else:
        print("Chưa đến thời hạn đăng ký học phần", login_req.status_code)
print("Đăng nhập thành công OK")
cookies = login_req.cookies

code_class = f.readline()
code_class = code_class[0:12] + "$0.0$" + code_class[0:14] + "$$0|"
type_class = f.readline()
register_payload = {'Hide': code_class, 'acceptConflict': 'false',
                    'classStudyUnitConflictId': '', 'RegistType': type_class}
while True:
    register = s.get(URL + "DangKyHocPhan/DangKy",
                     params=register_payload, timeout=60)
    if register.status_code == 200:
        if "Đăng ký thành công" in register.text:
            print(register.json()["Msg"] + code_class + "OK")
            break
        else:
            print("Gặp lỗi đang thử lại", register.status_code)
    else:
        print("Gặp lỗi đang thử lại", register.status_code)
    time.sleep(1)

#print("Đã đăng kí xong OK")
