# Aether

[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://python.org)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![GitHub Issues](https://img.shields.io/github/issues/utkaran/Aether.svg)](https://github.com/utkaran/Aether/issues)

> **An open-source framework for building ambient intelligence.**  
> Privacy-first, modular, and hackable. Born in a "garage" with pure enthusiasm.

---

## 🏗️ System Architecture

Aether построен по **модульной микросервисной архитектуре**, где каждый компонент отвечает за конкретную задачу.

### 🧠 Core Architecture Overview
┌─────────────────────────────────────────────────────────────┐
│ AETHER CORE │
├─────────────────────────────────────────────────────────────┤
│ ┌─────────────┐ ┌─────────────┐ ┌─────────────┐ │
│ │ BRAIN │ │ ORCHESTRATOR│ │ ENGINE │ │
│ │ │◄──►│ │◄──►│ │ │
│ │ • NLP │ │ • Command │ │ • Voice │ │
│ │ • Intent │ │ Routing │ │ Processing│ │
│ │ Classifier│ │ • Session │ │ • STT/TTS │ │
│ │ • Context │ │ Management│ │ • Audio I/O │ │
│ └─────────────┘ └─────────────┘ └─────────────┘ │
│ ▲ ▲ │
│ │ │ │
│ ▼ ▼ │
│ ┌─────────────────────────────────────────────────────────┤
│ │ NEURONS LAYER │
│ │ ┌─────────┐ ┌─────────┐ ┌─────────┐ ┌─────────┐ │
│ │ │ Audio │ │ Media │ │ System │ │ Weather │ ... │
│ │ │ Neuron │ │ Neuron │ │ Neuron │ │ Neuron │ │
│ │ └─────────┘ └─────────┘ └─────────┘ └─────────┘ │
│ └─────────────────────────────────────────────────────────┤
└─────────────────────────────────────────────────────────────┘

### 🔧 Component Details

#### **1. Brain Module** (`/brain`)
- **Intent Classifier** - распознает намерения пользователя из текста
- **Smart Command Handler** - ML-модель для "умной" обработки команд
- **Context Manager** - управление контекстом диалога в сессии

#### **2. Orchestrator** (`/neurons`)
- **Neuron Manager** - загружает и управляет "нейронами" (скиллами)
- **Command Router** - маршрутизирует команды к нужному нейрону
- **Session Controller** - управляет 20-секундными сессиями после wake-word

#### **3. Voice Engine** (`/engine`)
- **Wake Word Detection** - постоянно слушает ключевое слово "Пятница"
- **Speech-to-Text (STT)** - конвертирует голос в текст (Vosk/Whisper)
- **Text-to-Speech (TTS)** - синтезирует ответы (Silero/RHVoice)
- **Audio Manager** - работа с аудиопотоками и эффектами

#### **4. Neurons Layer** (`/neurons`, `/skills`)
**Модульные "нейроны" - каждый независим и отвечает за свою область:**
- `audio_neuron` - управление громкостью, звуком
- `media_neuron` - YouTube, музыка, видео
- `system_neuron` - выключение, перезагрузка, информация о системе
- `weather_neuron` - прогноз погоды через API
- `telegram_neuron` - интеграция с Telegram
- `reminder_neuron` - напоминания и календарь
- `time_neuron` - время, дата, таймеры

#### **5. Support Modules**
- **Config Manager** (`/config`) - настройки и персонализация
- **Event Bus** (`/utils`) - шина событий для межмодульного взаимодействия
- **GUI Layer** (`/gui`) - Tkinter интерфейс с индикацией статусов

### 🔄 Data Flow
User Speech
→ Wake Word Detection
→ STT Processing
→ Intent Classification
→ Command Routing
→ Neuron Execution
→ TTS Response
→ User Output

### 🎯 Key Architectural Decisions

1. **Модульность** - каждый "нейрон" можно разрабатывать и тестировать независимо
2. **Сессионность** - 20-секундные сессии после активации для естественного диалога
3. **Event-Driven** - шина событий для слабой связанности компонентов
4. **ML Ready** - архитектура готова к интеграции более сложных ML-моделей

---

## 🚀 Quick Start

```bash
# Clone the repository
git clone https://github.com/utkaran/Aether.git
cd Aether

# Install dependencies
pip install -r requirements.txt

# Launch Aether
python main.py

🛠️ Tech Stack
Language: Python 3.8+

Architecture: Modular microservices-style

ML: Custom intent classifier, Vosk/Whisper integration

GUI: Tkinter

Audio: PyAudio, pygame

Communication: Event bus, inter-process communication

🤝 Contributing
This is a passion-driven project! I welcome:

🔧 Developers to help build new neurons

🎨 Designers to improve the GUI

📚 Technical writers for documentation

💡 Ideas and feature requests

Feel free to:

Open an Issue for bugs or features

Submit a Pull Request

Fork and experiment!

🎯 Project Status
Active Development - This is my learning playground and passion project. Things might break, but innovation happens here!

📜 License
MIT License - see LICENSE file for details.

<div align="center">
"If you're not building something in your garage, you're just consuming what others build."

</div> ```
