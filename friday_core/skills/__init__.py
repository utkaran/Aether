# friday_core/skills/__init__.py

from friday_core.skills.basic_skills import BasicSkills
from friday_core.skills.audio_skills import AudioSkills
from friday_core.skills.automation_skills import automation_skills
from friday_core.skills.calendar_skills import calendar_skills
from friday_core.skills.email_skills import email_skills
from friday_core.skills.media_skills import MediaKills
from friday_core.skills.reminder_skills import ReminderSkills
from friday_core.skills.system_skills import SystemSkills
from friday_core.skills.telegram_skills import telegram_skills
from friday_core.skills.weather_skills import WeatherSkills
from friday_core.skills.working_system_info import WorkingSystemInfo

__all__ = [
  'BasicSkills',
  'AudioSkills',
  'automation_skills',
  'calendar_skills',
  'email_skills',
  'MediaKills',
  'ReminderSkills',
  'SystemSkills',
  'telegram_skills',
  'WeatherSkills',
  'WorkingSystemInfo',
]