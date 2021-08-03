import datetime

tomorrow = datetime.datetime.today() + datetime.timedelta(days=1)
tomorrow = tomorrow.date()
tomorrow = str(tomorrow.day) + "/" + str(tomorrow.month) + "/" + str(tomorrow.year)
print(tomorrow)


# today = str(today.day) + "/" + str(today.month) + "/" + str(today.year)
