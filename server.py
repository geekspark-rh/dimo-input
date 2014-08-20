import signal, sys, ssl, logging, time
from cam import Finder

import thread

sys.path.append('./vendor')
from SimpleWebSocketServer import WebSocket, SimpleWebSocketServer, SimpleSSLWebSocketServer

logging.basicConfig(format='%(asctime)s %(message)s', level=logging.DEBUG)

class InputServer(WebSocket):

    def handleMessage(self):
        if self.data is None:
            self.data = ''
        try:
            self.sendMessage(str(self.data))
        except Exception as n:
            print n

    def handleConnected(self):
        print self.address, 'connected'

    def handleClose(self):
        print self.address, 'closed'

def start_finder():
    Finder().init()

if __name__ == "__main__":
    def close_sig_handler(signal, frame):
        server.close()
        sys.exit()

    thread.start_new_thread(start_finder, ())
    signal.signal(signal.SIGINT, close_sig_handler)
    server = SimpleWebSocketServer('localhost', 8000, InputServer)
    server.serveforever()



