#!/usr/bin/env python2

import os
import sys
import glob
import time
import socket

sys.path.append('gen-py')
# sys.path.insert(0, glob.glob('../../lib/py/build/lib*')[0])

from sbs_messages.ttypes import *

from thrift import Thrift
from thrift.protocol import TBinaryProtocol
from thrift.transport import TTransport

from kafka import KafkaClient, SimpleProducer, KafkaConsumer

import logging
logging.basicConfig(level=logging.DEBUG)
log = logging.getLogger('planespark.producer')

# docker link ENVVARs

kafka_server = os.getenv('KAFKA_PORT_9092_TCP', 'tcp://localhost:9092')[6:]
sbs_server = os.getenv('SOURCE_PORT_30003_TCP', 'tcp://localhost:30003')[6:]

sbs_connect_retry_wait = 5
kafka_connect_retry_wait = 5

def sbs_generator():
    while True:
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            host, port = sbs_server.split(':' , 1)
            port = int(port)
            log.info('connecting to sbs server %s:%d' % (host, port))
            s.connect((host, port))
            log.info('connected')
            f = s.makefile()
            while True:
                rec = f.readline()
                log.info('got 1 record')
                yield rec.strip()
        except:
            log.exception('lost connection- will retry in %d seconds' % sbs_connect_retry_wait)
            time.sleep(sbs_connect_retry_wait)

def message_discriminator(cols):
    if cols[0] == 'SEL':
        s = SelectionChange()
        s.session_id = int(cols[2])
        s.aircraft_id = int(cols[3])
        s.hex_ident = cols[4]
        s.flight_id = int(cols[5])
        s.generated_timestamp = '%sT%s' % (cols[6].replace('/','-'), cols[7])
        s.logged_timestamp = '%sT%s' % (cols[8].replace('/','-'), cols[9])
        s.callsign = cols[10]
        s.write(protocol)
        return s

def serializer(callback):
    tbuffer = TTransport.TMemoryBuffer()
    protocol = TBinaryProtocol.TBinaryProtocol(tbuffer)

    while True:
        try:
            rec = yield
            cols = rec.split(',')
                callback(tbuffer.getvalue())
        except:
            log.exception('failure serializing record "%s"' % rec)
        finally:
            tbuffer._buffer.reset()
            tbuffer._buffer.truncate()
            assert len(tbuffer.getvalue()) == 0, str(dir(tbuffer))
        
def kafka_sender():
    while True:
        try:
            log.info('connecting to kafka server at %s' % kafka_server)
            cl = KafkaClient(kafka_server)
            pr = SimpleProducer(cl)
            cn = KafkaConsumer('planedata', bootstrap_servers=[kafka_server], group_id='planedata')
            cl.ensure_topic_exists('planedata')

            while True:
                msg = yield
                log.debug('committed 1 msg (%db) to kafka' % len(msg))
                pr.send_messages('planedata', msg)   
        except:
            log.exception('failed to send kafka message - will retry in %d seconds' % kafka_connect_retry_wait)
            time.sleep(kafka_connect_retry_wait)

sender = kafka_sender()
ser = serializer(lambda m: sender.send(m))

sender.send(None)
ser.send(None)

for rec in sbs_generator():
    ser.send(rec)


# vim: set ts=4 sw=4 expandtab:
