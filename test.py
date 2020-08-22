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

error = 0
# Hoc phan dang ki that bai
success = 0
# Hoc phan dang ki thanh cong

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
code_class = code_class.split("|")
type_class = f.readline()
type_class = type_class.split("|")
register_payload = {'Hide': '', 'acceptConflict': 'false',
                    'classStudyUnitConflictId': '', 'RegistType': ''}
for i in range(len(code_class)):
    temp_register_payload = register_payload
    temp_register_payload["Hide"] = code_class[i][0:14] + \
        "$0.0$" + code_class[i][0:12] + "$$0|"
    temp_register_payload["RegistType"] = type_class[i]
    # print(temp_register_payload)
    while True:
        register = s.get(URL + "DangKyHocPhan/DangKy",
                         params=temp_register_payload, timeout=60)
        # print(register.url)
        if register.status_code == 200:
            if "Đăng ký thành công" in register.text:
                print("Đăng ký thành công học phần" +
                      code_class[i][0:14] + " OK")
                success += 1
                break
            elif "Trùng lịch:" in register.json()['Msg']:
                temp_register_payload['acceptConflict'] = 'true'
                temp_register_payload['classStudyUnitConflictId'] = code_class[i][0:14]
                temp_register_payload['RegistType'] = ''
                print("Gặp lỗi đang thử lại!!", register.json()['Msg'])
            elif "đủ số lượng" in register.text:
                print(
                    "Học phần đủ số lượng, chuyển qua đăng kí học phần khác!!")
                error += 1
                break
            else:
                print("Gặp lỗi đang thử lại!!", register.json()['Msg'])
        else:
            print("Gặp lỗi đang thử lại", register.status_code)
        time.sleep(1)

print("Đã đăng kí xong OK,", error, "học phần đã full,",
      success, "học phần thành công")
