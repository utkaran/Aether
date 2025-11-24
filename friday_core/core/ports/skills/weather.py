from abc import ABC, abstractmethod
from typing import Protocol

class IWeatherSkills(Protocol):
  @abstractmethod
  def get_weather(self, city: str='') -> str:
    pass

  @abstractmethod
  def get_weather_by_location(self) -> str:
    pass

  @abstractmethod
  def get_weather_for_display(self, city: str='') -> str:
    pass

  @abstractmethod
  def get_forecast(self, city: str='', days: int=3) -> str:
    pass