FROM ubuntu:16.04


RUN apt-get update -y && \
    apt-get install -y python3-pip python-dev
RUN apt-get install -y locales locales-all
ENV LC_ALL en_US.UTF-8
ENV LANG en_US.UTF-8
ENV LANGUAGE en_US.UTF-8
# We copy just the requirements.txt first to leverage Docker cache
COPY ./requirements.txt /src/requirements.txt

WORKDIR /src

RUN pip3 install -r requirements.txt

COPY . /src

#ENTRYPOINT [ "python" ]

CMD [ "flasky.py" ]