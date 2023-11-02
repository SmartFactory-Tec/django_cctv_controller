from channels.generic.websocket import WebsocketConsumer
from threading import Thread
from multiprocessing import shared_memory
import json
import time
import cv2
import numpy as np
import base64


class StreamConsumer(WebsocketConsumer):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._thread_active = True
        self._shm = None
        self._camera_id = None

    def connect(self):
        self.accept()

        self._camera_id = self.scope["url_route"]["kwargs"]["camera_id"]
        self._camera_id = int(self._camera_id)

        t = Thread(target=self.send_frames)
        t.start()

    def close_memory(self):
        if self._shm:
            self._shm.close()
            self._shm.unlink()

    def send_frames(self):
        try:
            while self._thread_active:
                time.sleep(1 / 50)

                self._shm = shared_memory.SharedMemory(
                    name=f"camera_{self._camera_id}_stream"
                )

                frame = np.ndarray((480, 720, 3), dtype=np.uint8, buffer=self._shm.buf)

                if self._shm.size > 0:
                    if frame is not None:
                        _, jpg = cv2.imencode(".jpg", frame)

                        packet = {
                            "camera_id": self._camera_id,
                            "frame": base64.b64encode(jpg).decode(),
                            "fps": "Unknown",
                        }

                        self.send(json.dumps(packet))
                else:
                    self._thread_active = False

        except Exception as e:
            print(f"[EXCEPTION] An error occurred: {e}")

        finally:
            self.close_memory()

    def disconnect(self, close_code):
        self.close_memory()
