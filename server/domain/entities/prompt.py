"""Value Object - Prompt"""
from dataclasses import dataclass
@dataclass(frozen=True)
class Prompt:
    text: str
    negative_text: str = ""
    def __post_init__(self) -> None:
        if not self.text or not self.text.strip():
            raise ValueError("Prompt text cannot be empty")
        if len(self.text) > 1000:
            raise ValueError("Prompt text cannot exceed 1000 characters")
        object.__setattr__(self, "text", self.text.strip())