from dotenv import load_dotenv
import os

load_dotenv()

# OBS
OBS_HOST = os.getenv("OBS_HOST", "127.0.0.1")
OBS_PORT = int(os.getenv("OBS_PORT", "4455"))
OBS_PASSWORD = os.getenv("OBS_PASSWORD", "")

# Audio
AUDIO_DEVICE_ID = int(os.getenv("AUDIO_DEVICE_ID", "13"))
THRESHOLD_DB = float(os.getenv("THRESHOLD_DB", "-19.0"))
PERSISTENCE_DURATION = float(os.getenv("PERSISTENCE_DURATION", "2.0"))

# Video
REPLAY_BUFFER_DURATION = float(os.getenv("REPLAY_BUFFER_DURATION", "300"))
REPLAY_BUFFER_PATH = os.getenv("REPLAY_BUFFER_PATH", "")
OUTPUT_PATH = os.getenv("OUTPUT_PATH", "")
POST_ROLL = float(os.getenv("POST_ROLL", "30"))