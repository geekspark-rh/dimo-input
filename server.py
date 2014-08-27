import signal, sys, ssl, logging, time, os
from input import Finder

import thread
import getopt

sys.path.append(os.path.abspath(os.path.curdir + '/vendor/SimpleWebSocketServer'))
from SimpleWebSocketServer import WebSocket, SimpleWebSocketServer, SimpleSSLWebSocketServer

logging.basicConfig(format='%(asctime)s %(message)s', level=logging.DEBUG)

cam=1
debug=False

class InputServer(WebSocket):
    def handleMessage(self):
        if self.data is None:
            self.data = ''
        try:
            self.sendMessage(str(self.data))
        except Exception as n:
            print(n)

    def start_finder(self):
        opts = {
            'camera' : cam,
            'debug'  : debug
        }
        Finder().init(self, opts)

    def handleConnected(self):
        print(self.address, 'connected')
        thread.start_new_thread(self.start_finder, ())

    def handleClose(self):
        print(self.address, 'closed')

if __name__ == "__main__":
    def close_sig_handler(signal, frame):
        server.close()
        sys.exit()


    opts, args = getopt.getopt(sys.argv[1:], 'c:')
    for o, a in opts:
        if o == 'c':
            cam=0
        elif o == 'd':
            debug=True

    signal.signal(signal.SIGINT, close_sig_handler)
    server = SimpleWebSocketServer('0.0.0.0', 1337, InputServer)
    server.serveforever()

