#@+leo-ver=4-thin
#@+node:ville.20091010232339.6117:@thin ../external/lproto.py
#@@language python

#@<< docstring >>
#@+node:ville.20091010205847.1364:<< docstring >>
""" lproto - simple local socket protocol dispatcher (reactor) for PyQt 

Author: Ville M. Vainio <vivainio@gmail.com>

"""
#@nonl
#@-node:ville.20091010205847.1364:<< docstring >>
#@nl

#@<< imports >>
#@+node:ville.20091009234538.1373:<< imports >>
# todo move out qt dep
from PyQt4 import QtCore, QtNetwork
import struct
#@nonl
#@-node:ville.20091009234538.1373:<< imports >>
#@nl

#@+others
#@+node:ville.20091010205847.1363:sending
def mk_send_bytes(msg):
    lendesc = struct.pack('I', len(msg))
    return lendesc + msg

#@-node:ville.20091010205847.1363:sending
#@+node:ville.20091010205847.1362:class LProtoBuf
class LProtoBuf:
    def __init__(self):

        self.plen = -1
        self.buf = ""

    def set_recv_cb(self, cb):
        """ set func to call with received messages """
        self.recv_cb = cb
    def get_rlen(self):
        # read pkg length
        if self.plen == -1:
            return 4
        return self.plen - len(self.buf)

    def push_bytes(self, allbytes):
        while allbytes:
            rlen = self.get_rlen()
            byts = allbytes[0:rlen]
            self.push_bytes_one(byts)
            allbytes = allbytes[rlen:]

    def push_bytes_one(self, byts):
        if self.plen == -1:
            lendesc = byts[0:4]
            intlen = struct.unpack('I', lendesc)[0]
            print "have", intlen, "bytes"
            self.plen = intlen
            self.buf = byts[4:]
        else:
            self.buf = self.buf + byts

        if len(self.buf) == self.plen:
            print "dispatch msg", self.buf
            self.recv_cb(self.buf)
            self.buf = ""
            self.plen = -1
            return

        print "in buf",self.buf
#@-node:ville.20091010205847.1362:class LProtoBuf
#@+node:ville.20091009234538.1374:class LProtoServer
class LProtoServer:
    #@    @+others
    #@+node:ville.20091009234538.1380:initialization
    def __init__(self):
        self.srv = QtNetwork.QLocalServer()
        self.srv.connect(self.srv, QtCore.SIGNAL("newConnection()"),
            self.connected)

        self.ses = {}  

    def listen(self, name):
        self.srv.listen(name)
        print "listen on",self.srv.fullServerName()

    def msg_received(self, msg, ses):
        print "message", msg, "to ses", ses


    def connected(self):
        print "hnd con"
        lsock = self.srv.nextPendingConnection()
        print "conn", lsock
        buf =  LProtoBuf()

        self.ses[lsock] = ses_ent = {'_sock' : lsock, '_buf' : buf }

        def msg_recv_cb(msg):
            self.msg_received(msg, ses_ent)

        buf.set_recv_cb( msg_recv_cb )


        def readyread_cb():
            print "read ready"        
            allbytes = lsock.readAll()
            buf = ses_ent['_buf']
            buf.push_bytes(allbytes)


        lsock.connect(lsock, QtCore.SIGNAL('readyRead()'), readyread_cb)
        #self.connect(self.qsock, SIGNAL('connectionClosed()'), self.handleClosed)


    def readyread(self):
        pass

    #@-node:ville.20091009234538.1380:initialization
    #@-others
#@-node:ville.20091009234538.1374:class LProtoServer
#@+node:ville.20091010205847.1360:class LProtoClient
class LProtoClient:
    #@    @+others
    #@+node:ville.20091010205847.1361:initialization
    def __init__(self):
        self.cl = QtNetwork.QLocalSocket()

    def connect(self, name):
        self.cl.connectToServer(name)
        print "client connected"
        pass
    #@-node:ville.20091010205847.1361:initialization
    #@-others
#@-node:ville.20091010205847.1360:class LProtoClient
#@-others
#@nonl
#@-node:ville.20091010232339.6117:@thin ../external/lproto.py
#@-leo
