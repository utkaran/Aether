from abc import ABC, abstractmethod
from typing import Protocol, Optional
from dataclasses import dataclass
import time

@dataclass
class CommandContext:
  original_command: str
  user_id: Optional[str] = None
  session_id: Optional[str] = None
  timestamp: float = 0.0

class CommandProcessor(Protocol):
  @abstractmethod
  def can_handle(self, command: str) -> bool:
    pass

  @abstractmethod
  def process(self, command: str, context: CommandContext) -> str:
    pass

class CachedCommandProcessor(CommandProcessor):
  def __init__(self, cache_provider=None):
    self.cache_provider = cache_provider

  def process_with_cache(self, command: str, context: CommandContext) -> str:
    if self.cache_provider:
      cached = self.cache_provider.get(command)
      if cached is not None:
        return cached
      
    result = self.process(command, context)

    if self.cache_provider and result:
      self.cache_provider.set(command, result)

    return result
