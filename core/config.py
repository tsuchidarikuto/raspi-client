import os

class ClientConfig:
    def __init__(self):
        self.sample_rate = 16000
        self.chunk_size = 1024
        self.threshold = 500
        self.silence_duration = 1.0
        self.default_server_url = os.getenv("SERVER_URL", "http://localhost:8000")
        self.audio_format = "wav"
        self.notification_enabled = True

config = ClientConfig()
