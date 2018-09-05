import sys

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
    convert = Gst.ElementFactory.make('videoconvert', 'convert')
    sink = Gst.ElementFactory.make('ximagesink', 'sink')

    player = Gst.Pipeline.new('player')

    if not player or not source or not convert or not sink:
        sys.exit('Init Error!!')

    player.add(source)
    player.add(convert)
    player.add(sink)

    source.link(convert)
    convert.link(sink)

    player.set_state(Gst.State.PLAYING)

    bus = player.get_bus()
    bus.add_signal_watch()
    bus.connect('message', on_message)
    bus.timed_pop_filtered(Gst.CLOCK_TIME_NONE,
                           Gst.MessageType.EOS | Gst.MessageType.ERROR)

    player.set_state(Gst.State.NULL)


if __name__ == '__main__':
    main()
