FROM python:3.9.9-alpine3.13

ARG GIT_COMMIT

EXPOSE 8080
WORKDIR /usr/src/app

RUN apk add --update --no-cache py3-pip git gcc
RUN pip3 install pipenv

RUN git clone http://github.com/baluttrell/avengers_api.git /usr/src/app
RUN git checkout -f ${GIT_COMMIT}
RUN pipenv run pipenv install

CMD gunicorn -w 16 0.0.0.0:8080 /usr/src/app/wsgi:app
