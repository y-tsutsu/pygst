import sys
from datetime import datetime as dt

import gi
gi.require_version('Gst', '1.0')
from gi.repository import GObject, Gst, GLib

osel_src1 = None
osel_src2 = None


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
    sel = user_data
    old_pad = sel.get_property('active-pad')
    if old_pad == osel_src1:
        new_pad = osel_src2
    else:
        new_pad = osel_src1
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
    osel = Gst.ElementFactory.make('output-selector', 'osel')
    c1 = Gst.ElementFactory.make('videoconvert', None)
    c2 = Gst.ElementFactory.make('videoconvert', None)
    sink1 = Gst.ElementFactory.make('autovideosink', 'sink1')
    sink2 = Gst.ElementFactory.make('autovideosink', 'sink2')

    if not pipline or not src or not c0 or not toverlay or not osel or not c1 or not c2 or not sink1 or not sink2:
        sys.exit('missing element')

    pipline.add(src)
    pipline.add(c0)
    pipline.add(toverlay)
    pipline.add(osel)
    pipline.add(c1)
    pipline.add(sink1)
    pipline.add(c2)
    pipline.add(sink2)

    src.set_property('is-live', True)
    src.set_property('do-timestamp', True)
    src.set_property('num-buffers', 500)
    osel.set_property('resend-latest', True)

    sink1.connect('element-added', on_bin_element_added)
    sink2.connect('element-added', on_bin_element_added)

    src.link(c0)
    c0.link(toverlay)
    toverlay.link(osel)

    sinkpad = c1.get_static_pad('sink')
    osel_src1 = osel.get_request_pad('src_%u')

    if osel_src1.link(sinkpad) != Gst.PadLinkReturn.OK:
        sys.exit('linking output 1 converter failed')

    c1.link(sink1)

    sinkpad = c2.get_static_pad('sink')
    osel_src2 = osel.get_request_pad('src_%u')

    if osel_src2.link(sinkpad) != Gst.PadLinkReturn.OK:
        sys.exit('linking output 2 converter failed')

    c2.link(sink2)

    SWITCH_TIMEOUT = 1
    GObject.timeout_add_seconds(SWITCH_TIMEOUT, switch_cb, osel)

    bus = pipline.get_bus()
    bus.add_watch(0, my_bus_callback, loop)

    pipline.set_state(Gst.State.PLAYING)

    loop.run()

    pipline.set_state(Gst.State.NULL)


if __name__ == '__main__':
    main()
