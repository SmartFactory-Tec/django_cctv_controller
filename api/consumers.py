import asyncio
from channels.generic.websocket import AsyncWebsocketConsumer

from api.classes import Camera
from api.scripts.utility import getRTSPUrls, generateImagePacket


class VideoConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        await self.accept()

        camera_urls = getRTSPUrls("api/data/cameras.json")

        print(camera_urls)

        urls = [
            "http://pendelcam.kip.uni-heidelberg.de/mjpg/video.mjpg",
            # "http://webcam.zvnoordwijk.nl:82/mjpg/video.mjpg",
            # "http://camera.golfatlantide.com:8080/mjpg/video.mjpg?resolution=640x360&compression=12&fps=1&dummy=garb",
            # "http://myrafjell.sodvin.no/mjpg/video.mjpg"
        ]

        self.cameras = [Camera(url) for url in urls]
        camera_ids = range(len(self.cameras))

        try:
            while True:
                # Asynchronous sleep to control the pace of the loop
                await asyncio.sleep(1 / 25)

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
