FROM python:3.10.5-alpine3.15
COPY . /app
WORKDIR /app
RUN pip install -r requirements.txt
ENV FLASK_APP=app.py
CMD flask run -h 0.0.0.0 -p 5000