import signal, sys, ssl, logging, time, os
from cam import Finder

import thread

sys.path.append(os.path.abspath(os.path.curdir + '/vendor/SimpleWebSocketServer'))
from SimpleWebSocketServer import WebSocket, SimpleWebSocketServer, SimpleSSLWebSocketServer

logging.basicConfig(format='%(asctime)s %(message)s', level=logging.DEBUG)

class InputServer(WebSocket):
    def handleMessage(self):
        if self.data is None:
            self.data = ''
        try:
            self.sendMessage(str(self.data))
        except Exception as n:
            print(n)

    def start_finder(self):
        Finder().init(self, False)

    def handleConnected(self):
        print(self.address, 'connected')
        thread.start_new_thread(self.start_finder, ())

    def handleClose(self):
        print(self.address, 'closed')


if __name__ == "__main__":
    def close_sig_handler(signal, frame):
        server.close()
        sys.exit()

    signal.signal(signal.SIGINT, close_sig_handler)
    server = SimpleWebSocketServer('0.0.0.0', 1337, InputServer)
    server.serveforever()



