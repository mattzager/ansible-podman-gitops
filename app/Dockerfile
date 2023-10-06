FROM python:3.6-alpine

RUN pip install flask

COPY . /opt/

EXPOSE 8080
EXPOSE 8081

WORKDIR /opt

ENTRYPOINT ["python", "app.py"]