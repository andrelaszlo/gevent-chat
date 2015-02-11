# Gevent chat

An example UDP chat client and server using Gevent and urwid.

The main purpose of this program is to experiment with gevent's sockets and
`DatagramServer` and urwid/gevent integration. It's very much a toy/work in
progress and is not an example of best practices.


## Getting started

Clone and start a virtualenv. Install the requirements:

    $ pip install -r requirements.txt

Start the server (modify port in the source code if needed):

    $ python server.py

Start a client (change server and port in source if needed):

    $ python client.py <nickname>


## Features

* Multiple client chat over UDP
* Scrolling message pane (click on it and use the up/down arrows)
* Change nickname using `/nickname <newnickname>`
* Quit using `/quit` or `ctrl-C`


## Mandatory screenshot

The screenshot below shows the author chatting with himself:

![So much fun](/misc/screenshot.png)


## TODO

* Client heartbeat to reconnect when server is restarted and to garbage collect
  old clients.
* Better message format. Currently the record separator character is used.
* It feels slow, maybe because of urwid. Do some profiling.
* More server features like chat rooms, private messages etc
* Think about security :D
* Handle client connection state better
* ...