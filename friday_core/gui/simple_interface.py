# friday_core/gui/simple_interface.py

import tkinter as tk
from tkinter import scrolledtext, ttk
import threading
import time
from datetime import datetime
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))

class FridayGUI:
    def __init__(self):
        self.setup_gui()
        self.friday = None
        self.is_friday_loading = False
        self.is_closing = False  # Флаг закрытия приложения
        
        threading.Thread(target=self.initialize_friday, daemon=True).start()
        
    def setup_gui(self):
        self.root = tk.Tk()
        self.root.title("🤖 Пятница - Голосовой ассистент")
        self.root.geometry("700x500")
        self.root.configure(bg='#1e1e1e')
        self.root.minsize(600, 400)
        
        style = ttk.Style()
        style.theme_use('clam')
        style.configure('TFrame', background='#1e1e1e')
        
        self.setup_chat_area()
        self.setup_input_area()
        
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
        
    def setup_chat_area(self):
        title_frame = ttk.Frame(self.root)
        title_frame.pack(fill=tk.X, padx=10, pady=5)
        
        title_label = tk.Label(
            title_frame,
            text="🤖 Пятница - Чат",
            font=('Arial', 14, 'bold'),
            fg='#007acc',
            bg='#1e1e1e'
        )
        title_label.pack()
        
        chat_frame = ttk.Frame(self.root)
        chat_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        
        self.chat_area = scrolledtext.ScrolledText(
            chat_frame,
            wrap=tk.WORD,
            width=80,
            height=20,
            bg='#252526',
            fg='#d4d4d4',
            font=('Consolas', 10),
            insertbackground='white',
            relief='flat',
            borderwidth=0
        )
        self.chat_area.pack(fill=tk.BOTH, expand=True)
        self.chat_area.config(state=tk.DISABLED)
        
        self.chat_area.tag_config("user", foreground="#4ec9b0")
        self.chat_area.tag_config("friday", foreground="#9cdcfe")
        self.chat_area.tag_config("system", foreground="#ce9178")
        self.chat_area.tag_config("time", foreground="#6a9955", font=('Consolas', 8))
        
    def setup_input_area(self):
        input_frame = ttk.Frame(self.root)
        input_frame.pack(fill=tk.X, padx=10, pady=10)
        
        self.input_field = tk.Entry(
            input_frame,
            width=60,
            font=('Arial', 11),
            bg='#3c3c3c',
            fg='white',
            insertbackground='white',
            relief='sunken',
            borderwidth=1
        )
        self.input_field.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 10))
        self.input_field.bind('<Return>', self.send_message)
        self.input_field.bind('<KeyRelease>', self.on_key_release)
        
        self.send_btn = tk.Button(
            input_frame,
            text="📤",
            command=self.send_message,
            bg='#007acc',
            fg='white',
            font=('Arial', 12),
            relief='flat',
            borderwidth=0,
            width=4,
            state=tk.DISABLED
        )
        self.send_btn.pack(side=tk.RIGHT)
        
        hint_label = tk.Label(
            self.root,
            text="💡 Нажми Enter для отправки сообщения",
            font=('Arial', 9),
            fg='#858585',
            bg='#1e1e1e'
        )
        hint_label.pack(pady=(0, 5))
        
        self.input_field.focus()
        
    def initialize_friday(self):
        """Инициализация Пятницы в отдельном потоке"""
        self.is_friday_loading = True
        
        # Проверяем что окно еще существует
        if self.root.winfo_exists():
            self.root.after(0, self.add_message, "system", "🔄 Загружаю Пятницу...")
        
        try:
            from friday_core.main import Friday
            self.friday = Friday()
            self.is_friday_loading = False
            
            # Проверяем что окно еще существует
            if self.root.winfo_exists():
                self.root.after(0, self.add_message, "system", "✅ Пятница готова к работе!")
                self.root.after(0, self.add_message, "friday", "Привет! Я твой ассистент Пятница. Чем могу помочь?")
                
        except Exception as e:
            self.is_friday_loading = False
            # Проверяем что окно еще существует
            if self.root.winfo_exists():
                error_details = f"❌ Ошибка загрузки: {str(e)}\n"
                error_details += f"💡 Тип ошибки: {type(e).__name__}\n"

                import traceback
                tb = traceback.format_exc()
                error_details += f"🔍 Детали:\n{tb}"
                self.root.after(0, self.add_message, "system", error_details)
        
    def on_key_release(self, event):
        if self.input_field.get().strip():
            self.send_btn.config(state=tk.NORMAL, bg='#007acc')
        else:
            self.send_btn.config(state=tk.DISABLED, bg='#555555')
        
    def add_message(self, sender, message):
        """Добавление сообщения в чат"""
        # Дополнительная проверка на существование окна
        if not self.root.winfo_exists():
            return
            
        self.chat_area.config(state=tk.NORMAL)
        
        timestamp = datetime.now().strftime("%H:%M:%S")
        self.chat_area.insert(tk.END, f"[{timestamp}] ", "time")
        
        if sender == "user":
            self.chat_area.insert(tk.END, f"👤 Ты: {message}\n", "user")
        elif sender == "friday":
            self.chat_area.insert(tk.END, f"🤖 Пятница: {message}\n", "friday")
        elif sender == "system":
            self.chat_area.insert(tk.END, f"⚙️ Система: {message}\n", "system")
            
        self.chat_area.config(state=tk.DISABLED)
        self.chat_area.see(tk.END)
        
    def send_message(self, event=None):
        message = self.input_field.get().strip()
        if not message or self.is_friday_loading:
            return
            
        self.input_field.delete(0, tk.END)
        self.send_btn.config(state=tk.DISABLED, bg='#555555')
        
        self.add_message("user", message)
        
        threading.Thread(target=self.process_message, args=(message,), daemon=True).start()
        
    def process_message(self, message):
        """Обработка сообщения в отдельном потоке"""
        try:
            if self.friday is None:
                # Проверяем что окно еще существует
                if self.root.winfo_exists():
                    self.root.after(0, self.add_message, "system", "Пятница еще загружается...")
                return
                
            response = self.friday.command_handler.handle_command(message)
            
            time.sleep(0.5)
            
            # Обновляем UI в основном потоке только если окно существует
            if self.root.winfo_exists():
                self.root.after(0, self.add_message, "friday", response)
            
        except Exception as e:
            error_msg = f"Ошибка обработки: {str(e)}"
            # Проверяем что окно еще существует перед обновлением
            if self.root.winfo_exists():
                self.root.after(0, self.add_message, "system", error_msg)
        
    def on_closing(self):
        """Обработка закрытия окна"""
        self.is_closing = True
        
        if self.friday:
            try:
                self.friday.shutdown()
            except:
                pass
        
        try:
            self.root.destroy()
        except:
            pass
        
        # Принудительно завершаем процесс
        import os
        os._exit(0)
        
    def run(self):
        try:
            self.root.mainloop()
        except KeyboardInterrupt:
            self.on_closing()

def main():
    gui = FridayGUI()
    gui.run()

if __name__ == "__main__":
    main()