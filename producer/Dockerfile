FROM debian:8 

RUN rm /etc/apt/sources.list

ADD sources.list /etc/apt/

RUN apt-get update && \
    apt-get install -y thrift-compiler python python-pip python-dev && \
    pip install thrift kafka-python && \
    apt-get purge -y python-dev build-essential && \
    apt-get autoremove -y && \
    apt-get autoclean && \
    apt-get clean 

ADD src/ /src/

WORKDIR /src

RUN thrift --gen py sbs_messages.thrift

CMD ./producer.py

# vim: set ts=4 sw=4 expandtab:
