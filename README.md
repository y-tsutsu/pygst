# GStreamerの導入

ひとまず`gst-launch`を使ってUSBカメラの表示と動画保存を行う。

## インストール

```console
$ sudo apt install gstreamer1.0-*
```

自分の環境だと`gstreamer1.0-vaapi`のインストールに失敗するので、個別にインストールする。

```console
$ sudo apt install -y gstreamer1.0-alsa gstreamer1.0-fluendo-mp3 gstreamer1.0-plugins-bad gstreamer1.0-plugins-base-dbg gstreamer1.0-plugins-ugly gstreamer1.0-rtsp gstreamer1.0-x \
gstreamer1.0-clutter-3.0 gstreamer1.0-libav gstreamer1.0-plugins-bad-dbg gstreamer1.0-plugins-base-doc gstreamer1.0-plugins-ugly-dbg gstreamer1.0-rtsp-dbg \
gstreamer1.0-crystalhd gstreamer1.0-libav-dbg gstreamer1.0-plugins-bad-doc gstreamer1.0-plugins-good gstreamer1.0-plugins-ugly-doc gstreamer1.0-tools \
gstreamer1.0-doc gstreamer1.0-nice gstreamer1.0-plugins-base gstreamer1.0-plugins-good-dbg gstreamer1.0-pocketsphinx \
gstreamer1.0-espeak gstreamer1.0-packagekit gstreamer1.0-plugins-base-apps gstreamer1.0-plugins-good-doc gstreamer1.0-pulseaudio
```

## Webカメラの表示と保存

表示

```console
$ gst-launch-1.0 v4l2src ! videoconvert ! ximagesink
```

保存

```console
$ gst-launch-1.0 v4l2src num-buffers=500 \
! queue \
! x264enc \
! mp4mux \
! filesink location=video.mp4
```

## その他

### カメラ接続（VMware）

VMwareでカメラが接続できない場合は、接続設定を行った上で再起動を行うと接続できた。（はじめから接続設定がON状態の状態でVMwareを起動する。）

### 参考URL

[http://littlewing.hatenablog.com/entry/2016/02/24/200129](http://littlewing.hatenablog.com/entry/2016/02/24/200129)

# PythonからGStreamerを呼び出す

動的にパイプを組み替えたい（逆走検知時に別に動画を保存したい）ために、gst-launchを直接使うのではなくPythonのコードからGStreamerを使用したい。

## インストール

```console
$ sudo apt install -y libgirepository1.0-dev
$ pip install pygobject
```

## サンプルコード実行

```console
$ python3 hello.py
```

## その他

### 参考URL

[http://brettviren.github.io/pygst-tutorial-org/pygst-tutorial.html](http://brettviren.github.io/pygst-tutorial-org/pygst-tutorial.html)  
[https://lazka.github.io/pgi-docs/Gst-1.0/classes.html](https://lazka.github.io/pgi-docs/Gst-1.0/classes.html)

# C言語からGSdtreamerを呼び出す

## インストール

```console
$ sudo apt install -y libgstreamer1.0-0 gstreamer1.0-plugins-base gstreamer1.0-plugins-good gstreamer1.0-plugins-bad gstreamer1.0-plugins-ugly gstreamer1.0-libav gstreamer1.0-doc gstreamer1.0-tools
```

## その他

### 参考URL

[https://gstreamer.freedesktop.org/documentation/tutorials/basic/hello-world.html](https://gstreamer.freedesktop.org/documentation/tutorials/basic/hello-world.html)
