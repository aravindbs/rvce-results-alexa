FROM python:2.7.12

COPY requirements.txt /
RUN pip install -r ./requirements.txt

COPY . /Web/

WORKDIR /Web

EXPOSE 8000
ENV FLASK_APP=app.py
CMD flask run -h 0.0.0.0 -p $PORT