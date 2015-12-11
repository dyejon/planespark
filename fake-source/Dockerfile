FROM debian:8

RUN apt-get update && \ 
    apt-get install -y python net-tools && \
    apt-get autoclean && \
    apt-get clean

ADD source.py /

EXPOSE 30003

CMD /source.py
