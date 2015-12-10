#!/usr/bin/env python2

import sys, glob
sys.path.append('gen-py')
# sys.path.insert(0, glob.glob('../../lib/py/build/lib*')[0])

from sbs_messages.ttypes import *

from thrift import Thrift
from thrift.protocol import TBinaryProtocol
from thrift.transport import TTransport

outTransport = TTransport.TMemoryBuffer()
outProtocol = TBinaryProtocol.TBinaryProtocol(outTransport)

s = SelectionChange()

s.session_id = 1
s.aircraft_id = 2
s.hex_ident = "0xf"
s.flight_id = 3
s.generated_timestamp = '2015-12-09T01:01:02.125'
s.logged_timestamp = '2015-12-09T01:01:02.125'
s.callsign = 'TW124'

outProtocol.write(s)

import IPython; IPython.embed()
