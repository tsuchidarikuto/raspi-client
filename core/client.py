import asyncio
from typing import Optional
from core.config import config
from models import AudioConfig, VoiceActivityConfig
from services import AudioService, APIService

class VoiceClient:
    def __init__(self, server_url: Optional[str] = None):
        self.server_url = server_url or config.default_server_url
        
        self.audio_config = AudioConfig(
            sample_rate=config.sample_rate,
            chunk_size=config.chunk_size
        )
        
        self.vad_config = VoiceActivityConfig(
            threshold=config.threshold,
            silence_duration=config.silence_duration
        )
        
        self.audio_service = AudioService(self.audio_config, self.vad_config)
        self.api_service = APIService(self.server_url)
    
    async def run_conversation(self) -> None:
        print(f"Voice Client started (Server: {self.server_url})")
        print("Press Ctrl+C to exit")
        
        if not self.api_service.check_server_health():
            print(f"Warning: Server at {self.server_url} may not be responding")
        
        try:
            while True:
                audio_data = await self.audio_service.record_audio_with_vad()
                if not audio_data:
                    continue
                
                print("Sending audio to server...")
                
                response_audio = await self.api_service.send_audio_to_server(
                    audio_data, self.audio_config
                )
                if not response_audio:
                    print("Could not get response from server")
                    continue
                
                print("Playing response...")
                self.audio_service.play_audio(response_audio)
                
        except KeyboardInterrupt:
            pass
        finally:
            print("\nShutting down...")            
            self.audio_service.cleanup()
