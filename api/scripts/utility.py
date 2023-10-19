import json
import base64


def getRTSPUrls(route):
    """
    Generates RTSP URLs based on IP Camera documentation and credentials

    :param route: Route to .json file with camera data
    :returns: RTSP URLs
    """
    camera_file = open(route)
    data = json.load(camera_file)["data"]

    urls = []

    for camera in data:
        mac = camera["mac"]
        ip = camera["ip"]
        pwd = camera["pwd"]

        urls.append(f"rtsp://admin:{pwd}@{ip}:554/cam/realmonitor?channel=1&subtype=1")

    camera_file.close()

    return urls


def generateImagePacket(*, frame, camera_id, resolution=None, timestamp=None, fps=None):
    """
    Generates an image packet as a JSON string.

    :param frame: The image data to be encoded and included in the packet.
    :type frame: bytes

    :param camera_id: Identifier for the camera.
    :type camera_id: str

    :param resolution: (Optional) The resolution of the image.
    :type resolution: str or None

    :param timestamp: (Optional) The timestamp of when the image was captured.
    :type timestamp: str or None

    :param fps: (Optional) Frames per second of the video capture.
    : type fps: float or None

    :return: A JSON string containing the image packet information.
    :rtype: str
    """
    packet = {
        "camera_id": camera_id,
        "frame": base64.b64encode(frame).decode(),
    }

    if timestamp is not None:
        packet["timestamp"] = timestamp
    if resolution is not None:
        packet["resolution"] = resolution
    if fps is not None:
        packet["fps"] = fps

    return json.dumps(packet)
