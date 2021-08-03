import requests
import re
from datetime import date
from requests.models import Response
import credentials
import datetime
import api_key
import os
import telebot


API_KEY = api_key.api_key
bot = telebot.TeleBot(API_KEY)


@bot.message_handler(commands=["seats"])
def seats(message):
    bot.reply_to(message, "data")


# proxies = {
#     "http": "http://127.0.0.1:8080",
#     "https": "http://127.0.0.1:8080",
# }


def session_check():
    with open("cookie.txt", "r") as f:
        cookie = f.read().strip()
    print("session_check : " + cookie)
    cookies = {"_ticket_simply_session": cookie}
    r = requests.head(
        "http://svjt.svtbus.in/reports",
        cookies=cookies,
    )

    if r.status_code == 200:
        pass
    else:
        svtbus_login()


def svtbus_login():

    r = requests.get("http://svjt.svtbus.in")
    cookie = re.findall(r"_ticket_simply_session=(.*?);", r.headers["Set-Cookie"])[0]
    cookies = {"_ticket_simply_session": cookie}
    csrf_token = re.findall(r'csrf-token" content="(.*?)"', r.text)[0]
    payloads = {
        "authenticity_token": csrf_token,
        "login": credentials.username,
        "password": credentials.password,
        "commit": "Sign In",
    }

    r = requests.post(
        "http://svjt.svtbus.in/account/login",
        cookies=cookies,
        data=payloads,
        # proxies=proxies,
        # verify=False,
    )

    with open("cookie.txt", "w") as f:
        f.write(cookie)
    with open("csrf_token.txt", "w") as f:
        f.write(csrf_token)


@bot.message_handler(commands=["today"])
def today(message):
    session_check()
    today = date.today()
    today = str(today.day) + "/" + str(today.month) + "/" + str(today.year)

    url = (
        "http://svjt.svtbus.in/ibooking/bookings/search_service?rountrip_return=&render_new_dates=false&prev_date_for_cal=&is_from_modify_org_dest_service_ac=&is_pickup_confirm_phone_block=false&old_passanger_data_arr=&old_pnr_for_pickup_phone=&get_all_services=false&searchbus%5Bfrom%5D=-1&searchbus%5Bto%5D=-1&searchbus%5Bdepart%5D="
        + today
        + "&searchbus%5Bcode%5D=-1&searchbus_allocation=0&can_block_or_unblock=true"
    )

    try:
        with open("cookie.txt", "r") as f:
            cookie = f.read().strip()
        print("today : " + cookie)
        cookies = {"_ticket_simply_session": cookie}
        r = requests.get(url, cookies=cookies)
        r_dict = r.json()
        r_data = r_dict["data"]

        response = "\n"
        for line in r_data:

            response += line[0]
            res_info = line[12]
            response += (
                "\nAvailable seats: " + str(res_info["available_seats"]) + "\n\n"
            )

        print(response)
        bot.reply_to(message, response)
    except:
        pass


@bot.message_handler(commands=["tomorrow"])
def tomorrow(message):
    session_check()
    tomorrow = datetime.datetime.today() + datetime.timedelta(days=1)
    tomorrow = tomorrow.date()
    tomorrow = str(tomorrow.day) + "/" + str(tomorrow.month) + "/" + str(tomorrow.year)

    url_tomorrow = (
        "http://svjt.svtbus.in/ibooking/bookings/search_service?rountrip_return=&render_new_dates=false&prev_date_for_cal=&is_from_modify_org_dest_service_ac=&is_pickup_confirm_phone_block=false&old_passanger_data_arr=&old_pnr_for_pickup_phone=&get_all_services=false&searchbus%5Bfrom%5D=-1&searchbus%5Bto%5D=-1&searchbus%5Bdepart%5D="
        + tomorrow
        + "&searchbus%5Bcode%5D=-1&searchbus_allocation=0&can_block_or_unblock=true"
    )
    try:
        with open("cookie.txt", "r") as f:
            cookie = f.read().strip()
        print("today : " + cookie)
        cookies = {"_ticket_simply_session": cookie}
        r = requests.get(url_tomorrow, cookies=cookies)
        r_dict = r.json()
        r_data = r_dict["data"]

        response = "\n"
        for line in r_data:

            response += line[0]
            res_info = line[12]
            response += (
                "\nAvailable seats: " + str(res_info["available_seats"]) + "\n\n"
            )

        print(response)
        bot.reply_to(message, response)
    except:
        pass


bot.polling()
