FROM python:3.10.7

WORKDIR /usr/src/app
COPY ./requirements.txt ./

RUN apt-get update && apt-get install -y libopencv-dev
RUN pip3 install -r requirements.txt

ENV BASE_DIR_NAME /tmp/tone/

RUN mkdir -p /tmp/tone/raw
RUN mkdir -p /tmp/tone/out
RUN mkdir -p /tmp/tone/tmp

CMD [ "/bin/bash" ]
