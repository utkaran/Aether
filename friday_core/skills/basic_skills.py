# friday_core/skills/basic_skills.py

import datetime
import webbrowser
import os

class BasicSkills:
    @staticmethod
    def get_time():
        """Возвращает текущее время"""
        now = datetime.datetime.now()
        return f"Сейчас {now.hour} часов {now.minute} минут"
    
    @staticmethod
    def get_date():
        """Возвращает текущую дату"""
        today = datetime.datetime.now()
        months = {
            1: "января", 2: "февраля", 3: "марта", 4: "апреля",
            5: "мая", 6: "июня", 7: "июля", 8: "августа",
            9: "сентября", 10: "октября", 11: "ноября", 12: "декабря"
        }
        return f"Сегодня {today.day} {months[today.month]} {today.year} года"
    
    @staticmethod
    def open_browser(browser_name=None, url='https://google.com'):
        try:
            if browser_name == 'chrome':
                os.system(f'start chrome "{url}"')
                return "Открываю Chrome"
            elif browser_name == 'firefox':
                os.system(f'start firefox "{url}"')
                return "Открываю Firefox"
            elif browser_name == 'edge':
                os.system(f'start msedge "{url}"')
                return "Открываю Edge"
            elif browser_name == 'opera':
                os.system(f'start opera "{url}"')
                return "Открываю Opera"
            elif browser_name == 'Yandex':
                # ПРАВИЛЬНАЯ команда для Яндекс.Браузера
                os.system(f'start browser "{url}"')
                return "Открываю Яндекс.Браузер"
            else:
                # Системный браузер по умолчанию
                webbrowser.open(url)
                return "Открываю браузер"
        except Exception as e:
            webbrowser.open(url)
            return "Открываю браузер"
        
    
    @staticmethod
    def search_web(query):
        """Выполняет поиск в интернете"""
        search_url = f"https://www.google.com/search?q={query}"
        webbrowser.open(search_url)
        return f"Ищу информацию по запросу: {query}"
    
    @staticmethod
    def create_note(note_text):
        """Создает текстовую заметку"""
        try:
            with open("notes.txt", "a", encoding="utf-8") as file:
                timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
                file.write(f"{timestamp}: {note_text}\n")
            return "Заметка сохранена"
        except Exception as e:
            return f"Ошибка при сохранении заметки: {e}"
        
    @staticmethod
    def close_browser(browser_name=None):
        browsers = {
            'chrome': ['chrome.exe'],
            'firefox': ['firefox.exe'],
            'edge': ['msedge.exe'],
            'opera': ['opera.exe'],
            'yandex': ['browser.exe'],
            'яндекс': ['browser.exe']
        }
        closed = False
        target_browser = browser_name.lower() if browser_name else 'браузер'
        
        if target_browser in browsers:
            for process_name in browsers[target_browser]:
                try:
                    os.system(f'taskkill /f /im {process_name} >nul 2>&1')
                    closed = True
                except:
                    continue

        return closed
    

        