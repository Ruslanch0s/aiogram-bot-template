FROM python:3.8

WORKDIR /src
ENV WEBAPP_PORT=3001
COPY . .
RUN pip install -r requirements.txt
CMD python app.py