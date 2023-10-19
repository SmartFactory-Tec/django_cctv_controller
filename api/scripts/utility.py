import json
import base64


def getRTSPUrls(route):
    """
    Generates RTSP URLs based on the IP Camera documentation and credentials.

    This function takes in the route to a .json file containing camera data. It reads the file, extracts the necessary information such as MAC address, IP address, and password for each camera, and generates RTSP URLs based on the provided data.

    Args:
        route (str): Route to the .json file with camera data.

    Returns:
        list: A list of RTSP URLs generated based on the camera data.
    """
    # Open the .json file containing camera data
    camera_file = open(route)

    # Load the camera data from the .json file
    data = json.load(camera_file)["data"]

    urls = []

    # Iterate through each camera's data and create the corresponding RTSP URL
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
