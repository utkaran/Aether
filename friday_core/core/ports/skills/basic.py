from abc import ABC, abstractmethod
from typing import Protocol

class IBasicSkills(Protocol):
  @abstractmethod
  def get_time(self) -> str:
    pass

  @abstractmethod
  def get_date(self) -> str:
    pass

  @abstractmethod
  def open_browser(self, browser: str='default') -> str:
    pass

  @abstractmethod
  def close_browser(self, browser: str='all') -> str:
    pass

  @abstractmethod
  def search_web(self, query: str) -> str:
    pass

  @abstractmethod
  def create_note(self, text: str) -> str:
    pass