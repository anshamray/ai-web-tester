import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    # OpenAI API настройки
    OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
    
    # Playwright настройки
    BROWSER_HEADLESS = True
    BROWSER_TIMEOUT = 30000  # 30 секунд
    PAGE_LOAD_TIMEOUT = 10000  # 10 секунд
    
    # Настройки для анализа сайтов
    MAX_PAGES_TO_ANALYZE = 10
    MAX_LINKS_TO_CHECK = 50
    REQUEST_DELAY = 1  # секунды между запросами
    
    # Настройки для отчетов
    REPORTS_DIR = "reports"
    
    @classmethod
    def validate(cls):
        """Проверяет наличие обязательных настроек"""
        if not cls.OPENAI_API_KEY or cls.OPENAI_API_KEY == "your-openai-api-key-here":
            raise ValueError("OPENAI_API_KEY не установлен")
        return True 