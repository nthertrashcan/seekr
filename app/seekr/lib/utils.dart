import 'package:web_socket_channel/io.dart';
import 'package:permission_handler/permission_handler.dart';
import 'dart:io';
import 'package:open_file/open_file.dart';

final logfile = File('/storage/emulated/0/Seekr/_/log.txt');
final cachefile = File('/storage/emulated/0/Seekr/_/cache.txt');
final ipfile = File('/storage/emulated/0/Seekr/_/ip.txt');
final pausedfile = File('/storage/emulated/0/Seekr/_/paused.txt');

var extn = [
  "pdf",
  "docx",
  "doc",
  "mp4",
  "mkv",
  "webm",
  "txt",
  "wav",
  "mp3",
  "rar",
  "zip",
  "xz",
  "py",
  "cpp",
  "java",
  "jpeg",
  "png",
  "jpg",
  "xml"
];

var dest = {
  [".png", ".jpeg", ".jpg"]: '/storage/emulated/0/Seekr/Images',
  [".mp4", ".mkv", ".webm"]: '/storage/emulated/0/Seekr/Video',
  [".mp3", ".wav"]: '/storage/emulated/0/Seekr/Audio',
  [".pdf", ".doc", ".docx", ".xml"]: '/storage/emulated/0/Seekr/Documents',
  [".xz", ".zip", ".rar", ".py", ".java", ".cpp"]:
      '/storage/emulated/0/Seekr/Others'
};

class Initialize {
  void reper() async {
    if (await Permission.storage.request().isGranted) {}
    createdir();
  }

  void createdir() async {
    var dir = Directory('/storage/emulated/0/Seekr');
    if (!dir.existsSync()) {
      await Directory('/storage/emulated/0/Seekr').create(recursive: true);
    }
    dir = Directory('/storage/emulated/0/Seekr/Audio');
    if (!dir.existsSync()) {
      await Directory('/storage/emulated/0/Seekr/Audio')
          .create(recursive: true);
    }
    dir = Directory('/storage/emulated/0/Seekr/Video');
    if (!dir.existsSync()) {
      await Directory('/storage/emulated/0/Seekr/Video')
          .create(recursive: true);
    }
    dir = Directory('/storage/emulated/0/Seekr/Images');
    if (!dir.existsSync()) {
      await Directory('/storage/emulated/0/Seekr/Images')
          .create(recursive: true);
    }
    dir = Directory('/storage/emulated/0/Seekr/Documents');
    if (!dir.existsSync()) {
      await Directory('/storage/emulated/0/Seekr/Documents')
          .create(recursive: true);
    }
    dir = Directory('/storage/emulated/0/Seekr/Others');
    if (!dir.existsSync()) {
      await Directory('/storage/emulated/0/Seekr/Others')
          .create(recursive: true);
    }
    dir = Directory('/storage/emulated/0/Seekr/_');
    if (!dir.existsSync()) {
      await Directory('/storage/emulated/0/Seekr/_').create(recursive: true);
    }

    if (!logfile.existsSync()) {
      logfile.writeAsStringSync("");
    }

    if (!cachefile.existsSync()) {
      cachefile.writeAsStringSync("");
    }

    if (!ipfile.existsSync()) {
      ipfile.writeAsStringSync("");
    }

    if (!pausedfile.existsSync()) {
      pausedfile.writeAsStringSync("");
    }
  }

  Initialize() {
    reper();
  }
}

IOWebSocketChannel connect(String ip) {
  IOWebSocketChannel channel;
  channel = IOWebSocketChannel.connect("ws://$ip");
  return channel;
}

void addtoSink(String file, IOWebSocketChannel channel) async {
  var filename = file;
  File f = File("$file");
  filename = filename.split('/').last;
  channel.sink.add("--1$filename");
  channel.sink.add(f.lengthSync().toString());
}

void writeToFile(String filename, int filesize, List<int> bytes) async {
  filename = filedest(filename);
  File file = File('$filename');
  if (check(filename, filesize) == 1 || check(filename, filesize) == 2) {
    file.writeAsBytesSync(bytes, mode: FileMode.writeOnlyAppend);
  }
}

int check(String filename, int filesize) {
  filename = filedest(filename);
  File file = File('$filename');
  if (file.existsSync()) {
    if (filesize > file.lengthSync()) {
      return 2;
    } else {
      return 0;
    }
  } else
    return 1;
}

String filedest(String filename) {
  dest.forEach((key, value) {
    key.forEach((ext) {
      if (filename.endsWith(ext)) {
        filename = "$value/$filename";
      }
    });
  });
  return filename;
}

int leftover(String filename, int filesize) {
  filename = filedest(filename);
  File file = File('$filename');
  return file.lengthSync();
}

List<String> readlog() {
  List<String> loglist = [];
  try {
    logfile.readAsLinesSync().forEach((log) {
      if (log.contains("-u")) {
        log = log.split("-u")[1].trim();
      } else {
        log = log.split("-r")[1].trim();
      }
      if (!loglist.contains(log)) {
        loglist.add(log);
      }
    });
  } catch (e) {}

  return loglist;
}

void cache(String arg) {
  cachefile.writeAsStringSync(arg, mode: FileMode.write);
}

void clearCache() {
  cachefile.writeAsStringSync("", mode: FileMode.write);
}

String readCache() {
  try {
    return cachefile.readAsStringSync();
  } catch (e) {
    return "";
  }
}

void paused(String operation, String arg) {
  pausedfile.writeAsStringSync("$operation$arg", mode: FileMode.write);
}

void clearPause() {
  pausedfile.writeAsStringSync("", mode: FileMode.write);
}

String readPause() {
  try {
    return pausedfile.readAsStringSync();
  } catch (e) {
    return "";
  }
}

void saveIP(String arg) {
  ipfile.writeAsStringSync(arg, mode: FileMode.write);
}

String readIP() {
  try {
    if (ipfile.existsSync()) return ipfile.readAsStringSync();
  } catch (e) {}

  return "0.0.0.0:12345";
}

void open(String file) {
  OpenFile.open(file);
}

bool checkbytes(filename, data) {
  var f = File(filedest(filename));

  try {
    if (f.readAsBytesSync().contains(data)) {
      print("contained already");
      return true;
    } else
      return false;
  } catch (e) {
    return false;
  }
}
