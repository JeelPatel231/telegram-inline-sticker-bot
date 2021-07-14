FROM redis:latest

RUN apt update && apt install -y python3 python3-pip git
RUN git clone https://github.com/JeelPatel231/telegram-inline-sticker-bot /root/bot
WORKDIR /root/bot

RUN pip3 install -r requirements.txt
