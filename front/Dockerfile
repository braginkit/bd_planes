FROM alpine:3.16
RUN apk --update add bash nano
RUN apk add --no-cache bash coreutils grep sed
FROM tiangolo/uwsgi-nginx:python3.8
ENV STATIC_URL /static
ENV STATIC_PATH /home/Nik/app/app/static
COPY ./requirements.txt /home/Nik/app/requirements.txt
RUN pip3 install -r /home/Nik/app/requirements.txt



