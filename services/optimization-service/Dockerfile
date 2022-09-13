FROM python:3.9-slim
LABEL maintainer = "Martin Beisel <beisel@iaas.uni-stuttgart.de>"

COPY . /
RUN apt-get update && apt-get install -y gcc python3-dev
RUN pip install -r requirements.txt

EXPOSE 5000

ENV FLASK_APP=optimization-service.py
ENV FLASK_ENV=development
ENV FLASK_DEBUG=0

CMD python -m flask run --host=0.0.0.0
