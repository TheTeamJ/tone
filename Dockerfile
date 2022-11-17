FROM python:3.10.7

WORKDIR /app
COPY . .

RUN apt-get update && apt-get install -y libopencv-dev
RUN pip3 install gunicorn
RUN pip3 install -r requirements.txt

ENV PORT 8080
ENV BASE_DIR_NAME /tmp/tone/

RUN mkdir -p /tmp/tone/raw
RUN mkdir -p /tmp/tone/out
RUN mkdir -p /tmp/tone/tmp

CMD exec gunicorn --bind 0.0.0.0:$PORT --workers 1 --threads 8 --timeout 0 app:app
