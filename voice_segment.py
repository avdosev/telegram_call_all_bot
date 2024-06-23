from dataclasses import dataclass
from typing import Optional

@dataclass
class VoiceSegment:
    start_time: float  # in seconds
    end_time: float  # in seconds
    text: str