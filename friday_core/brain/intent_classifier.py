# brain/intent_classifier.py

import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
import pickle
import json
from pathlib import Path
from functools import lru_cache

class IntentClassifier:
    def __init__(self):
        self.vectorizer = TfidfVectorizer(max_features=1000, ngram_range=(1, 2))
        self.classifier = RandomForestClassifier(n_estimators=100, random_state=42)
        self.model_path = "ml_models/intent_classifier.pkl"
        self.is_trained = False
        
        # 🔥 ОПТИМИЗАЦИЯ: Быстрые паттерны для частых команд
        self._quick_patterns = {}
        self._build_quick_patterns()
        
        self.intents = {
            'weather': ['погода', 'температура', 'градус', 'дождь', 'солнце'],
            'music': ['музыка', 'включи', 'песня', 'плэйлист', 'хитмо'],
            'system': ['выключи', 'перезагрузи', 'компьютер', 'система'],
            'browser': ['открой', 'браузер', 'интернет', 'поиск', 'найди'],
            'reminder': ['напомни', 'таймер', 'событие', 'календарь'],
            'screenshot': ['скриншот', 'снимок', 'скрин'],
            'volume': ['громкость', 'звук', 'тише', 'громче'],
            'time': ['время', 'час', 'который час'],
            'greeting': ['привет', 'здравствуй', 'добрый', 'хай'],
            'farewell': ['пока', 'выход', 'стоп', 'заверши'],
            'calendar': ['календарь', 'событие', 'встреча', 'добавь событие'],
            'telegram': ['телеграм', 'telegram', 'отправь в телеграм'],
            'system_info': ['система', 'ресурсы', 'батарея', 'процессы', 'загрузка'],
            'application': ['открой', 'запусти', 'закрой', 'приложение', 'программа'],
            'config': ['настройки', 'конфиг', 'сброс', 'город', 'голос'],
            'help': ['помощь', 'команды', 'умеешь', 'что ты можешь']
        }
        
        self._load_model()

    def _build_quick_patterns(self):
        """Быстрые паттерны для мгновенного определения интентов"""
        quick_mapping = {
            'погода': 'weather',
            'температура': 'weather', 
            'музыка': 'music',
            'включи': 'music',
            'выключи': 'system',
            'перезагрузи': 'system',
            'открой': 'browser',
            'браузер': 'browser',
            'найди': 'browser',
            'напомни': 'reminder',
            'таймер': 'reminder',
            'скриншот': 'screenshot',
            'снимок': 'screenshot',
            'громкость': 'volume',
            'звук': 'volume',
            'время': 'time',
            'час': 'time',
            'привет': 'greeting',
            'здравствуй': 'greeting',
            'пока': 'farewell',
            'выход': 'farewell',
            'календарь': 'calendar',
            'событие': 'calendar',
            'телеграм': 'telegram',
            'telegram': 'telegram',
            'система': 'system_info',
            'ресурсы': 'system_info',
            'батарея': 'system_info',
            'приложение': 'application',
            'запусти': 'application',
            'настройки': 'config',
            'конфиг': 'config',
            'помощь': 'help',
            'команды': 'help'
        }
        self._quick_patterns = quick_mapping

    # 🔥 ОПТИМИЗАЦИЯ: Кэширование с ограничением по времени
    @lru_cache(maxsize=200)
    def predict_intent(self, text):
        """Кэшированное предсказание интента"""
        if not self.is_trained:
            return 'unknown'
            
        try:
            text_lower = text.lower().strip()
            
            # 🔥 ОПТИМИЗАЦИЯ: Сначала быстрая проверка
            quick_intent = self._quick_intent_check(text_lower)
            if quick_intent != 'unknown':
                return quick_intent
            
            # Полный ML анализ только если быстрая проверка не сработала
            X = self.vectorizer.transform([text_lower])
            prediction = self.classifier.predict(X)[0]
            confidence = np.max(self.classifier.predict_proba(X))
            
            return prediction if confidence > 0.6 else 'unknown'
            
        except Exception as e:
            print(f'Ошибка предсказания: {e}')
            return 'unknown'

    def _quick_intent_check(self, text):
        """Сверхбыстрая проверка по ключевым словам"""
        for keyword, intent in self._quick_patterns.items():
            if keyword in text:
                return intent
        return 'unknown'

    def _load_model(self):
        try:
            if Path(self.model_path).exists():
                with open(self.model_path, 'rb') as f:
                    model_data = pickle.load(f)
                    self.vectorizer = model_data['vectorizer']
                    self.classifier = model_data['classifier']
                    self.is_trained = True
                print('✅ ML модель загружена')
        except Exception as e:
            print(f'❌ Ошибка загрузки модели: {e}')

    def prepare_training_data(self):
        texts = []
        labels = []
        for intent, keywords in self.intents.items():
            for keyword in keywords:
                texts.append(keyword)
                labels.append(intent)
                variations = [
                    f'какая {keyword}',
                    f'покажи {keyword}',
                    f'включи {keyword}',
                    f'найди {keyword}',
                    f'скажи {keyword}',
                    f'установи {keyword}',
                    keyword
                ]
                for var in variations:
                    texts.append(var)
                    labels.append(intent)
        return texts, labels

    def train(self):
        try:
            texts, labels = self.prepare_training_data()
            X = self.vectorizer.fit_transform(texts)
            y = np.array(labels)
            X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
            self.classifier.fit(X_train, y_train)
            
            Path('ml_models').mkdir(exist_ok=True)
            with open(self.model_path, 'wb') as f:
                pickle.dump({
                    'vectorizer': self.vectorizer,
                    'classifier': self.classifier,
                }, f)
                
            self.is_trained = True
            accuracy = self.classifier.score(X_test, y_test)
            
            # 🔥 ОПТИМИЗАЦИЯ: Очищаем кэш после переобучения
            self.predict_intent.cache_clear()
            
            print(f'✅ Модель обучена! Точность: {accuracy:.2f}')
            return accuracy
            
        except Exception as e:
            print(f'❌ Ошибка обучения: {e}')
            return 0

# Глобальный экземпляр
intent_classifier = IntentClassifier()