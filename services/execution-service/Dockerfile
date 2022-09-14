FROM python:3.8-slim-buster

WORKDIR /execution-service
COPY . /execution-service

RUN pip3 install -r requirements.txt 

ENTRYPOINT [ "python" ]

CMD ["execution-service.py" ]