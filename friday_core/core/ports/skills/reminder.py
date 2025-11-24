from abc import ABC, abstractmethod
from typing import Protocol

class IReminderSkills(Protocol):
  @abstractmethod
  def set_reminer(self, text:str, minutes: int) -> str:
    pass

  @abstractmethod
  def set_timer(self, minutes: int) -> str:
    pass

  @abstractmethod
  def get_reminders(self) -> str:
    pass

  @abstractmethod
  def cancel_reminders(self, reminder_id: str) -> str:
    pass
    
    