import asyncio
from typing import Dict, List, Optional, Any
from playwright.async_api import async_playwright, Browser, Page, BrowserContext
from dataclasses import dataclass
import json
import time
from config import Config

@dataclass
class PageInfo:
    """Информация о странице"""
    url: str
    title: str
    content: str
    links: List[str]
    images: List[str]
    forms: List[Dict[str, Any]]
    meta_tags: Dict[str, str]
    status_code: Optional[int] = None
    load_time: Optional[float] = None
    errors: List[str] = None

class PlaywrightBrowserTool:
    """Инструмент для работы с браузером через Playwright"""
    
    def __init__(self):
        self.browser: Optional[Browser] = None
        self.context: Optional[BrowserContext] = None
        self.page: Optional[Page] = None
        self.playwright = None
        
    async def __aenter__(self):
        """Асинхронный контекстный менеджер - вход"""
        await self.start()
        return self
        
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """Асинхронный контекстный менеджер - выход"""
        await self.close()
        
    async def start(self):
        """Запускает браузер"""
        self.playwright = await async_playwright().start()
        self.browser = await self.playwright.chromium.launch(
            headless=Config.BROWSER_HEADLESS
        )
        self.context = await self.browser.new_context()
        self.page = await self.context.new_page()
        
        # Устанавливаем таймауты
        self.page.set_default_timeout(Config.BROWSER_TIMEOUT)
        
    async def close(self):
        """Закрывает браузер"""
        if self.page:
            await self.page.close()
        if self.context:
            await self.context.close()
        if self.browser:
            await self.browser.close()
        if self.playwright:
            await self.playwright.stop()
            
    async def navigate_to_page(self, url: str) -> PageInfo:
        """Переходит на страницу и собирает информацию о ней"""
        if not self.page:
            raise RuntimeError("Браузер не запущен. Используйте async with или вызовите start()")
            
        start_time = time.time()
        errors = []
        
        try:
            # Переходим на страницу
            response = await self.page.goto(url, wait_until="domcontentloaded")
            status_code = response.status if response else None
            
            # Ждем загрузки страницы
            await self.page.wait_for_load_state("networkidle", timeout=Config.PAGE_LOAD_TIMEOUT)
            
            load_time = time.time() - start_time
            
            # Собираем информацию о странице
            page_info = await self._extract_page_info(url, status_code, load_time)
            page_info.errors = errors
            
            return page_info
            
        except Exception as e:
            errors.append(f"Ошибка при загрузке страницы: {str(e)}")
            load_time = time.time() - start_time
            
            # Возвращаем частичную информацию даже при ошибке
            return PageInfo(
                url=url,
                title="",
                content="",
                links=[],
                images=[],
                forms=[],
                meta_tags={},
                status_code=None,
                load_time=load_time,
                errors=errors
            )
    
    async def _extract_page_info(self, url: str, status_code: Optional[int], load_time: float) -> PageInfo:
        """Извлекает информацию со страницы"""
        
        # Получаем заголовок
        title = await self.page.title()
        
        # Получаем текстовое содержимое
        content = await self.page.evaluate("() => document.body.innerText")
        
        # Получаем все ссылки
        links = await self.page.evaluate("""
            () => Array.from(document.querySelectorAll('a[href]'))
                      .map(a => a.href)
                      .filter(href => href && !href.startsWith('javascript:'))
        """)
        
        # Получаем все изображения
        images = await self.page.evaluate("""
            () => Array.from(document.querySelectorAll('img[src]'))
                      .map(img => img.src)
        """)
        
        # Получаем информацию о формах с расширенным контекстом
        forms = await self.page.evaluate("""
            () => Array.from(document.querySelectorAll('form')).map((form, index) => {
                // Получаем все поля ввода
                const inputs = Array.from(form.querySelectorAll('input, select, textarea')).map(input => ({
                    name: input.name || '',
                    type: input.type || 'text',
                    required: input.required || false,
                    placeholder: input.placeholder || '',
                    value: input.value || ''
                }));
                
                // Получаем все кнопки в форме
                const buttons = Array.from(form.querySelectorAll('button, input[type="submit"]')).map(btn => ({
                    text: btn.textContent?.trim() || btn.value || '',
                    type: btn.type || 'button'
                }));
                
                // Пытаемся определить назначение формы по контексту
                const formText = form.textContent?.trim() || '';
                const nearbyText = form.parentElement?.textContent?.trim() || '';
                
                // Получаем классы формы для дополнительного анализа
                const classes = form.className || '';
                
                return {
                    index: index + 1,
                    action: form.action || '',
                    method: form.method || 'GET',
                    inputs: inputs,
                    buttons: buttons,
                    classes: classes,
                    form_text: formText.substring(0, 200),
                    nearby_text: nearbyText.substring(0, 300),
                    has_inputs: inputs.length > 0,
                    has_buttons: buttons.length > 0
                };
            })
        """)
        
        # Получаем мета-теги
        meta_tags = await self.page.evaluate("""
            () => {
                const metas = {};
                document.querySelectorAll('meta').forEach(meta => {
                    const name = meta.getAttribute('name') || meta.getAttribute('property');
                    const content = meta.getAttribute('content');
                    if (name && content) {
                        metas[name] = content;
                    }
                });
                return metas;
            }
        """)
        
        return PageInfo(
            url=url,
            title=title,
            content=content[:5000],  # Ограничиваем размер контента
            links=list(set(links)),  # Убираем дубликаты
            images=list(set(images)),
            forms=forms,
            meta_tags=meta_tags,
            status_code=status_code,
            load_time=load_time
        )
    
    async def check_link(self, url: str) -> Dict[str, Any]:
        """Проверяет доступность ссылки"""
        try:
            response = await self.page.goto(url, wait_until="domcontentloaded")
            return {
                "url": url,
                "status": "ok",
                "status_code": response.status if response else None,
                "error": None
            }
        except Exception as e:
            return {
                "url": url,
                "status": "error",
                "status_code": None,
                "error": str(e)
            }
    
    async def take_screenshot(self, path: str = None) -> bytes:
        """Делает скриншот страницы"""
        if not self.page:
            raise RuntimeError("Браузер не запущен")
            
        screenshot = await self.page.screenshot(
            path=path,
            full_page=True
        )
        return screenshot
    
    async def execute_javascript(self, script: str) -> Any:
        """Выполняет JavaScript на странице"""
        if not self.page:
            raise RuntimeError("Браузер не запущен")
            
        return await self.page.evaluate(script) 