import asyncio
import cv2
import threading
from channels.generic.websocket import AsyncWebsocketConsumer

from .scripts.utility import getRTSPUrls, generateImagePacket


class VideoConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        await self.accept()

        camera_urls = getRTSPUrls("api/data/cameras.json")

        print(camera_urls)

        urls = [
            "http://pendelcam.kip.uni-heidelberg.de/mjpg/video.mjpg",
        ]

        self.cameras = [VideoCamera(url) for url in urls]
        camera_ids = range(len(self.cameras))

        try:
            while True:
                # Asynchronous sleep to control the pace of the loop
                await asyncio.sleep(0.1)

                # Iterate through the camera IDs and corresponding camera objects
                for camera_id, camera in zip(camera_ids, self.cameras):
                    # Generate data packet containing image-related information
                    message = generateImagePacket(
                        frame=camera.get_frame(),
                        camera_id=camera_id,
                        fps=camera.get_fps(),
                    )

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
