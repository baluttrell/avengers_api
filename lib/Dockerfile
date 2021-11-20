FROM ubuntu:latest

ARG GIT_COMMIT
ENV LC_ALL C.UTF-8
ENV LANG C.UTF-8

EXPOSE 8080
WORKDIR /usr/src/app

RUN apt-get update
RUN apt-get install -y git apt-utils debconf-utils gcc build-essential
RUN apt-get install -y python3-pip python3-dev python3-setuptools --no-install-recommends
RUN apt-get install -y locales

RUN echo "en_US.UTF-8 UTF-8" > /etc/local.gen
RUN locale-gen

RUN pip3 install --upgrade pip
RUN pip3 install pipenv

RUN git clone https://github.com/baluttrell/avengers_api.git /usr/src/app
RUN git checkout -f ${GIT_COMMIT}
RUN pipenv --python /usr/bin/python3 run pipenv install --system

CMD pipenv run gunicorn -w 16 0.0.0.0:8080 /usr/src/app/wsgi:app
