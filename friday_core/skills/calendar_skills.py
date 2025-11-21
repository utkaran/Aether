# calendar_skills.py
import datetime
import json
import os
import re
from pathlib import Path

class CalendarSkills:
    def __init__(self):
        self.calendar_file = "data/calendar.json"
        self._ensure_data_dir()
        self.events = self._load_events()
        
        # Словари для преобразования месяцев
        self.months = {
            'января': '01', 'февраля': '02', 'марта': '03',
            'апреля': '04', 'мая': '05', 'июня': '06', 
            'июля': '07', 'августа': '08', 'сентября': '09',
            'октября': '10', 'ноября': '11', 'декабря': '12',
            'январь': '01', 'февраль': '02', 'март': '03',
            'апрель': '04', 'май': '05', 'июнь': '06',
            'июль': '07', 'август': '08', 'сентябрь': '09',
            'октябрь': '10', 'ноябрь': '11', 'декабрь': '12'
        }
    
    def _ensure_data_dir(self):
        """Создает папку data если её нет"""
        Path("data").mkdir(exist_ok=True)
    
    def _load_events(self):
        """Загружает события из файла"""
        try:
            if os.path.exists(self.calendar_file):
                with open(self.calendar_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
            return []
        except Exception as e:
            print(f"❌ Ошибка загрузки календаря: {e}")
            return []
    
    def _save_events(self):
        """Сохраняет события в файл"""
        try:
            with open(self.calendar_file, 'w', encoding='utf-8') as f:
                json.dump(self.events, f, ensure_ascii=False, indent=2)
            return True
        except Exception as e:
            print(f"❌ Ошибка сохранения календаря: {e}")
            return False
    
    def _parse_russian_date(self, date_text):
        """Преобразует русскую дату в формат дд.мм.гггг"""
        try:
            # Убираем лишние слова
            clean_text = date_text.replace(' года', '').replace(' год', '').strip()
            
            # Ищем паттерн: число месяц год
            pattern = r'(\d{1,2})\s+([а-я]+)\s+(\d{4})'
            match = re.search(pattern, clean_text)
            
            if match:
                day = match.group(1)
                month_ru = match.group(2)
                year = match.group(3)
                
                # Преобразуем месяц
                month_num = self.months.get(month_ru.lower())
                if month_num:
                    return f"{day.zfill(2)}.{month_num}.{year}"
            
            return None
        except Exception as e:
            print(f"❌ Ошибка парсинга даты: {e}")
            return None
    
    def _extract_datetime_from_text(self, text):
        """Извлекает дату и время из текста команды"""
        try:
            # Пытаемся найти русскую дату
            date_pattern = r'(\d{1,2}\s+[а-я]+\s+\d{4}\s*(?:года)?)'
            date_match = re.search(date_pattern, text)
            
            if date_match:
                russian_date = date_match.group(1)
                date_str = self._parse_russian_date(russian_date)
                if date_str:
                    # Убираем дату из текста, чтобы получить название события
                    title = re.sub(date_pattern, '', text).strip()
                    
                    # Ищем время
                    time_match = re.search(r'(\d{1,2}:\d{2})', text)
                    time_str = time_match.group(1) if time_match else None
                    
                    # Если время не найдено, ищем просто число
                    if not time_str:
                        time_match = re.search(r'(\d{1,2})\s*(?:часов|час)?', text)
                        if time_match:
                            hour = time_match.group(1).zfill(2)
                            time_str = f"{hour}:00"
                    
                    return title, date_str, time_str
            
            # Если русская дата не найдена, ищем числовую дату
            numeric_date_match = re.search(r'(\d{1,2}\.\d{1,2}\.\d{4})', text)
            if numeric_date_match:
                date_str = numeric_date_match.group(1)
                title = re.sub(r'(\d{1,2}\.\d{1,2}\.\d{4})', '', text).strip()
                
                # Ищем время
                time_match = re.search(r'(\d{1,2}:\d{2})', text)
                time_str = time_match.group(1) if time_match else None
                
                return title, date_str, time_str
            
            return None, None, None
            
        except Exception as e:
            print(f"❌ Ошибка извлечения даты: {e}")
            return None, None, None
    
    def add_event(self, title, date_str=None, time_str=None, description=""):
        """Добавляет событие в календарь"""
        try:
            # Если date_str не передан, пытаемся извлечь из title
            if date_str is None:
                extracted_title, extracted_date, extracted_time = self._extract_datetime_from_text(title)
                if extracted_date:
                    title = extracted_title
                    date_str = extracted_date
                    time_str = extracted_time or time_str
            
            # Проверяем, что дата есть
            if not date_str:
                return "Не удалось распознать дату. Используйте: '25 декабря 2024' или '25.12.2024'"
            
            # Парсим дату
            if time_str:
                event_datetime = datetime.datetime.strptime(f"{date_str} {time_str}", "%d.%m.%Y %H:%M")
            else:
                event_datetime = datetime.datetime.strptime(date_str, "%d.%m.%Y")
                time_str = "00:00"
            
            event = {
                'id': len(self.events) + 1,
                'title': title,
                'date': date_str,
                'time': time_str,
                'datetime': event_datetime.isoformat(),
                'description': description,
                'created': datetime.datetime.now().isoformat()
            }
            
            self.events.append(event)
            self.events.sort(key=lambda x: x['datetime'])  # Сортируем по дате
            
            if self._save_events():
                time_text = f" в {time_str}" if time_str != "00:00" else ""
                return f"Событие '{title}' добавлено на {date_str}{time_text}"
            else:
                return "Ошибка сохранения события"
                
        except ValueError as e:
            return "Неверный формат даты. Используйте: '25 декабря 2024 15:30' или '25.12.2024 15:30'"
        except Exception as e:
            return f"Ошибка добавления события: {e}"
    
    def get_events(self, date_str=None):
        """Показывает события (все или на конкретную дату)"""
        if not self.events:
            return "В календаре нет событий"
        
        try:
            if date_str:
                # Фильтруем по дате
                filtered_events = [e for e in self.events if e['date'] == date_str]
                if not filtered_events:
                    return f"На {date_str} событий нет"
                
                result = f"📅 События на {date_str}:\n"
                for event in filtered_events:
                    time_display = f" в {event['time']}" if event['time'] != "00:00" else ""
                    result += f"• {event['title']}{time_display}"
                    if event['description']:
                        result += f" - {event['description']}"
                    result += "\n"
                return result.strip()
            
            else:
                # Показываем ближайшие 5 событий
                now = datetime.datetime.now()
                future_events = [e for e in self.events if datetime.datetime.fromisoformat(e['datetime']) > now]
                
                if not future_events:
                    return "Ближайших событий нет"
                
                result = "📅 Ближайшие события:\n"
                for event in future_events[:5]:
                    event_dt = datetime.datetime.fromisoformat(event['datetime'])
                    time_display = f" в {event['time']}" if event['time'] != "00:00" else ""
                    result += f"• {event_dt.strftime('%d.%m.%Y')}{time_display}: {event['title']}\n"
                return result.strip()
                
        except Exception as e:
            return f"Ошибка получения событий: {e}"
    
    def delete_event(self, event_id):
        """Удаляет событие по ID"""
        try:
            event_id = int(event_id)
            for i, event in enumerate(self.events):
                if event['id'] == event_id:
                    deleted_title = event['title']
                    del self.events[i]
                    if self._save_events():
                        return f"Событие '{deleted_title}' удалено"
                    else:
                        return "Ошибка сохранения изменений"
            return "Событие с таким ID не найдено"
        except ValueError:
            return "Неверный ID события"
        except Exception as e:
            return f"Ошибка удаления события: {e}"
    
    def get_today_events(self):
        """Показывает события на сегодня"""
        today = datetime.datetime.now().strftime("%d.%m.%Y")
        return self.get_events(today)

# Глобальный экземпляр
calendar_skills = CalendarSkills()