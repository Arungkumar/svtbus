import requests
import os
import re

from requests.sessions import session

import credentials
import token_data

if os.path.exists("token.txt"):
    pass
else:
    pass


proxies = {
    "http": "http://127.0.0.1:8080",
    "https": "http://127.0.0.1:8080",
}


def svtbus_login():

    ss = requests.session()
    r = ss.get("http://svjt.svtbus.in/account/login", proxies=proxies, verify=False)
    authenticity_token = re.findall(r'content="(.*?)"', r.text)
    csrf_token = "authenticity_token = " + '"' + authenticity_token[3] + '"'
    cookie = re.findall(r"_ticket_simply_session=(.*?) ", str(r.cookies))
    cookie = cookie[0]
    cookie_data = "_ticket_simply_session = " + '"' + cookie + '"'
    data = {
        "authenticity_token": authenticity_token[3],
        "login": credentials.username,
        "password": credentials.password,
        "commit": "Sign In",
    }

    r = ss.post(
        "http://svjt.svtbus.in/account/login", data=data, proxies=proxies, verify=False
    )

    session_data = csrf_token + "\n" + cookie_data
    with open("token_data.py", "w") as f:
        f.write(session_data)


ticket_simply_session = token_data._ticket_simply_session
authenticity_token = token_data.authenticity_token

cookies = {"_ticket_simply_session": ticket_simply_session}

r = requests.get(
    "http://svjt.svtbus.in/bookings?show_overlay=true",
    cookies=cookies,
    proxies=proxies,
    verify=False,
)

if "/account/signin" in str(r.content):
    print("Login Please")
    svtbus_login()
else:
    print("keep Going")
