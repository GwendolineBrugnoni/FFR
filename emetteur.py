"""Example of video streaming emitter.
This script get the flux from the camera and send it to given ip and port.
The consumer of this script can be the script video_stream_consumer.py
"""
from hermes.camera.CV2AsynchronousVideoCapture import CV2AsynchronousVideoCapture
from hermes.stream.VideoStream import VideoStream
import cv2

consumer_ip = "127.0.0.1"
consumer_port = 5000
encoding_param = {"params": [int(cv2.IMWRITE_JPEG_QUALITY), 50]}

if __name__ == "__main__":
    recorder = CV2AsynchronousVideoCapture().start()
    emitter = VideoStream(role=VideoStream.EMITTER,socket_ip="0.0.0.0",encoding_param=encoding_param).start()
    emitter.add_subscriber((consumer_ip, consumer_port))
    while recorder.read_frame() is None:
        pass
    while emitter.get_is_running() is False:
        pass
    print("start")
    for _ in range(1000):
        frame = recorder.read_frame()
        emitter.refresh_image(frame)
    recorder.stop()
    emitter.stop()
