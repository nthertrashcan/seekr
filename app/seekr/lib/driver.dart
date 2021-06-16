import 'dart:io';
import 'dart:math';
import 'package:file_picker/file_picker.dart';
import 'package:flutter/cupertino.dart';
import 'package:flutter/material.dart';
import 'package:web_socket_channel/io.dart';
import 'functions.dart';
import 'utils.dart';
import 'package:percent_indicator/percent_indicator.dart';
import 'package:flutter_treeview/flutter_treeview.dart';
import 'package:blinking_text/blinking_text.dart';
import 'package:flutter_fadein/flutter_fadein.dart';

class Driver extends StatefulWidget {
  @override
  _DriverState createState() => _DriverState();
}

class _DriverState extends State<Driver> {
  String currentip = "0.0.0.0:12345";
  String filename = "a";
  String notFound = "Not Found!!!";
  String operation = "";
  String waitingMessage = "";
  String currentFile = "";

  int n1 = 0;
  int n2 = 0;

  int e = 0;
  int ne = 0;
  int uploadingFileSize = 0;
  int incomingFileSize = 0;
  int currentFileSize = 0;

  double percentage = 0.0;
  List<Node> nodes = [];
  List<int> uploadingData = [];
  List<String> incominglof = [];
  List<String> outgoinglof = [];
  bool activateTextfield = false;
  bool isRunning = false;
  bool isUploading = false;
  bool isSearching = false;
  bool isDownloading = false;
  bool isReceiving = false;
  bool isConnected = false;
  bool isPaused = false;

  TextEditingController ip = new TextEditingController();
  TextEditingController query = new TextEditingController();

  var channel;
  var progressColor = Colors.white;

  final fadeController = FadeInController();

  @override
  void initState() {
    Initialize();
    currentip = readIP();
    super.initState();
  }

  @override
  Widget build(BuildContext context) {
    return home(context);
  }

  Widget home(context) {
    setState(() {
      try {
        if (this.nodes.isEmpty) {
          this.nodes = lof();
        }
      } catch (e) {}
    });

    TreeViewController _treeViewController =
        TreeViewController(children: this.nodes);

    TreeViewTheme _treeViewTheme = TreeViewTheme(
      expanderTheme: ExpanderThemeData(
        type: ExpanderType.caret,
        modifier: ExpanderModifier.none,
        position: ExpanderPosition.start,
        color: Colors.grey,
        size: 20,
      ),
      labelStyle:
          TextStyle(fontSize: 13, letterSpacing: 0.1, fontFamily: 'Muli'),
      parentLabelStyle: TextStyle(
        fontSize: 16,
        letterSpacing: 0.1,
        fontFamily: 'Muli',
        fontWeight: FontWeight.w800,
        color: Colors.blue,
      ),
      iconTheme: IconThemeData(
        size: 18,
        color: Colors.grey[300],
      ),
      colorScheme: ColorScheme.light(),
    );

    return Scaffold(
        appBar: AppBar(
          title: Container(
            padding: EdgeInsets.only(left: 80),
            child: Row(
                mainAxisAlignment: MainAxisAlignment.spaceBetween,
                children: [
                  isRunning
                      ? IconButton(
                          onPressed: () => stop(),
                          icon: Icon(Icons.stop),
                        )
                      : activateTextfield
                          ? IconButton(
                              onPressed: () {
                                setState(() {
                                  this.activateTextfield = false;
                                });
                              },
                              icon: Icon(Icons.home))
                          : IconButton(
                              onPressed: () {
                                lof();
                                channel = connect(currentip);
                                listener();
                              },
                              icon: Icon(Icons.cloud,
                                  color: isConnected
                                      ? Colors.blue
                                      : Colors.white)),
                  isRunning
                      ? readPause() == ""
                          ? IconButton(
                              onPressed: () => pause(), icon: Icon(Icons.pause))
                          : Container()
                      : readCache() != ""
                          ? IconButton(
                              onPressed: () {
                                clearCache();
                                this.outgoinglof.clear();
                                this.incominglof.clear();
                              },
                              icon: Icon(Icons.delete))
                          : readPause() != ""
                              ? IconButton(
                                  onPressed: () =>
                                      !this.isConnected ? null : resume(),
                                  icon: Icon(Icons.play_arrow))
                              : Container(),
                ]),
          ),
          backgroundColor: Colors.grey[350],
        ),
        backgroundColor: Colors.yellow.shade50,
        drawer: Drawer(
          child: ListView(
            controller: ScrollController(initialScrollOffset: 1.0),
            padding: EdgeInsets.zero,
            children: <Widget>[
              ListTile(
                title: Container(),
              ),
              ListTile(
                  title: TextField(
                      controller: ip,
                      decoration: InputDecoration(
                          hintText: currentip == "0.0.0.0:12345"
                              ? "Enter IP"
                              : "Change IP"))),
              ListTile(
                title: Icon(Icons.smart_button),
                onTap: () {
                  if (ip.text != "") {
                    currentip = ip.text;
                    channel = connect(currentip);
                    listener();
                  }

                  ip.text = "";
                  Navigator.pop(context);
                },
              ),
              Container(
                  height: MediaQuery.of(context).size.height / 1.5,
                  child: TreeView(
                      controller: _treeViewController,
                      onNodeTap: (key) {
                        setState(() {
                          _treeViewController =
                              _treeViewController.copyWith(selectedKey: key);
                          open(key);
                          Navigator.pop(context);
                        });
                      },
                      theme: _treeViewTheme)),
            ],
          ),
        ),
        body: Column(crossAxisAlignment: CrossAxisAlignment.center, children: [
          isRunning
              ? Container()
              : activateTextfield
                  ? getInput()
                  : Container(),
          isRunning
              ? Container()
              : activateTextfield
                  ? Container()
                  : main(),
          isUploading ? progress() : Container(),
          isSearching ? _incominglof(_treeViewTheme) : Container(),
          isReceiving ? progress() : Container(),
          FadeIn(
            child: BlinkText(' $waitingMessage',
                style: TextStyle(fontSize: 15.0, color: Colors.blue),
                beginColor: Colors.grey[300],
                times: pow(2, 64).toInt(),
                duration: Duration(seconds: 1)),
            duration: Duration(milliseconds: 10),
            controller: fadeController,
          )
        ]));
  }

  Widget main() {
    return Container(
        padding: EdgeInsets.only(top: 100),
        child: Column(children: [
          IconButton(
              iconSize: 150,
              icon: Icon(Icons.cloud_upload_outlined),
              onPressed: !this.isConnected
                  ? null
                  : () {
                      pickfiles();
                    }),
          IconButton(
              iconSize: 150,
              icon: Icon(Icons.cloud_download_outlined),
              onPressed: !this.isConnected
                  ? null
                  : () {
                      setState(() {
                        this.activateTextfield = true;
                        this.waitingMessage = "Searching";
                      });
                    }),
          IconButton(
              iconSize: 20,
              icon: Icon(Icons.download_for_offline_outlined),
              onPressed: !this.isConnected
                  ? null
                  : () {
                      setState(() {
                        this.activateTextfield = true;
                        this.waitingMessage = "Downloading";
                        this.isDownloading = true;
                      });
                    })
        ]));
  }

  Widget getInput() {
    return Container(
        padding: EdgeInsets.fromLTRB(0, 20, 0, 0),
        child: Row(
          mainAxisAlignment: MainAxisAlignment.spaceAround,
          children: [
            Container(
                width: 200.0,
                child: TextField(
                  maxLines: null,
                  keyboardType: TextInputType.multiline,
                  style: TextStyle(fontFamily: 'Muli', fontSize: 15),
                  controller: query,
                  autofocus: true,
                  showCursor: _keyboardIsVisible() ? false : true,
                  decoration: InputDecoration(
                    isCollapsed: !_keyboardIsVisible() ? false : true,
                  ),
                )),
            IconButton(
                icon: Icon(Icons.send),
                onPressed: () {
                  setState(() {
                    this.isRunning = true;
                    if (this.isDownloading) {
                      this.operation = "--2";
                      download(channel, query.text);
                    } else {
                      this.operation = "--0";
                      receive(channel, query.text);
                    }
                    query.text = "";
                    fadeController.fadeIn();
                  });
                })
          ],
        ));
  }

  Widget progress() {
    return Container(
        padding: EdgeInsets.only(top: 100),
        child: CircularPercentIndicator(
          radius: 200.0,
          lineWidth: 1.0,
          percent: this.percentage,
          center: new Text(
            "  ${(this.percentage * 100).ceil()}%",
            style: new TextStyle(fontWeight: FontWeight.bold, fontSize: 20.0),
          ),
          footer: new Text(
            filename,
            style: new TextStyle(fontWeight: FontWeight.bold, fontSize: 11.0),
          ),
          circularStrokeCap: CircularStrokeCap.butt,
          progressColor: this.progressColor,
        ));
  }

  void resume() {
    var arg = readPause();
    if (arg != "") {
      if (arg.contains("--1")) {
        arg = arg.split("--1")[1];
        if (!this.outgoinglof.contains(arg)) {
          this.outgoinglof.add(arg);
        }
        this.currentFile = this.outgoinglof[0];

        upload(channel, this.outgoinglof[0]);
        setState(() {
          this.isRunning = true;
        });
        clearPause();
      } else if (arg.contains("--2")) {
        arg = arg.split("--2")[1];
        this.currentFile = arg;
        download(channel, arg);
        setState(() {
          this.isRunning = true;
          this.operation = "--2";
          this.waitingMessage = "Downloading";
          fadeController.fadeIn();
        });
        clearPause();
      } else if (arg.contains("--0")) {
        arg = arg.split("--0")[1];
        this.currentFile = arg;
        receive(channel, arg);
        setState(() {
          if (!arg.contains("--r")) {
            this.waitingMessage = "Searching";
            fadeController.fadeIn();
          }
          this.isRunning = true;
        });
        clearPause();
      }
    }
  }

  void pause() {
    setState(() {
      clearCache();
      paused(this.operation, this.currentFile);
      this.isPaused = true;
      this.activateTextfield = false;
      this.fadeController.fadeOut();
      this.percentage = 0.0;
      this.filename = "";

      if (this.isUploading) {
        channel.sink.add("--C");

        if (this.outgoinglof.length > 1) {
          this.outgoinglof.removeAt(0);
          if (this.outgoinglof.isNotEmpty) {
            if (this.isConnected) {
              this.currentFile = this.outgoinglof[0];
              upload(channel, this.outgoinglof[0]);
            }
          }
        } else {
          this.outgoinglof.removeAt(0);
          this.isRunning = false;
          this.isUploading = false;
          this.isConnected = false;

          channel.sink.close();
        }
      } else if (isReceiving) {
        channel.sink.add("--C");

        this.isRunning = false;
        this.isSearching = false;
        this.isReceiving = false;
        this.isConnected = false;
        this.isDownloading = false;
        channel.sink.close();
      } else {
        this.isRunning = false;
        this.isSearching = false;
        this.isReceiving = false;
        this.isConnected = false;
        this.isDownloading = false;
        try {
          channel.sink.close();
        } catch (e) {}
      }
    });
  }

  void stop() {
    setState(() {
      if (isSearching) {
        clearCache();
      }
      this.fadeController.fadeOut();
      this.activateTextfield = false;
      this.isRunning = false;
      this.isUploading = false;
      this.isSearching = false;
      this.isReceiving = false;
      this.isConnected = false;

      try {
        channel.sink.add("--C");
        channel.sink.close();
      } catch (e) {}
    });
  }

  void _onConnecting() {
    setState(() {
      this.isConnected = true;
    });
    saveIP(this.currentip);
    var arg = readCache();
    if (arg != "") {
      if (arg.contains("--1")) {
        arg = arg.split("--1")[1];
        if (!this.outgoinglof.contains(arg)) {
          this.outgoinglof.add(arg);
        }
        this.currentFile = this.outgoinglof[0];
        upload(channel, this.outgoinglof[0]);
        setState(() {
          this.isRunning = true;
        });
      } else if (arg.contains("--2")) {
        arg = arg.split("--2")[1];
        this.currentFile = arg;
        download(channel, arg);
        setState(() {
          this.isRunning = true;
          this.operation = "--2";
          this.waitingMessage = "Downloading";
          fadeController.fadeIn();
        });
      } else if (arg.contains("--0")) {
        arg = arg.split("--0")[1];

        this.currentFile = arg;
        receive(channel, arg);
        setState(() {
          if (!arg.contains("--r")) {
            this.waitingMessage = "Searching";
            fadeController.fadeIn();
          }
          this.isRunning = true;
        });
      }
    }
  }

  void _processUploadingBytes(element) {
    if (this.outgoinglof.isNotEmpty) {
      this.uploadingFileSize = int.parse(element.split("--upnbytes")[1]);
      if (this.uploadingFileSize == -2) {
        clearCache();
        setState(() {
          if (this.outgoinglof.length == 1) this.isRunning = false;
        });
        this.outgoinglof.removeAt(0);
        if (this.outgoinglof.isNotEmpty) {
          this.currentFile = this.outgoinglof[0];
          upload(channel, this.outgoinglof[0]);
        }
      } else {
        setState(() {
          this.isUploading = true;
        });
        n1 = this.uploadingFileSize;
        n2 = this.uploadingFileSize + e;
        this.filename = this.outgoinglof[0];
        File f = File("$filename");
        this.filename = this.filename.split("/").last;
        this.uploadingData = f.readAsBytesSync();
        ne = (this.uploadingData.length.toString()).length - 1;
        if (ne > 6) {
          ne = 6;
        }
        e = pow(10, ne).toInt();
      }
    }
  }

  void _processUploading() {
    if (this.isConnected) if (this.uploadingFileSize != -2) {
      var updl = this.uploadingData.length;
      if (this.uploadingFileSize < updl) {
        if (n2 < updl) {
          this.percentage = n2 / updl;
          changePercent(this.percentage);
          channel.sink.add(this.uploadingData.sublist(n1, n2));
          n1 = n2;
          n2 += e;
        } else {
          channel.sink.add(this.uploadingData.sublist(n1, updl));
          channel.sink.add("--X");
        }
      }
    }
  }

  void _processOnUpload() {
    changePercent(1.0);
    if (this.isConnected) {
      this.outgoinglof.removeAt(0);
      if (this.outgoinglof.isNotEmpty) {
        this.currentFile = this.outgoinglof[0];
        upload(channel, this.outgoinglof[0]);
      }
    }
  }

  void _processReceivingBytes(element) {
    if (this.operation == "--2") {
      fadeController.fadeOut();
    }
    this.incomingFileSize = int.parse(element.split("--nbytes")[1]);
  }

  void _processReceivingFileExistence(file) {
    extn.forEach((e) {
      if (file.toString().endsWith(e)) {
        this.filename = file;
        if (isDownloading) this.currentFile = file;
        if (check(this.filename, this.incomingFileSize) == 1) {
          channel.sink.add("--111");
          setState(() {
            this.isReceiving = true;
          });
        } else if (check(this.filename, this.incomingFileSize) == 2) {
          channel.sink.add("--222");
          setState(() {
            this.isReceiving = true;
          });
          this.currentFileSize = leftover(this.filename, this.incomingFileSize);

          channel.sink.add(currentFileSize.toString());
        } else {
          channel.sink.add("--000");
          this.currentFile = "";
          clearCache();
          setState(() {
            this.activateTextfield = false;
            this.isRunning = false;
            this.isReceiving = false;
            this.isDownloading = false;
            this.isSearching = false;

            open(filedest(filename));
          });
        }
      }
    });
  }

  void _processRecievingByteData(data) {
    writeToFile(this.filename, this.incomingFileSize, data);
    this.currentFileSize = File('${filedest(filename)}').lengthSync();
    this.percentage = currentFileSize / incomingFileSize;
    changePercent(this.percentage);
  }

  void _processIncomingLof(element) {
    setState(() {
      fadeController.fadeOut();
      this.incominglof = element.split("--lof")[1].split("+");
      // print(this.incominglof);
      if (this.incominglof[0] == "") {
        clearCache();
        this.notFound = "Not found!!!";
      }
      this.isSearching = true;
    });
  }

  void listener() {
    channel.stream.forEach((element) {
      if (element.runtimeType == String) {
        if (element.contains("--connsucc200")) {
          _onConnecting();
        } else if (element.contains("--upnbytes")) {
          _processUploadingBytes(element);
        } else if (element.contains("--uploading")) {
          _processUploading();
        } else if (element.contains("--uploaded")) {
          _processOnUpload();
        } else if (element.contains("--lof")) {
          _processIncomingLof(element);
        } else if (element.contains("--ifp")) {
          if (!readCache().contains("--d")) {
            cache("${readCache()} --d${element.split("--ifp")[1]}");
            this.currentFile = readCache().split("--0")[1];
          }
        } else if (element.contains("--nbytes")) {
          fadeController.fadeOut();
          _processReceivingBytes(element);
        } else {
          _processReceivingFileExistence(element);
        }
      } else {
        try {
          if (this.isConnected) {
            _processRecievingByteData(element);
            if (this.isConnected) channel.sink.add("--X");
          }
        } catch (e) {}
      }
    });
  }

  void changePercent(perc) {
    setState(() {
      if (perc < 1.0) {
        this.percentage = perc;
      } else {
        var op = "";
        this.nodes = lof();
        this.percentage = 0.0;
        this.activateTextfield = false;
        this.isSearching = false;
        this.isReceiving = false;

        if (this.isUploading) {
          op = "u";
          if (this.outgoinglof.length == 1) {
            this.isRunning = false;
            this.isUploading = false;
            this.isConnected = false;
            channel.sink.close();
          }
        } else {
          this.isRunning = false;
          this.isUploading = false;
          this.isConnected = false;
          open(filedest(filename));
          channel.sink.close();
          op = "r";
        }

        clearCache();

        if (readPause().contains(currentFile)) {
          clearPause();
        }

        if (!readlog().contains(filename))
          logfile.writeAsStringSync("-$op $filename\n",
              mode: FileMode.writeOnlyAppend);
      }
    });
  }

  void pickfiles() async {
    this.outgoinglof = [];
    try {
      FilePickerResult? result =
          await FilePicker.platform.pickFiles(allowMultiple: true);
      if (result != null) {
        List<File> files = result.paths.map((path) => File(path!)).toList();
        files.forEach((element) {
          var path = element.path.toString();
          if (!this.outgoinglof.contains(path)) {
            this.outgoinglof.add(path);
          }
        });

        try {
          this.currentFile = this.outgoinglof[0];
          upload(channel, this.outgoinglof[0]);
          setState(() {
            this.isRunning = true;
            this.operation = "--1";
          });
        } catch (e) {}
      }
    } catch (e) {}
  }

  bool _keyboardIsVisible() {
    return (MediaQuery.of(context).viewInsets.bottom == 0.0);
  }

  List<Node> _getIncomingLofTreeView(List lof) {
    List<Node> nodes = [];
    if (lof.isNotEmpty) {
      var fileswithextn = {};
      var crosscheck = [];
      fileswithextn["directory"] = [];
      extn.forEach((ext) {
        fileswithextn[ext] = [];
      });
      lof.forEach((file) {
        extn.forEach((ext) {
          if (file.endsWith(ext)) {
            fileswithextn[ext].add(file);
            crosscheck.add(file);
          }
        });
        if (!crosscheck.contains(file)) {
          fileswithextn["directory"].add(file);
        }
      });

      fileswithextn.forEach((key, value) {
        List<Node> internalNodes = [];
        if (value.isNotEmpty) {
          value.forEach((file) {
            internalNodes.add(Node(key: file, label: file));
          });
          nodes.add(Node(key: key, label: key, children: internalNodes));
        }
      });
    }

    return nodes;
  }

  List<Node> lof() {
    var dir = Directory('/storage/emulated/0/Seekr');
    List<Node> nodes = [];
    var icon = {
      "Audio": Icons.music_note,
      "Video": Icons.featured_video,
      "Documents": Icons.text_snippet_rounded,
      "Images": Icons.image_sharp,
      "Others": Icons.file_present,
      "_": Icons.text_snippet
    };

    dir.list(recursive: false, followLinks: true).forEach((element) {
      List<Node> internalNodes = [];
      var internalFiles = [];
      var filesExist = false;
      var dirname = element.path.split("/").last;
      var curdir = Directory(element.path);
      curdir.listSync().forEach((file) {
        internalFiles.add(file.path);
        filesExist = true;
      });
      if (filesExist) {
        internalFiles.forEach((file) {
          internalNodes.add(Node(
              label: file.split("/").last, key: file, icon: icon[dirname]));
        });
        nodes.add(Node(
            label: dirname,
            key: element.path,
            icon: Icons.folder,
            children: internalNodes));
      }
    }).whenComplete(() {
      setState(() {
        this.nodes = nodes;
      });
    });
    return nodes;
  }

  Widget _incominglof(_treeViewTheme) {
    TreeViewController _treeViewController =
        TreeViewController(children: _getIncomingLofTreeView(this.incominglof));

    if (!_keyboardIsVisible()) {
      this.notFound = "";
    }
    return this.incominglof[0] != ""
        ? Container(
            height: _keyboardIsVisible()
                ? MediaQuery.of(context).size.height / 1.5
                : MediaQuery.of(context).size.height / 4,
            padding: EdgeInsets.all(20.0),
            child: TreeView(
                controller: _treeViewController,
                onNodeTap: (key) {
                  setState(() {
                    _treeViewController =
                        _treeViewController.copyWith(selectedKey: key);

                    var selectedfile = key;
                    var dirflag = true;
                    extn.forEach((ext) {
                      if (selectedfile.endsWith(ext)) {
                        selectedfile = selectedfile.split("." + ext)[0];
                        dirflag = false;
                      }
                    });
                    if (dirflag)
                      cache("--0$selectedfile --r$key.zip");
                    else
                      cache("--0$selectedfile --r$key");

                    channel.sink.add(key);
                    this.isSearching = false;
                    this.isReceiving = true;
                  });
                },
                theme: _treeViewTheme))
        : Container(
            child: Text(this.notFound,
                style: TextStyle(
                    fontFamily: 'Muli',
                    color: Colors.red[300],
                    fontSize: 14,
                    fontWeight: FontWeight.bold)));
  }
}
