# Gevent chat

An example UDP chat client and server using Gevent and urwt.

The main purpose of this program is to experiment with gevent's sockets and
`DatagramServer` and urwt/gevent integration. It's very much a toy/work in
progress and is not an example of best practices.


## Getting started

Clone and start a virtualenv. Install the requirements:

    $ pip install -r requirements.txt

Start the server (modify port in the source code if needed):

    $ python server.py

Start a client (change server and port in source if needed):

    $ python client.py <nickname>


## Mandatory screenshot

The screenshot below shows the author chatting with himself:

![So much fun](/misc/screenshot.gif)


## TODO

* Client heartbeat to reconnect when server is restarted and to garbage collect
  old clients.
* Better message format. Currently the record separator character is used.
* It feels slow, maybe because of urwt. Do some profiling.
* More server features like chat rooms, private messages etc
* ...