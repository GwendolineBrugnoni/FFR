"""Example of video streaming consumer.
This script receive the video stream of a VideoStream emitter and will display it in a new window.
The emitter of this script can be the script video_stream_emitter.py
Press ESC to quit the example while running.
"""

from hermes.stream.VideoStream import VideoStream
import cv2
import datetime

consumer_ip = "0.0.0.0"
consumer_port = 5001

if __name__ == "__main__":
    cv2.namedWindow("preview")
    consumer = VideoStream(role=VideoStream.CONSUMER, socket_ip=consumer_ip,
                           socket_port=consumer_port).start()
    while consumer.get_is_running() is False:
        pass
    while True:
        new_frame = consumer.get_rcv_img()
        if new_frame is not None:
            #traitement ici
            cv2.imshow("preview", new_frame)


        key = cv2.waitKey(20)
        if key == 27:  # exit on ESC
            break
    cv2.destroyWindow("preview")
    consumer.stop()