import asyncio
from channels.generic.websocket import AsyncWebsocketConsumer

from api.classes import Camera
from api.scripts.utility import getRTSPUrls, generateImagePacket

urls = [
    "http://pendelcam.kip.uni-heidelberg.de/mjpg/video.mjpg",
    "http://webcam.zvnoordwijk.nl:82/mjpg/video.mjpg",
    "http://camera.golfatlantide.com:8080/mjpg/video.mjpg?resolution=640x360&compression=12&fps=1&dummy=garb",
    "http://myrafjell.sodvin.no/mjpg/video.mjpg",
]


class VideoConsumer(AsyncWebsocketConsumer):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.camera_urls = kwargs.get("camera_urls")

    async def connect(self):
        await self.accept()
        camera_id = self.scope["url_route"]["kwargs"]["camera_id"]
        camera_id = int(camera_id)

        camera_urls = getRTSPUrls("api/data/cameras.json")

        self.camera = Camera(urls[camera_id])

        try:
            while True:
                # Asynchronous sleep to control the pace of the loop
                await asyncio.sleep(1 / 50)
                # Iterate through the camera IDs and corresponding camera objects

                # Generate data packet containing image-related information
                message = generateImagePacket(
                    frame=self.camera.get_frame(),
                    camera_id=camera_id,
                    fps=self.camera.get_fps(),
                )

                await self.send(message)
        except asyncio.CancelledError:
            pass
