# test_event_subscribers.py
from friday_core.utills.event_bus import event_bus, EventType

class TestEventSubscribers:
    def __init__(self):
        self._setup_subscriptions()
    
    def _setup_subscriptions(self):
        """Подписка для тестирования шины"""
        event_bus.subscribe(EventType.COMMAND_RECEIVED, self._on_command_received)
        event_bus.subscribe(EventType.COMMAND_EXECUTED, self._on_command_executed)
    
    def _on_command_received(self, event):
        """Просто логируем - не мешаем основной работе"""
        print(f"🎯 Event Bus: Получена команда '{event['data']['command']}'")
    
    def _on_command_executed(self, event):
        """Анализируем успешность выполнения"""
        data = event['data']
        status = "✅ Успех" if data["success"] else "❌ Ошибка"
        print(f"🎯 Event Bus: Команда '{data['command']}' -> {status}")

# Создаем при старте (не мешает работе)
test_subscribers = TestEventSubscribers()