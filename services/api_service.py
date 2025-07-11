import requests
from typing import Optional
from models import AudioData, AudioConfig
from utils import create_wav_buffer, validate_audio_data

class APIService:
    def __init__(self, server_url: str):
        self.server_url = server_url
    
    def _print_error(self, context: str, error: Exception) -> None:
        print(f"{context} error: {error}")
    
    async def send_audio_to_server(self, audio_data: AudioData, config: AudioConfig) -> Optional[bytes]:
        if not validate_audio_data(audio_data.data):
            self._print_error("Audio validation", ValueError("Invalid audio data"))
            return None
        
        try:
            wav_buffer = create_wav_buffer(audio_data.data, config)
            
            files = {"audio": ("audio.wav", wav_buffer, "audio/wav")}
            response = requests.post(f"{self.server_url}/process_audio", files=files)
            response.raise_for_status()
            
            return response.content
        except requests.exceptions.ConnectionError:
            print(f"Error: Cannot connect to server at {self.server_url}")
            return None
        except Exception as e:
            self._print_error("Server communication", e)
            return None
    
    def check_server_health(self) -> bool:
        try:
            response = requests.get(f"{self.server_url}/health")
            return response.status_code == 200
        except:
            return False
