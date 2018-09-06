import sys
from datetime import datetime as dt

import gi
gi.require_version('Gst', '1.0')
from gi.repository import GObject, Gst


def on_message(bus, message):
    t = message.type
    if t == Gst.MessageType.EOS:
        print('End-Of-Stream reached.')
    elif t == Gst.MessageType.ERROR:
        err, debug = message.parse_error()
        print('Error: {} {}'.format(err, debug))


def main():
    Gst.init(None)

    source = Gst.ElementFactory.make('v4l2src', 'source')
    queue = Gst.ElementFactory.make('queue', 'queue')
    enc = Gst.ElementFactory.make('x264enc', 'enc')
    mux = Gst.ElementFactory.make('mp4mux', 'mux')
    sink = Gst.ElementFactory.make('filesink', 'sink')

    source.set_property('num-buffers', 500)
    sink.set_property('location', dt.now().strftime('%Y_%m_%d') + '.mp4')

    player = Gst.Pipeline.new('player')

    if not player or not source or not queue or not enc or not mux or not sink:
        sys.exit('Init Error!!')

    player.add(source)
    player.add(queue)
    player.add(enc)
    player.add(mux)
    player.add(sink)

    source.link(queue)
    queue.link(enc)
    enc.link(mux)
    mux.link(sink)

    player.set_state(Gst.State.PLAYING)

    bus = player.get_bus()
    bus.add_signal_watch()
    bus.connect('message', on_message)
    bus.timed_pop_filtered(Gst.CLOCK_TIME_NONE,
                           Gst.MessageType.EOS | Gst.MessageType.ERROR)

    player.set_state(Gst.State.NULL)


if __name__ == '__main__':
    main()
