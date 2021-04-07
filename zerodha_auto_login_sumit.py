import requests
import time

user = 'HK5851'
pswd = 's@nju1502'
twofa = '150210'


funds = "https://api.kite.trade/user/margins"



def kiteLogin():  # automated login
  # print("Logging in...")
  sesh2 = requests.Session()
  url = "https://kite.zerodha.com/api/login"
  twofaUrl = "https://kite.zerodha.com/api/twofa"
  reqId = eval(sesh2.post(url, {"user_id": user, "password": pswd}).text)["data"]["request_id"]
  time.sleep(3)
  login = sesh2.post(twofaUrl, {"user_id": user, "request_id": reqId, "twofa_value": twofa})
  time.sleep(2)
  reqToken = sesh2.get("https://kite.zerodha.com/oms/user/margins")
  s = reqToken.request.headers['Cookie'].split()[2].split(';')[0].replace('=', ' ', 1)
  return s

def hello_world():
      headers = { "X-Kite-Version" : "3",
                  "Authorization" : kiteLogin()}
      js = requests.get(funds, headers=headers).json()
      if (js['status']=='success'):
        r ='Already login'
      else:
        
        headers = {"X-Kite-Version": "3",
                  "Authorization": kiteLogin()}
        js = requests.get(funds, headers=headers).json()
        if (js['status']=='success'):
          r ='Relogin Success'

      return js
print(kiteLogin())
print(hello_world())