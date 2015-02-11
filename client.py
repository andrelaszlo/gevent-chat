import gevent
from urwid import ListBox, SimpleFocusListWalker, Frame, MainLoop, Edit, Text
from urwid_geventloop import GeventLoop

class ChatMessages(ListBox):
    def __init__(self):
        self.walker = SimpleFocusListWalker([])
        super(ChatMessages, self).__init__(self.walker)

    def add(self, message):
        self.walker.append(Text(message))
        self.set_focus(len(self.walker)-1)

class ChatInput(Edit):

    def setup(self, messages):
        self.messages = messages
        return self

    def keypress(self, size, key):
        if key == 'enter':
            self.messages.add(self.get_edit_text())
            self.set_edit_text('')
        super(ChatInput, self).keypress(size, key)

output = ChatMessages()
for i in range(100):
    output.add("Test message %d" % i)

message = ChatInput(caption='> ').setup(output)

window = Frame(body=output, footer=message, focus_part='footer')
main_loop = MainLoop(window, event_loop=GeventLoop())
#gevent.spawn(background_loop)
main_loop.run()
