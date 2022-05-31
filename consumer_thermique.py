"""Example of video streaming consumer.
This script receive the video stream of a VideoStream emitter and will display it in a new window.
The emitter of this script can be the script video_stream_emitter.py
Press ESC to quit the example while running.
"""

from hermes.stream.VideoStream import VideoStream
import cv2
import datetime

consumer_ip = "127.0.0.1"
consumer_port = 5000

def traitement_thermique(img):
    img_largeur = img.shape[0]
    img_hauteur = img.shape[1]

    for i in range(img_largeur):
        for j in range(img_hauteur):
            if (img[i][j][0] > 150):
                img[i][j][0], img[i][j][1], img[i][j][2] = 0, 0, 0

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
            image = traitement_thermique(new_frame)
            cv2.imshow("preview", new_frame)

        key = cv2.waitKey(20)
        if key == 27:  # exit on ESC
            break
    cv2.destroyWindow("preview")
    consumer.stop()