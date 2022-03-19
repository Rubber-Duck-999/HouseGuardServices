FROM python:3.8

RUN mkdir /project
WORKDIR /project

COPY requirements.txt ./
RUN pip3 install -r requirements.txt

COPY . .
CMD python3 app.py