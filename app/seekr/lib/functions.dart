import 'utils.dart';
import 'package:web_socket_channel/io.dart';

void receive(IOWebSocketChannel channel, String arg) {
  cache("--0$arg");
  channel.sink.add("--0$arg");
}

void upload(IOWebSocketChannel channel, String file) {
  cache("--1$file");
  addtoSink(file, channel);
}

void download(IOWebSocketChannel channel, String arg) {
  cache("--2$arg");
  channel.sink.add("--2$arg");
}
