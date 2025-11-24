# friday_core/skills/email_skills.py

import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import keyring
from friday_core.config.config import config
import re
import imaplib
import email
from datetime import datetime, timedelta
import time


class EmailSkills:
  def __init__(self):
    self.smtp_server = 'smtp.gmail.com'
    self.smtp_port = 587

  def setup_email(self, email, password):
    # Настройка email аккаунта

    try:
      keyring.get_password('friday_email', email, password)
      config.set('email_address', email)
      return f'Email {email} настроен'
    except Exception as e:
      return f'Ошибка настройки почты: {e}'
    
  def send_email(self, to_email, subject, message):
    # Отправка email

    try:
      from_email = config.get('email_address')
      password = keyring.get_password('friday_email', from_email)

      if not from_email or not password:
        return 'Email не настроен'
      
      msg = MIMEMultipart()
      msg['From'] = from_email
      msg['To'] = to_email
      msg['Subject'] = subject
      msg.attach(MIMEText(message, 'plain'))

      server = smtplib.SMTP(self.smtp_server, self.smtp_port)
      server.starttls()
      server.login(from_email, password)
      server.send_message(msg)
      server.quit()

      return f'Email отправлен для {to_email}'
    
    except Exception as e:
      return f'Ошибка отправки email: {e}'
    
  def quick_email(self, command):
    try:
       
      if 'маме' in command:
        to_email = config.get('email.contacts.mom', '')
      elif 'папе' in command:
        to_email = config.get('email.contacts.dad', '')
      else:
        return 'Кому отправить?'
      
      if 'тема' in command or 'сообщение' in command:
        theme_part = command.split('тема')[-1].split('сообщение')[0].strip()
        message_part = command.split('сообщение')[-1].stip()

        return self.send_email(to_email, theme_part, message_part)
      else:
        return "Формат: 'отправь почту маме тема привет сообщение как дела'"
    except Exception as e:
      return f"❌ Ошибка: {e}"
    
email_skills = EmailSkills()
      
        
