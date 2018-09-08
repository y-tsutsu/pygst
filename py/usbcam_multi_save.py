import sys
from datetime import datetime as dt

import gi
gi.require_version('Gst', '1.0')
from gi.repository import GObject, Gst, GLib

osel_src1 = None
osel_src2 = None

SWITCH_TIMEOUT_SEC = 10


def my_bus_callback(bus, message, loop):
    t = message.type
    if t == Gst.MessageType.ERROR:
        err, debug = message.parse_error()
        print('Error: {}'.format(err))
        loop.quit()
    elif t == Gst.MessageType.EOS:
        loop.quit()
    else:
        # print(t)
        pass
    return True


def switch_cb(user_data):
    print('!!!')

    sel, sink1, sink2 = user_data
    old_pad = sel.get_property('active-pad')
    new_pad = osel_src2 if old_pad == osel_src1 else osel_src1

    new_sink = sink2 if old_pad == osel_src1 else sink1
    new_sink.set_state(Gst.State.NULL)
    new_sink.set_property('location', dt.now().strftime('%Y_%m_%d_%H_%M_%S') + '.mp4')
    new_sink.set_state(Gst.State.PLAYING)

    sel.set_property('active-pad', new_pad)
    return True


def on_bin_element_added(bin, element):
    element.set_property('sync', False)
    element.set_property('async', False)


def main():
    global osel_src1
    global osel_src2

    Gst.init(None)
    loop = GLib.MainLoop().new(None, False)

    pipline = Gst.Pipeline.new('pipeline')

    src = Gst.ElementFactory.make('videotestsrc', 'src')
    c0 = Gst.ElementFactory.make('videoconvert', None)
    toverlay = Gst.ElementFactory.make('timeoverlay', 'timeoverlay')
    enc = Gst.ElementFactory.make('x264enc', 'enc')
    osel = Gst.ElementFactory.make('output-selector', 'osel')
    sink1 = Gst.ElementFactory.make('filesink', 'sink1')
    sink2 = Gst.ElementFactory.make('filesink', 'sink2')

    if not pipline or not src or not c0 or not toverlay or not osel or not sink1 or not sink2:
        sys.exit('missing element')

    pipline.add(src)
    pipline.add(c0)
    pipline.add(toverlay)
    pipline.add(enc)
    pipline.add(osel)
    pipline.add(sink1)
    pipline.add(sink2)

    osel.set_property('resend-latest', True)
    sink1.set_property('location', dt.now().strftime('%Y_%m_%d_%H_%M_%S') + '.mp4')
    sink2.set_property('location', dt.now().strftime('%Y_%m_%d_%H_%M_%S') + '.mp4')
    sink1.set_property('sync', False)
    sink2.set_property('sync', False)
    sink1.set_property('async', False)
    sink2.set_property('async', False)

    src.link(c0)
    c0.link(toverlay)
    toverlay.link(enc)
    enc.link(osel)

    sinkpad = sink1.get_static_pad('sink')
    osel_src1 = osel.get_request_pad('src_%u')

    if osel_src1.link(sinkpad) != Gst.PadLinkReturn.OK:
        sys.exit('linking output 1 converter failed')

    sinkpad = sink2.get_static_pad('sink')
    osel_src2 = osel.get_request_pad('src_%u')

    if osel_src2.link(sinkpad) != Gst.PadLinkReturn.OK:
        sys.exit('linking output 2 converter failed')

    GObject.timeout_add_seconds(SWITCH_TIMEOUT_SEC, switch_cb, (osel, sink1, sink2))

    bus = pipline.get_bus()
    bus.add_watch(0, my_bus_callback, loop)

    pipline.set_state(Gst.State.PLAYING)

    loop.run()

    pipline.set_state(Gst.State.NULL)


if __name__ == '__main__':
    main()
