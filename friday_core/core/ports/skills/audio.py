from abc import ABC, abstractmethod
from typing import Protocol

class IAudioSkills(Protocol):
  @abstractmethod
  def set_volume(self, level: int) -> str:
    pass

  @abstractmethod
  def volume_up(self) -> str:
    pass

  @abstractmethod
  def volume_down(self) -> str:
    pass

  @abstractmethod
  def mute(self) -> str:
    pass
