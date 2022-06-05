"""Example of video streaming emitter.
This script get the flux from the camera and send it to given ip and port.
The consumer of this script can be the script video_stream_consumer.py
"""
import datetime

from hermes.camera.CV2AsynchronousVideoCapture import \
    CV2AsynchronousVideoCapture
from hermes.stream.VideoStream import VideoStream
from hermes.network.AsyncUDPChannel import AsyncUDPChannel
import cv2

encoding_param = {"params": [int(cv2.IMWRITE_JPEG_QUALITY), 50]}

server_ip = "192.168.50.1"
server_port = 8000
emitter_port = 8001


class Consumer:
    client_ttl = 15

    def __init__(self, _consumer_ip, _consumer_port):
        self.ip = _consumer_ip
        self.port = _consumer_port
        self.last_contact = datetime.datetime.now()

    def new_contact(self):
        self.last_contact = datetime.datetime.now()

    def is_alive(self):
        return (
                       datetime.datetime.now() - self.last_contact).seconds <= Consumer.client_ttl


if __name__ == "__main__":
    consumers = {}
    server = AsyncUDPChannel(socket_ip=server_ip,
                             socket_port=server_port).start()

    recorder = CV2AsynchronousVideoCapture().start()
    emitter = VideoStream(role=VideoStream.EMITTER, socket_ip=server_ip,
                          encoding_param=encoding_param,
                          socket_port=emitter_port).start()

    while recorder.read_frame() is None:
        pass
    while emitter.get_is_running() is False:
        pass
    print("start")
    # Add new subscribers or refresh existing
    while True:
        if server.message_available():
            msg = server.pull()
            consumer_ip = msg[1][0]
            try:
                consumer_port = int(bytes.decode(msg[0], 'utf8'))
            except:
                print("Invalid message")
            consumer_name = str(consumer_ip) + str(consumer_port)
            if consumer_name not in consumers.keys():
                consumers[consumer_name] = Consumer(consumer_ip, consumer_port)
                emitter.add_subscriber((consumer_ip, consumer_port))
                print(f"start sending to {consumer_ip}:{consumer_port}")
                print(consumers)
            else:
                consumers[consumer_name].new_contact()
                print(f"contact from {consumer_ip}:{consumer_port}")

        # Remove inactive subscribers
        consumer_names = [key for key in consumers.keys()]
        for consumer_name in consumer_names:
            if not consumers[consumer_name].is_alive():
                for i, subscriber in enumerate(emitter.get_subs_list()):
                    if subscriber[0] == consumers[consumer_name].ip and \
                            subscriber[1] == consumers[consumer_name].port:
                        print(
                            f"stop sending to {consumers[consumer_name].ip}:{consumers[consumer_name].port}")
                        emitter.remove_subscriber(i)
                        consumers.pop(consumer_name)
                        break

        # Send picture
        frame = recorder.read_frame()
        emitter.refresh_image(frame)

    recorder.stop()
    emitter.stop()
    server.stop()