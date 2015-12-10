FROM debian:8

RUN apt-get update && \ 
    apt-get install -y netcat && \
    apt-get autoclean && \
    apt-get clean

ADD start.sh /

CMD /start.sh
