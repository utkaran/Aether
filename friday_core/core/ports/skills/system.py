from abc import ABC, abstractmethod
from typing import Protocol

class ISystemSkills(Protocol):
  @abstractmethod
  def shutdown(self, seconds: int) -> str:
    pass

  @abstractmethod
  def restart(self, secconds: int) -> str:
    pass

  @abstractmethod
  def cancel_shutdown(self) -> str:
    pass