"""Example of video streaming consumer.
This script receive the video stream of a VideoStream emitter and will display it in a new window.
The emitter of this script can be the script video_stream_emitter.py
Press ESC to quit the example while running.
"""

from hermes.stream.VideoStream import VideoStream
import cv2
import imutils
import datetime

consumer_ip = "127.0.0.1"
consumer_port = 5000

def reconnaissance_faciale(image):
    cascadefile = "haarcascade_frontalface_alt.xml"
    classCascade = cv2.CascadeClassifier(cascadefile)
    # Echelle de gris
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    # Reconnaissance faciale
    faces = classCascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30),
                                          flags=cv2.CASCADE_SCALE_IMAGE)
    # Dessine des rectangles autour des visages trouvés
    for (x, y, w, h) in faces:
        cv2.rectangle(image, (x, y), (x + w, y + h), (255, 0, 0), 2)

def reconnaissance_forme(image1):

    hog = cv2.HOGDescriptor()
    hog.setSVMDetector(cv2.HOGDescriptor_getDefaultPeopleDetector())

    # Reading the Image

    # Resizing the Image
    image1 = imutils.resize(image1,
                            width=min(500, image1.shape[1]))

    # Detecting all humans
    (humans, _) = hog.detectMultiScale(image1,
                                       winStride=(5, 5),
                                       padding=(3, 3),
                                       scale=1.21)

    # Drawing the rectangle regions
    for (x, y, w, h) in humans:
        cv2.rectangle(image1, (x, y),
                      (x + w, y + h),
                      (0, 0, 255), 2)
    return image1
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
            image1 = reconnaissance_forme(new_frame)
            reconnaissance_faciale(image1)
            cv2.imshow("preview", image1)

        key = cv2.waitKey(20)
        if key == 27:  # exit on ESC
            break
    cv2.destroyWindow("preview")
    consumer.stop()