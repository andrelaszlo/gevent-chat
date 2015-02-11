import gevent
from urwid import ListBox, SimpleFocusListWalker, Frame, MainLoop, Edit, Text
from urwid_geventloop import GeventLoop

class ChatMessages(ListBox):
    def __init__(self, chat):
        self.chat = chat
        self.walker = SimpleFocusListWalker([])
        super(ChatMessages, self).__init__(self.walker)

    def add(self, message):
        self.walker.append(Text(message))
        self.set_focus(len(self.walker)-1)

class ChatInput(Edit):

    def __init__(self, chat):
        self.chat = chat
        super(ChatInput, self).__init__(caption='> ')

    def keypress(self, size, key):
        if key == 'enter':
            self.chat.output.add(self.get_edit_text())
            self.set_edit_text('')
        super(ChatInput, self).keypress(size, key)

class Chat(object):

    def __init__(self):
        self.output = ChatMessages(self)
        self.message = ChatInput(self)
        self.window = Frame(
            body=self.output,
            footer=self.message,
            focus_part='footer'
        )

    def run(self):
        for i in range(100):
            self.output.add("Test message %d" % i)
        main_loop = MainLoop(self.window, event_loop=GeventLoop())
        main_loop.run()

if __name__ == '__main__':
    Chat().run()
