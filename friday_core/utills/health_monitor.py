import psutil
import gc
import threading
import time
from dataclasses import dataclass
from typing import Dict, List
from friday_core.utills.logger import perfomance_logger
from friday_core.brain.optimized_smart_command import OptimizedSmartCommand

@dataclass
class SystemHealth:
  cpu_recent: float
  memory_percent: float
  active_threads: int
  command_queue_size: int
  cache_hit_rate: float


class HealthMonitor:
  def __init__(self, command_handler):
    self.command_handler = command_handler
    self.health_stats: List[SystemHealth] = []
    self.monitoring = False
    self.monitor_thread = None

    self.warning_thresholds = {
      'cpu': 80.0,
      'memory': 85.0,
      'threads': 50
    }

  def start_monitoring(self):
    self.monitoring = True
    self.monitor_thread = threading.Thread(target=self._monitor_loop, daemon=True)
    self.monitor_thread.start()

  def _monitor_loop(self):
    while self.monitoring:
      try:
        health = self._check_health()
        self.health_stats.append(health)
        
        # сохраненяем только последние 100 записей
        if len(self.health_stats) > 100:
          self.health_stats = self.health_stats[-50:]

        # проверяем пороги

        self._check_thresholds(health)

        if len(self.health_stats) % 10 == 0:
          gc.collect()

      except Exception as e:
        perfomance_logger.error(f"Ошибка в мониторинге: {e}")

      time.sleep(30) # 30 секунд


  def _check_health(self) -> SystemHealth:
    process = psutil.Process()

    cache_hits = 0
    cache_misses = 0
    if hasattr(self.command_handler, '_response_cache'):
      cache_size = len(self.command_handler._response_cache)

    return SystemHealth(
      cpu_recent=psutil.cpu_percent(),
      memory_percent=process.memory_percent(),
      active_threads=threading.active_count(),
      command_queue_size=0,
      cache_hit_rate=cache_hits / max((cache_hits + cache_misses), 1)
    )
  
  def _check_thresholds(self, health: SystemHealth):
    warnings = []

    if health.cpu_recent > self.warning_thresholds['cpu']:
      warnings.append(f"Высокая загрузка ЦП: {health.cpu_recent}%")

    if health.memory_percent > self.warning_thresholds['memory']:
      warnings.append(f"Высокая память: {health.memory_percent}%")
      self._clear_cache()

    if health.active_threads > self.warning_thresholds['threads']:
      warnings.append(f"Слишком много активных потоков: {health.active_threads}")

    for warning in warnings:
      perfomance_logger.logger.warning(warning)

  def _clear_cache(self):
    if hasattr(self.command_handler, '_response_cache'):
      with self.command_handler.cache_lock():
        self.command_handler._response_cache.clear()
        self.command_handler._cache_timestamps.clear()
      self.command_handler._preprocessed_commands.cache_clear()

    perfomance_logger.logger.info('Кэш очищен')

  def get_health_report(self) -> Dict:
    if not self.health_stats:
        return {"status": "No data available"}
    
    current = self.health_stats[-1]
    avg_cpu = sum(h.cpu_percent for h in self.health_stats) / len(self.health_stats)
    
    return {
        "status": "HEALTHY" if current.cpu_percent < 80 and current.memory_percent < 85 else "WARNING",
        "current_cpu": current.cpu_percent,
        "current_memory": current.memory_percent,
        "average_cpu": avg_cpu,
        "active_threads": current.active_threads,
        "cache_hit_rate": current.cache_hit_rate,
        "monitoring_duration": len(self.health_stats)
    }
