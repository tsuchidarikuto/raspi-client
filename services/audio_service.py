import asyncio
import subprocess
import tempfile
import os
import pyaudio
from typing import Optional
from models import AudioData, AudioConfig, VoiceActivityConfig
from utils import calculate_audio_energy, validate_audio_data

class AudioService:
    def __init__(self, audio_config: AudioConfig, vad_config: VoiceActivityConfig):
        self.audio_config = audio_config
        self.vad_config = vad_config
        self.audio = pyaudio.PyAudio()
        self.format = pyaudio.paInt16
    
    def _print_error(self, context: str, error: Exception) -> None:
        print(f"{context} error: {error}")
    
    async def record_audio_with_vad(self) -> Optional[AudioData]:
        stream = self.audio.open(
            format=self.format,
            channels=self.audio_config.channels,
            rate=self.audio_config.sample_rate,
            input=True,
            frames_per_buffer=self.audio_config.chunk_size
        )
        
        frames = []
        is_speaking = False
        silence_chunks = 0
        silence_threshold = int(
            self.vad_config.silence_duration * self.audio_config.sample_rate / self.audio_config.chunk_size
        )
        
        print("Listening... (speak to start recording)")
        
        try:
            while True:
                data = stream.read(self.audio_config.chunk_size, exception_on_overflow=False)
                energy = calculate_audio_energy(data)
                
                if energy > self.vad_config.threshold:
                    if not is_speaking:
                        print("Recording started...")
                        is_speaking = True
                    frames.append(data)
                    silence_chunks = 0
                elif is_speaking:
                    frames.append(data)
                    silence_chunks += 1
                    if silence_chunks > silence_threshold:
                        print("Recording stopped.")
                        break
                
                await asyncio.sleep(0.001)
                
        except KeyboardInterrupt:
            return None
        finally:
            stream.close()
        
        if not frames:
            return None
        
        audio_data = b''.join(frames)
        duration = len(frames) * self.audio_config.chunk_size / self.audio_config.sample_rate
        
        return AudioData(
            data=audio_data,
            sample_rate=self.audio_config.sample_rate,
            duration=duration
        )
    
    def play_audio(self, audio_data: bytes) -> None:
        try:
            with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as temp_file:
                temp_file.write(audio_data)
                temp_path = temp_file.name
            
            # Use aplay for Raspberry Pi / Linux
            subprocess.run(["aplay", temp_path], check=True)
            os.unlink(temp_path)
        except Exception as e:
            self._print_error("Audio playback", e)
    
    def cleanup(self) -> None:
        if hasattr(self, 'audio'):
            self.audio.terminate()
