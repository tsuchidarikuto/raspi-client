from dataclasses import dataclass

@dataclass
class AudioData:
    data: bytes
    sample_rate: int
    duration: float
    
    @property
    def size(self) -> int:
        return len(self.data)

@dataclass
class AudioConfig:
    sample_rate: int
    chunk_size: int
    channels: int = 1
    format_type: str = "wav"

@dataclass
class VoiceActivityConfig:
    threshold: float
    silence_duration: float
    min_recording_duration: float = 0.5
