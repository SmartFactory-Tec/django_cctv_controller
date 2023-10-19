import cv2
import threading


class Camera(object):
    """Class for capturing frames from a video source."""

    def __init__(self, url):
        """Initialize the Camera object.

        Args:
            url (str): The URL or path of the video source.
        """
        self._cap = cv2.VideoCapture(url)
        (self._ret, self._frame) = self._cap.read()
        threading.Thread(target=self._update, args=()).start()

    def __del__(self):
        """Release the video capture object when the instance is deleted."""
        self._cap.release()

    def get_fps(self):
        """Get the frames per second (FPS) of the video source.

        Returns:
            float: The FPS of the video source.
        """
        cap = self._cap
        return cap.get(cv2.CAP_PROP_FPS)

    def get_frame(self):
        """Get the current frame as a JPEG image.

        Returns:
            bytes: The JPEG encoded image of the current frame.
        """
        frame = self._frame
        ret = self._ret

        if ret:
            _, jpg = cv2.imencode(".jpg", frame)
            return jpg

    def _update(self):
        """Continuously update the current frame from the video source."""
        while True:
            (self._ret, self._frame) = self._cap.read()
