# event_bus.py
import json
import time
from typing import Dict, List, Callable, Any
from enum import Enum

class EventType(Enum):
    COMMAND_RECEIVED = "command_received"
    INTENT_CLASSIFIED = "intent_classified" 
    COMMAND_EXECUTED = "command_executed"
    RESPONSE_READY = "response_ready"
    ERROR_OCCURRED = "error_occurred"
    SESSION_STARTED = "session_started"
    SESSION_ENDED = "session_ended"

class EventBus:
    def __init__(self):
        self._subscribers: Dict[EventType, List[Callable]] = {
            event_type: [] for event_type in EventType
        }
        self._event_history = []
        print("Event Bus: Инициализирован")
    
    def subscribe(self, event_type: EventType, callback: Callable):
        """Подписка на тип событий"""
        if event_type not in self._subscribers:
            self._subscribers[event_type] = []
        self._subscribers[event_type].append(callback)
        print(f'EventBus: Подписка на {event_type}')
    
    def publish(self, event_type: EventType, data: Dict[str, Any] = None):
        #Публикация события

        event = {
            'type': event_type.value,
            'timestamp': time.time(),
            'data': data or {}
        }

        self._event_history.append(event)

        if len(self._event_history) > 1000:
            self._event_history = self._event_history[-500:]

        for callback in self._subscribers.get(event_type, []):
            try:
                callback(event)
            except Exception as e:
                print(f"Event Bus: Ошибка в обработчике {event_type}: {e}")
        print(f"Event Bus: Опубликовано {event_type}")

    def get_stats(self):
        stats = {}
        for event_type in EventType:
            count = sum(1 for e in self._event_history if e['type'] == event_type.value)
            stats[event_type.value] = count
        return stats
    
event_bus = EventBus()