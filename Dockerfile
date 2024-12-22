FROM python:3.12

WORKDIR /hw6

COPY . /hw6

EXPOSE 65432

CMD ["python", "tcp_chat.py", "server"]
