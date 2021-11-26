FROM ubuntu:latest

ARG GIT_COMMIT
ENV LC_ALL C.UTF-8
ENV LANG C.UTF-8

EXPOSE 8080
WORKDIR /usr/src/app

RUN apt-get update && apt-get install -y git apt-utils debconf-utils gcc build-essential
RUN apt-get update && apt-get install -y python3-pip python3-dev python3-setuptools python-setuptools python3-pkg-resources --no-install-recommends
RUN apt-get update && apt-get install -y locales && echo "en_US.UTF-8 UTF-8" > /etc/local.gen && locale-gen

RUN pip3 install --upgrade pip && pip3 install pipenv && pip install setuptools
RUN apt-get install --reinstall python-pkg-resources

RUN git clone https://github.com/baluttrell/avengers_api.git /usr/src/app && git checkout -f ${GIT_COMMIT}
RUN pipenv --python /usr/bin/python3 run pipenv install
