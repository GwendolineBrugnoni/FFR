import socket

from hermes.stream.VideoStream import VideoStream
import cv2
import datetime
from hermes.network.AsyncUDPChannel import AsyncUDPChannel

def get_ip():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.settimeout(0)
    try:
        # doesn't even have to be reachable
        s.connect(('10.255.255.255', 1))
        IP = s.getsockname()[0]
    except Exception:
        IP = '127.0.0.1'
    finally:
        s.close()
    return IP


# consumer_ip = "192.168.50.146"
consumer_ip = get_ip()
print(consumer_ip)
consumer_video_port = "5001"

server_port = 8000
server_ip = "192.168.50.1"
# server_ip = "127.0.0.1"

max_time_between_pings = 5


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

if __name__ == "__main__":
    client = AsyncUDPChannel(socket_ip=consumer_ip,
                             socket_port=5000).start()
    cv2.namedWindow("preview")
    consumer = VideoStream(role=VideoStream.CONSUMER,
                           socket_ip=consumer_ip,
                           socket_port=int(consumer_video_port),
                           use_rcv_img_buffer=False,
                           max_queue_size=10000).start()

    while consumer.get_is_running() is False:
        pass

    # Connection to server
    print("Connection request")
    client.sendto(bytes(consumer_video_port, 'utf8'), (server_ip, server_port))
    last_ping = datetime.datetime.now()

    while True:
        # Ping server
        if (
                datetime.datetime.now() - last_ping).seconds > max_time_between_pings:
            print("Refresh connection")
            client.sendto(bytes(consumer_video_port, 'utf8'),
                          (server_ip, server_port))
            last_ping = datetime.datetime.now()

        new_frame = consumer.get_rcv_img()

        if new_frame is not None:
            # traitement ici
            reconnaissance_faciale(new_frame)
            cv2.imshow("preview", new_frame)

        key = cv2.waitKey(20)
        if key == 27:  # exit on ESC
            break

    cv2.destroyWindow("preview")
    consumer.stop()
    client.stop()