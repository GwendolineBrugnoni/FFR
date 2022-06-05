from hermes.stream.VideoStream import VideoStream
import cv2
import datetime
from hermes.network.AsyncUDPChannel import AsyncUDPChannel
import socket

# Permet de récupérer l'ip et ne pas changer le fichier à chaque
# fois que l'on change d'ip
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


consumer_ip = get_ip()
consumer_video_port = "5001"

# La raspberry pi à été configurer pour ne jamais changer d'ip dans notre cas
server_port = 8000
server_ip = "192.168.50.1"

max_time_between_pings = 5

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
            cv2.imshow("preview", new_frame)

        key = cv2.waitKey(20)
        if key == 27:  # exit on ESC
            break

    cv2.destroyWindow("preview")
    consumer.stop()
    client.stop()
