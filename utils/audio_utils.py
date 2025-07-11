import io
import wave
import numpy as np
from typing import Optional
from models import AudioConfig

def calculate_audio_energy(audio_data: bytes) -> float:
    audio_np = np.frombuffer(audio_data, dtype=np.int16)
    return float(np.abs(audio_np).mean()) if len(audio_np) > 0 else 0.0

def create_wav_buffer(audio_data: bytes, config: AudioConfig) -> io.BytesIO:
    buffer = io.BytesIO()
    with wave.open(buffer, 'wb') as wf:
        wf.setnchannels(config.channels)
        wf.setsampwidth(2)
        wf.setframerate(config.sample_rate)
        wf.writeframes(audio_data)
    
    buffer.seek(0)
    return buffer

def validate_audio_data(audio_data: Optional[bytes]) -> bool:
    return audio_data is not None and len(audio_data) > 0
