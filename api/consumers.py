import asyncio
import cv2
import threading
import base64
from channels.generic.websocket import AsyncWebsocketConsumer


class VideoConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        await self.accept()

        urls = [
            "http://pendelcam.kip.uni-heidelberg.de/mjpg/video.mjpg",
            # "http://webcam.zvnoordwijk.nl:82/mjpg/video.mjpg",
            # "http://camera.golfatlantide.com:8080/mjpg/video.mjpg?resolution=640x360&compression=12&fps=1&dummy=garb",
            # "http://myrafjell.sodvin.no/mjpg/video.mjpg"
        ]

        self.cameras = [VideoCamera(url) for url in urls]
        camera_ids = range(len(self.cameras))

        try:
            while True:
                await asyncio.sleep(0.1)
                for camera_id, camera in zip(camera_ids, self.cameras):
                    frame = camera.get_frame()
                    jpg_as_text = base64.b64encode(frame)
                    message = f"{camera_id}:{jpg_as_text.decode()}"

                    await self.send(message)
        except asyncio.CancelledError:
            pass


class VideoCamera(object):
    def __init__(self, url):
        self.cap = cv2.VideoCapture(url)
        (self.ret, self.frame) = self.cap.read()
        threading.Thread(target=self.update, args=()).start()

    def __del__(self):
        self.cap.release()

    def get_fps(self):
        cap = self.cap
        return cap.get(cv2.CAP_PROP_FPS)

    def get_frame(self):
        frame = self.frame
        ret = self.ret
        cap = self.cap

        if ret:
            _, jpg = cv2.imencode(".jpg", frame)

            return jpg

    def update(self):
        while True:
            (self.ret, self.frame) = self.cap.read()
