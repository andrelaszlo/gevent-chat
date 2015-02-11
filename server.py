import logging
from gevent.server import DatagramServer


class ChatServer(DatagramServer):

    def __init__(self, *args):
        self.clients = []
        super(ChatServer, self).__init__(*args)

    def handle(self, data, address):
        logging.debug('%s: received %r' % (address[0], data))
        self.socket.sendto(data.upper(), address)

if __name__ == '__main__':
    logging.getLogger().setLevel(logging.DEBUG)
    logging.info("Chat server starting")
    ChatServer(':9000').serve_forever()
