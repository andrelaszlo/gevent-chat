import gevent
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
                self.chat.write_message(message)
            self.set_edit_text('')

        super(ChatInput, self).keypress(size, key)


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

    def write(self, message):
        self.output.add(message)

    def write_message(self, message):
        self.write("%s <%s> %s" % (self.time(), self.nickname, message))

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

    def run(self):
        """ Start the chat client """
        self.write_status("Chat started at %s" % self.time(date=True))
        self.main_loop = MainLoop(self.window, event_loop=GeventLoop())
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
