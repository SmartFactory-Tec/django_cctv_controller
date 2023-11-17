import os
import platform


## TODO Change path according to environment
def get_base_directory():
    try:
        # Check if the WSL_DISTRO_NAME environment variable is present
        if "WSL2_GUI_APPS_ENABLED" in os.environ:
            # If it is, assume it's WSL 2
            return os.path.join("/mnt/c/", "django-cctv-controller")
        else:
            # Otherwise, it's a native Windows or Linux environment
            return os.path.join("C:", "django-cctv-controller")
    except Exception as e:
        print(f"An error occurred: {e}")
        return None


base_directory = os.path.join("/mnt/c/", "django-cctv-controller")
os.makedirs(base_directory, exist_ok=True)


class Config:
    # Width of the video frame
    FRAME_WIDTH = 854

    # Height of the video frame
    FRAME_HEIGHT = 480

    # Size of the video frame in bytes (width * height * 3 channels for RGB)
    FRAME_SIZE_BYTES = FRAME_HEIGHT * FRAME_WIDTH * 3

    # Interval for video segmentation
    VIDEO_SEGMENTATION_INTERVAL = 10

    # Interval for processing segmentation
    PROCESSING_SEGMENTATION_INTERVAL = 0.2

    # Boxes confidence threshold
    BOX_CONFIDENCE_THRESHOLD = 0.75

    # URL for accessing camera API
    CAMERA_API_URL = f"http://localhost:8000/api/cameras/"

    # URL for accessing camera API
    USERS_API_URL = f"http://localhost:8000/api/people/"

    # Path for the recognition database
    RECOGNITION_DB_PATH = os.path.join(base_directory, "data", "db")

    # Base directory for storing video data
    VIDEO_STORAGE_PATH = os.path.join(base_directory, "cctv_footage")
