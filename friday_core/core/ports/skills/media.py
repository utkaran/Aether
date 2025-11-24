from abc import ABC, abstractmethod
from typing import Protocol

class IMediaSkills(Protocol):
  @abstractmethod
  def play_hitmo(self) -> str:
    pass

  @abstractmethod
  def play_on_youtube(self, query: str='') -> str:
    pass

  @abstractmethod
  def pause_media(self) -> str:
    pass

  @abstractmethod
  def play_media(self) -> str:
    pass

  @abstractmethod
  def next_track(self) -> str:
    pass

  @abstractmethod
  def prev_track(self) -> str:
    pass