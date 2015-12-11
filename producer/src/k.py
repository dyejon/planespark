#!/usr/bin/python2

import os
from kafka import KafkaClient, SimpleProducer, KafkaConsumer

import logging
logging.basicConfig(level=logging.DEBUG)
log = logging.getLogger()

server = os.getenv('KAFKA_PORT_9092_TCP', 'tcp://localhost:9092')[6:]

print server
cl = KafkaClient(server)
pr = SimpleProducer(cl)
cn = KafkaConsumer('test', bootstrap_servers=[server], group_id='test')

cl.ensure_topic_exists('test')
for i in xrange(0,100):
	pr.send_messages('test',str(i))
	print 'wrote', i

print 'starting consumer'

for message in cn:
    print "%s:%d:%d: key=%s value=%s" % (
	message.topic, message.partition,
	message.offset, message.key,
	message.value
    )


# vim: set ts=4 sw=4 expandtab:
