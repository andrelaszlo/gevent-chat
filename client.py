import gevent
import urwid
from urwid_geventloop import GeventLoop

txt = urwid.Text(u"Hello World")
fill = urwid.Filler(txt, 'top')
main_loop = urwid.MainLoop(fill, event_loop=GeventLoop())
#gevent.spawn(background_loop)
main_loop.run()
