# friday_core/engine/voice_engine.py

import speech_recognition as sr
import re
import time
from friday_core.engine.sound_manager import sound_manager
from friday_core.config.config import config
import threading

class VoiceEngine:
    def __init__(self):
        print("🔧 Инициализация голосового движка...")
        
        # 🔥 ИСПРАВЛЕНИЕ: Прямая инициализация без свойств
        self._recognizer = None
        self._microphone = None
        self._tts_engine = None
        self._recognizer_initialized = False
        self._tts_initialized = False
        
        self.wake_words = config.get('assistant.wake_words', ['пятница'])
        self.language = config.get('assistant.language', 'ru-RU')
        
        # Активная сессия
        self.active_session = False
        self.session_timeout = 20
        self.last_command_time = 0
        self.session_timer = None

        self._init_recognizer()
        
        print("✅ Голосовой движок готов")

    def _init_recognizer(self):
        """Инициализация распознавателя (только когда нужен)"""
        if not self._recognizer_initialized:
            print("🔧 Инициализация распознавателя речи...")
            self._recognizer = sr.Recognizer()
            self._microphone = sr.Microphone()
            self._calibrate_microphone()
            self._recognizer_initialized = True

    def _init_tts(self):
        """Инициализация TTS (только когда нужен)"""
        if not self._tts_initialized:
            print("🔧 Инициализация TTS движка...")
            try:
                from friday_core.engine.ffplay_tts import FFplayTTS
                self._tts_engine = FFplayTTS()
                
                # Принудительно устанавливаем голос из конфига
                config_voice = config.get('voice.edge_voice', 'ru-RU-SvetlanaNeural')
                self._tts_engine.set_voice(config_voice)
                print(f"✅ TTS движок готов. Голос: {config_voice}")
                self._tts_initialized = True
                
            except ImportError as e:
                print(f"❌ FFplayTTS не доступен: {e}")
                self._tts_engine = None

    def _calibrate_microphone(self):
        """Калибровка микрофона"""
        print("🔧 Калибровка микрофона...")
        try:
            with self._microphone as source:
                self._recognizer.adjust_for_ambient_noise(source, duration=2)
                self._recognizer.energy_threshold = 300
            print("✅ Микрофон откалиброван")
        except Exception as e:
            print(f"❌ Ошибка калибровки: {e}")

    def _remove_emojis(self, text):
        """Быстрая очистка текста от эмодзи"""
        emoji_pattern = re.compile(
            "["
            "\U0001F600-\U0001F64F"  # эмоции
            "\U0001F300-\U0001F5FF"  # символы  
            "\U0001F680-\U0001F6FF"  # транспорт
            "\U0001F1E0-\U0001F1FF"  # флаги
            "]+", flags=re.UNICODE
        )
        clean_text = emoji_pattern.sub('', text)
        clean_text = re.sub(r'\s+', ' ', clean_text).strip()
        return clean_text

    def speak(self, text):
        """Озвучка текста через Edge-TTS"""
        if not text or not text.strip():
            return
            
        assistant_name = config.get('assistant.name', 'Пятница')
        print(f"🤖 {assistant_name}: {text}")
        
        try:
            from friday_core.config.personalization import personalization
            
            # Стилизация ответа
            style = personalization.get_response_style()
            if style == 'friendly':
                friendly_prefixes = ['Конечно!', 'С удовольствием', 'Вот что я нашла: ']
                import random
                if random.random() < 0.3:
                    text = random.choice(friendly_prefixes) + ' ' + text
            elif style == 'casual':
                text = text.replace('Сейчас', 'Щас').replace('температура', 'темпра')

            # Быстрая очистка текста
            clean_text = self._remove_emojis(text)
            if not clean_text.strip():
                print("🔇 Текст содержит только эмодзи - пропускаю озвучку")
                return

            print(f"🔊 Озвучиваю: '{clean_text}'")
            
            # Инициализируем TTS если нужно
            self._init_tts()
            
            if self._tts_engine:
                self._tts_engine.speak(clean_text)
            else:
                print("🔇 TTS не доступен - только вывод текста")
                
        except Exception as e:
            print(f"❌ Ошибка озвучки: {e}")

    def _start_session(self):
        self.active_session = True
        self.last_command_time = time.time()
        print('Активная сессия начата')
        if self.session_timer:
            self.session_timer.cancel()
        self.session_timer = threading.Timer(self.session_timeout, self._end_session)
        self.session_timer.daemon = True
        self.session_timer.start()

    def _end_session(self):
        if self.active_session:
            self.active_session = False
            print('Сессия завершена')
            sound_manager.play_notification()

    def _reset_session_timer(self):
        if self.active_session and self.session_timer:
            self.session_timer.cancel()
            self.session_timer = threading.Timer(self.session_timeout, self._end_session)
            self.session_timer.daemon = True
            self.session_timer.start()
            self.last_command_time = time.time()

    def smart_listen(self):
        """Исправленная версия без рекурсии и проблем с инициализацией"""
        try:
            # 🔥 ИСПРАВЛЕНИЕ: Инициализируем распознаватель ПЕРЕД использованием
            self._init_recognizer()
            
            if self.active_session:
                print('🎤 Сессия активна - слушаю команду...')
                with self._microphone as source:
                    audio = self._recognizer.listen(source, timeout=5, phrase_time_limit=8)

                print("Аудио получено, распознаю...")
                command = self._recognizer.recognize_google(audio, language=self.language).lower()
                print(f'✅ Распознано в активной сессии: {command}')
                self._reset_session_timer()
                
                if any(word in command for word in ['спасибо', 'достаточно', 'отдыхай']):
                    self._end_session()
                    return None
                return command
            else:
                print(f'🎯 Ожидаю ключевое слово {self.wake_words}')
                with self._microphone as source:
                    audio = self._recognizer.listen(source, timeout=10, phrase_time_limit=8)

                print("🔊 Аудио получено, пытаюсь распознать...")
                try:

                    command = self._recognizer.recognize_google(audio, language=self.language).lower()
                    print(f'✅ Распознано: {command}')
                except Exception as e:
                    print(f'❌ Ошибка распознавания: {e}')
                    return None

                for wake_word in self.wake_words:
                    if wake_word in command:
                        sound_manager.play_activation()
                        print(f'🤖 {config.get("assistant.name", "Пятница")} активирована')
                        self._start_session()
                        
                        clean_command = command.split(wake_word, 1)[-1].strip()
                        if clean_command:
                            sound_manager.play_listening()
                            return clean_command
                        else:
                            self.speak('Да, сэр')
                            return ""  # Пустая команда вместо рекурсии
                return None
                
        except sr.WaitTimeoutError:
            if self.active_session:
                return ''
            return None
        except sr.UnknownValueError:
            if self.active_session:
                return 'не расслышала'
            return None
        except Exception as e:
            print(f'❌ Ошибка распознавания: {e}')
            if self.active_session:
                return 'ошибка'
            return None

    def listen_for_command(self):
        """Слушает микрофон (старый метод для совместимости)"""
        try:
            print("🎤 Слушаю...")
            self._init_recognizer()
            
            with self._microphone as source:
                audio = self._recognizer.listen(source, timeout=5, phrase_time_limit=8)
            
            command = self._recognizer.recognize_google(audio, language=self.language)
            print(f"✅ Распознано: {command}")
            return command.lower()
            
        except sr.WaitTimeoutError:
            return ""
        except sr.UnknownValueError:
            return "не расслышал"
        except Exception as e:
            print(f"❌ Ошибка распознавания: {e}")
            return "ошибка"