from vidstream import AudioSender
from vidstream import AudioReceiver
import time
import threading

Sender=AudioSender('192.168.36.178',6669)
Sender_thread= threading.Thread(target=Sender.start_stream)

receiver=AudioReceiver('192.168.36.22',6669)
receiver_thread= threading.Thread(target=receiver.start_server())

receiver_thread.start()

time.sleep(4)

Sender_thread.start()