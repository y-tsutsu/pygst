# Webカメラの表示と保存

表示

```console
$ gst-launch-1.0 v4l2src ! videoconvert ! ximagesink
```

保存

```console
$ timeout 30 gst-launch-1.0 -v v4l2src \
! videorate \
! video/x-raw,framerate=30/1 \
! clockoverlay \
! x264enc \
! h264parse \
! mpegtsmux \
! filesink location=`date -I`.ts
```

参考URL

http://littlewing.hatenablog.com/entry/2016/02/24/200129
