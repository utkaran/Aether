from abc import ABC, abstractmethod
from typing import Protocol

class IAutomationSkills(Protocol):
  @abstractmethod
  def take_screenshot(self, area: bool = False, description: str = '') -> str:
    pass

  @abstractmethod
  def take_multiple_screenshots(self, count: int=3) -> str:
    pass

  @abstractmethod
  def open_screenshot_folder(self) -> str:
    pass

  @abstractmethod
  def list_recent_screenshots(self, count: int=5) -> str:
    pass

  @abstractmethod
  def get_screenshot_stats(self) -> str:
    pass

  @abstractmethod
  def cleanup_old_screenshots(self, days: int=30) -> str:
    pass

  @abstractmethod
  def open_application(self, app_name: str) -> str:
    pass

  @abstractmethod
  def close_application(self, app_name: str) -> str:
    pass

  @abstractmethod
  def get_system_resources(self) -> str:
    pass

  @abstractmethod
  def window_management(self, action: str) -> str:
    pass