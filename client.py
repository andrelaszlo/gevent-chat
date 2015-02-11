import gevent
import gevent.socket
import socket
import sys
from datetime import datetime
from urwid_geventloop import GeventLoop
from urwid import (ListBox, SimpleFocusListWalker, Frame, MainLoop, Edit, Text,
                   ExitMainLoop)

class ChatMessages(ListBox):
    """ Show the last couple of chat messages as a scrolling list """

    def __init__(self, chat):
        self.chat = chat
        self.walker = SimpleFocusListWalker([])
        super(ChatMessages, self).__init__(self.walker)

    def add(self, message):
        self.walker.append(Text(message))
        self.set_focus(len(self.walker)-1)


class ChatInput(Edit):
    """ Where the user types a message or commands """

    def __init__(self, chat):
        self.chat = chat
        super(ChatInput, self).__init__(caption='> ')

    def keypress(self, size, key):
        message = self.get_edit_text()

        if key == 'enter':
            if message == '':
                return
            if message[0] == '/':
                self.chat.user_command(message[1:])
            else:
                self.chat.write_message(self.chat.nickname, message)
                self.chat.send_message(message)
            self.set_edit_text('')

        super(ChatInput, self).keypress(size, key)


class Connection(object):

    HANDSHAKE_INIT = 'HELO'
    HANDSHAKE_RESPONSE = 'OHAI'

    STATE_CONNECTING = 0
    STATE_CONNECTED = 1
    STATE_DISCONNECTED = 2

    RECORD_SEPARATOR = '\x1e'

    SERVER = 'localhost'
    PORT = 9000

    def __init__(self, chat):
        self.state = self.STATE_CONNECTING
        self.chat = chat
        self.socket = gevent.socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    def handle(self, message):
        if message[0] == self.HANDSHAKE_RESPONSE:
            self.state = self.STATE_CONNECTED
            self.chat.connected()
        elif message[0] == 'MSG':
            _, nickname, message = message
            self.chat.write_message(nickname, message)
        else:
            self.chat.write("Unknown data received: %r" % message)

    def parse_message(self, data):
        return data.split(self.RECORD_SEPARATOR)

    def connected(self):
        return self.state == self.STATE_CONNECTED

    def open(self):
        self.socket.sendto(self.HANDSHAKE_INIT, (self.SERVER, self.PORT))
        while True:
            data = []
            while True:
                datagram = self.socket.recv(256)
                if data != '':
                    data.append(datagram)
                if datagram == '' or datagram[-1] == '\x00':
                    break
            self.handle(self.parse_message(''.join(data)[:-1]))

    def send(self, *args):
        payload = self.RECORD_SEPARATOR.join(args) + '\x00'
        self.socket.sendto(payload, (self.SERVER, self.PORT))


class Chat(object):
    """ The main chat class. Connects the GUI pieces together. """

    def __init__(self, nickname):
        self.nickname = nickname
        self.output = ChatMessages(self)
        self.message = ChatInput(self)
        self.window = Frame(
            body=self.output,
            footer=self.message,
            focus_part='footer'
        )
        self.main_loop = None
        self.connection = Connection(self)

    def connected(self):
        self.write_status('Connected')

    def send_message(self, message):
        self.connection.send('MSG', self.nickname, message)

    def write(self, message):
        self.output.add(message)

    def write_message(self, nickname, message):
        self.write("%s <%s> %s" % (self.time(), nickname, message))

    def write_status(self, message):
        self.write("*** %s ***" % message)

    def time(self, date=False):
        format_string = '%X'
        if date:
            format_string = '%c'
        return datetime.now().strftime(format_string).strip()

    def user_command(self, command):
        arguments = command.split(' ')
        command = arguments.pop(0)

        def _require_args(args, n):
            if len(args) < n:
                self.write("%s needs %d argument(s), %d given" %
                           (command, n, len(args)))
                return False
            return True

        def _quit():
            raise ExitMainLoop()
        def _unknown():
            self.write('Unknown command %r' % command)
        def _nickname(new_nickname):
            self.nickname = new_nickname
            self.write_status('Nickname changed to %r' % new_nickname)

        command_map = {
            'quit': (_quit, 0),
            'nickname': (_nickname, 1)
        }

        command, args_needed = command_map.get(command, (_unknown, 0))
        if _require_args(arguments, args_needed):
            command(*arguments)

    def connect(self):
        self.write_status('Connecting')
        self.connection.open()

    def run(self):
        """ Start the chat client """
        self.write_status("Chat started at %s" % self.time(date=True))
        self.main_loop = MainLoop(self.window, event_loop=GeventLoop())
        gevent.spawn(self.connect)
        self.main_loop.run()


if __name__ == '__main__':

    nickname = "Anonymous"
    if len(sys.argv) > 1:
        nickname = sys.argv[1]

    chat = Chat(nickname)
    try:
        chat.run()
    except KeyboardInterrupt:
        chat.main_loop.stop()
