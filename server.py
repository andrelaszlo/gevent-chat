import logging
from gevent.server import DatagramServer


class ChatServer(DatagramServer):

    def __init__(self, *args):
        self.clients = set()
        super(ChatServer, self).__init__(*args)

    def handle(self, data, address):
        logging.debug('%s: received %r' % (address[0], data))

        if address not in self.clients:
            self.clients.add(address)

        if data == 'HELO':
            # Handshake
            self.socket.sendto('OHAI\x00', address)
            return

        self.broadcast(address, data)

    def broadcast(self, origin, message):
        for address in self.clients:
            if address == origin:
                continue
            logging.debug("sending %r to %r" % (message, address))
            self.socket.sendto(message, address)

if __name__ == '__main__':
    logging.getLogger().setLevel(logging.DEBUG)
    logging.info("Chat server starting")
    ChatServer(':9000').serve_forever()
