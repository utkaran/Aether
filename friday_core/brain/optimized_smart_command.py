#/friday_core/brain/optimized_smart_command.py

import time
import functools
from functools import lru_cache
from typing import Dict, Any
import threading
from friday_core.brain.command_handler import CommandHandler
import re
from friday_core.utills.logger import perfomance_logger

# optimized_smart_command.py - исправления
class OptimizedSmartCommand(CommandHandler):
  def __init__(self):
    super().__init__()
    self._response_cache = {}
    self._cache_lock = threading.Lock()  # Исправлено: Lock вместо RLock если не нужно рекурсивной блокировки
    self._cache_ttl = 300  # 5 минут
    self._cache_timestamps = {}

    self._volume_pattern = re.compile(r'громкость\s+на\s+(\d+)')
    self._weather_patterns = {
        'москва': re.compile(r'Москва'),
        'рязань': re.compile(r'Рязань')
    }

  @lru_cache(maxsize=500)
  def processes_command(self, command: str) -> str:  # Исправлено имя метода
    command_lower = command.lower().strip()
    replacements = {
        'пожалуйста': '', 'сделай': '', 'можешь': '',
        'скажи': '', 'покажи': '', 'включи': ''
    }

    for old, new in replacements.items():
      command_lower = command_lower.replace(old, new)
    return ''.join(command_lower.split())
    
  def get_cached_response(self, command: str) -> Any:
        # Исправлено: правильное использование блокировки
    with self._cache_lock:
      cache_key = self.processes_command(command)  # Исправлено имя метода
      if cache_key in self._response_cache:
        if time.time() - self._cache_timestamps.get(cache_key, 0) < self._cache_ttl:
          return self._response_cache[cache_key]
        else:
                    # Исправлено: правильное удаление из словаря
          del self._response_cache[cache_key]
          del self._cache_timestamps[cache_key]
      return None
    
  def set_cached_response(self, command: str, response: Any):
        # Безопасное сохранение в кэш
    with self._cache_lock:
      cache_key = self.processes_command(command)  # Исправлено имя метода
      self._response_cache[cache_key] = response
      self._cache_timestamps[cache_key] = time.time()

  def handle_command(self, command: str) -> str:
    start_time = time.time()
    try:
      cached_response = self.get_cached_response(command)
      if cached_response is not None:
        processing_time = time.time() - start_time
        perfomance_logger.log_command(command, processing_time, True)
        return cached_response
            
      response = super().handle_command(command)

      if not any(word in response.lower() for word in ['ошибка', 'не понял', 'текущ', 'сейчас']):
        self.set_cached_response(command, response)  # Исправлено имя метода
            
        processing_time = time.time() - start_time
        perfomance_logger.log_command(command, processing_time, True)

        return response
        
    except Exception as e:
      processing_time = time.time() - start_time
      perfomance_logger.error_count += 1
      perfomance_logger.log_command(command, processing_time, False)
      perfomance_logger.logger.error(f"Ошибка обработки команды: {e}")

      return "Извините, произошла внутренняя ошибка. Попробуйте позже."



