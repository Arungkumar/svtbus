FROM python

WORKDIR /app

COPY . /app

RUN pip install requests fire pyTelegramBotAPI

CMD ["python", "master.py"]
