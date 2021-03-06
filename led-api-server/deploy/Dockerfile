# Copyright 2013 Thatcher Peskens
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

FROM ubuntu:16.04 as base-stage

# Install required packages and remove the apt packages cache when done.

RUN apt-get update && \
    apt-get upgrade -y && \
    apt-get install -y \
    nginx \
    supervisor \
    python3 \
    python3-dev \
    python3-setuptools \
    python3-pip \
    cron \
    tzdata \
    nano \
    sqlite3 && \
    pip3 install -U pip setuptools && \
    rm -rf /var/lib/apt/lists/*

# set timezone
ENV TZ=Europe/Amsterdam
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone

# COPY requirements.txt and RUN pip install BEFORE adding the rest of your code, this will cause Docker's caching mechanism
# to prevent re-installing (all your) dependencies when you made a change a line or two in your app.

COPY requirements /home/docker/code/



From base-stage as develop-stage
RUN pip3 install -r /home/docker/code/local.txt

# add (the rest of) our code
COPY . /home/docker/code/



FROM base-stage as production-stage
# install uwsgi now because it takes a little while
RUN pip3 install uwsgi

# setup all the configfiles
RUN echo "daemon off;" >> /etc/nginx/nginx.conf
COPY deploy/nginx-app.conf /etc/nginx/sites-available/default
COPY deploy/supervisor-app.conf /etc/supervisor/conf.d/


RUN pip3 install -r /home/docker/code/production.txt

# add (the rest of) our code
COPY . /home/docker/code/

EXPOSE 8888
CMD ["supervisord", "-n"]
