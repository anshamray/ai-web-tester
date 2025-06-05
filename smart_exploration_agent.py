import asyncio
import random
import string
from typing import Dict, List, Any, Optional, Tuple
from langchain_openai import ChatOpenAI
from langchain.schema import HumanMessage, SystemMessage
from browser_tool import PlaywrightBrowserTool, PageInfo
from config import Config
import json
from datetime import datetime
import os
import time
from playwright.async_api import Page, ElementHandle

class SmartExplorationAgent:
    """Умный агент для глубокого исследования веб-сайтов"""
    
    def __init__(self):
        Config.validate()
        self.llm = ChatOpenAI(
            temperature=0.3,  # Немного больше креативности для исследования
            api_key=Config.OPENAI_API_KEY,
            model="gpt-4o-mini"
        )
        self.browser_tool = PlaywrightBrowserTool()
        self.session_data = {}  # Данные сессии для сохранения состояния
        self.discovered_pages = set()  # Обнаруженные страницы
        self.user_personas = self._create_user_personas()
        
    def _create_user_personas(self) -> List[Dict[str, Any]]:
        """Создает различные пользовательские персоны для тестирования"""
        return [
            {
                "name": "regular_user",
                "email_prefix": "testuser",
                "first_name": "John",
                "last_name": "Doe",
                "age": "25",
                "phone": "+1234567890",
                "address": "123 Main St",
                "city": "New York",
                "country": "USA",
                "company": "Test Corp",
                "behavior": "cautious"  # осторожный пользователь
            },
            {
                "name": "power_user",
                "email_prefix": "poweruser",
                "first_name": "Jane",
                "last_name": "Smith",
                "age": "35",
                "phone": "+1987654321",
                "address": "456 Oak Ave",
                "city": "San Francisco",
                "country": "USA",
                "company": "Tech Solutions",
                "behavior": "aggressive"  # активный пользователь
            },
            {
                "name": "edge_case_user",
                "email_prefix": "edgeuser",
                "first_name": "Александр",  # Unicode имя
                "last_name": "O'Connor-Smith",  # Сложная фамилия
                "age": "99",
                "phone": "+7-800-555-0199",
                "address": "Улица Пушкина, дом Колотушкина",
                "city": "Москва",
                "country": "Россия",
                "company": "ООО 'Тест & Ко'",
                "behavior": "boundary_testing"  # граничные случаи
            }
        ]
    
    async def deep_explore_website(self, url: str, max_depth: int = 3) -> Dict[str, Any]:
        """Глубокое исследование веб-сайта с попытками регистрации и взаимодействия"""
        
        print(f"🚀 Начинаю глубокое исследование сайта: {url}")
        print(f"📊 Максимальная глубина исследования: {max_depth}")
        
        exploration_report = {
            "url": url,
            "timestamp": datetime.now().isoformat(),
            "exploration_depth": max_depth,
            "discovered_pages": [],
            "registration_attempts": [],
            "form_interactions": [],
            "hidden_functionality": [],
            "user_flows": [],
            "security_findings": [],
            "accessibility_issues": [],
            "performance_insights": []
        }
        
        async with self.browser_tool:
            # Этап 1: Базовый анализ главной страницы
            print("🔍 Этап 1: Анализ главной страницы...")
            main_page = await self.browser_tool.navigate_to_page(url)
            exploration_report["main_page_analysis"] = await self._analyze_page_deeply(main_page)
            
            # Этап 2: Поиск и анализ форм регистрации/входа
            print("📝 Этап 2: Поиск форм регистрации и входа...")
            auth_forms = await self._discover_auth_forms(main_page)
            exploration_report["auth_forms_discovered"] = len(auth_forms)
            
            # Этап 3: Попытки регистрации с разными персонами
            print("👥 Этап 3: Попытки регистрации с разными пользователями...")
            for persona in self.user_personas:
                registration_result = await self._attempt_registration(auth_forms, persona)
                if registration_result:
                    exploration_report["registration_attempts"].append(registration_result)
            
            # Этап 4: Исследование всех доступных форм
            print("📋 Этап 4: Интеллектуальное заполнение всех форм...")
            form_results = await self._explore_all_forms(main_page)
            exploration_report["form_interactions"] = form_results
            
            # Этап 5: Поиск скрытой функциональности
            print("🕵️ Этап 5: Поиск скрытой функциональности...")
            hidden_features = await self._discover_hidden_functionality()
            exploration_report["hidden_functionality"] = hidden_features
            
            # Этап 6: Исследование пользовательских потоков
            print("🛤️ Этап 6: Анализ пользовательских потоков...")
            user_flows = await self._analyze_user_flows(main_page, max_depth)
            exploration_report["user_flows"] = user_flows
            
            # Этап 7: Проверка безопасности
            print("🔒 Этап 7: Анализ безопасности...")
            security_findings = await self._security_analysis()
            exploration_report["security_findings"] = security_findings
            
            # Этап 8: Анализ производительности
            print("⚡ Этап 8: Анализ производительности...")
            performance_insights = await self._performance_analysis()
            exploration_report["performance_insights"] = performance_insights
            
            # Сохраняем отчет
            await self._save_exploration_report(exploration_report)
            
            print(f"✅ Исследование завершено!")
            print(f"📄 Обнаружено страниц: {len(self.discovered_pages)}")
            print(f"📝 Попыток регистрации: {len(exploration_report['registration_attempts'])}")
            print(f"📋 Форм протестировано: {len(exploration_report['form_interactions'])}")
            
            return exploration_report
    
    async def _analyze_page_deeply(self, page_info: PageInfo) -> Dict[str, Any]:
        """Глубокий анализ страницы с помощью AI"""
        
        prompt = f"""
        Perform a deep analysis of this web page for intelligent exploration:
        
        URL: {page_info.url}
        Title: {page_info.title}
        
        Content preview: {page_info.content[:3000]}
        
        Forms found: {len(page_info.forms)}
        Links found: {len(page_info.links)}
        
        Forms details:
        {json.dumps(page_info.forms, ensure_ascii=False, indent=2)}
        
        Analyze and identify:
        1. Site purpose and main functionality
        2. User registration/login opportunities
        3. Interactive elements that need testing
        4. Potential hidden or advanced features
        5. Security considerations
        6. Areas that might require authentication
        7. E-commerce or transaction capabilities
        8. Social features or user-generated content
        9. API endpoints or AJAX functionality
        10. Mobile/responsive considerations
        
        Provide specific recommendations for intelligent exploration and testing.
        
        Respond in JSON format with detailed analysis and actionable recommendations.
        """
        
        messages = [
            SystemMessage(content="You are an expert web application security tester and UX researcher. Provide detailed, actionable insights for comprehensive website exploration."),
            HumanMessage(content=prompt)
        ]
        
        response = self.llm.invoke(messages)
        
        try:
            return json.loads(response.content)
        except json.JSONDecodeError:
            return {"analysis": response.content, "format": "text"}
    
    async def _discover_auth_forms(self, page_info: PageInfo) -> List[Dict[str, Any]]:
        """Обнаруживает формы аутентификации (регистрация, вход)"""
        
        auth_forms = []
        
        # Анализируем существующие формы
        for form in page_info.forms:
            form_purpose = await self._classify_form_purpose(form)
            if form_purpose in ['registration', 'login', 'signup', 'signin']:
                auth_forms.append({
                    "form": form,
                    "purpose": form_purpose,
                    "confidence": 0.8
                })
        
        # Ищем дополнительные формы на странице
        additional_forms = await self._search_for_auth_links()
        auth_forms.extend(additional_forms)
        
        return auth_forms
    
    async def _classify_form_purpose(self, form: Dict[str, Any]) -> str:
        """Классифицирует назначение формы с помощью AI"""
        
        form_text = form.get('form_text', '') + ' ' + form.get('nearby_text', '')
        inputs = form.get('inputs', [])
        buttons = form.get('buttons', [])
        
        # Простая эвристика
        text_lower = form_text.lower()
        
        # Проверяем ключевые слова для регистрации
        registration_keywords = [
            'sign up', 'register', 'create account', 'join', 'get started',
            'create your account', 'become a member', 'start your journey',
            'join us', 'create profile', 'new account', 'registration',
            'create a password', 'create password', 'birthdate', 'birth date',
            'date of birth', 'age verification'
        ]
        
        # Проверяем ключевые слова для входа
        login_keywords = [
            'sign in', 'login', 'log in', 'enter', 'access account',
            'welcome back', 'member login', 'user login', 'enter password'
        ]
        
        if any(keyword in text_lower for keyword in registration_keywords):
            return 'registration'
        elif any(keyword in text_lower for keyword in login_keywords):
            return 'login'
        elif any(keyword in text_lower for keyword in ['contact', 'message', 'email us']):
            return 'contact'
        elif any(keyword in text_lower for keyword in ['search']):
            return 'search'
        elif any(keyword in text_lower for keyword in ['subscribe', 'newsletter']):
            return 'subscription'
        
        # Анализ полей ввода для более точной классификации
        input_types = [inp.get('type', '').lower() for inp in inputs]
        input_names = [inp.get('name', '').lower() for inp in inputs]
        input_placeholders = [inp.get('placeholder', '').lower() for inp in inputs]
        
        all_input_text = ' '.join(input_names + input_placeholders).lower()
        
        # Специальная проверка для Pinterest-подобных форм
        # Если есть placeholder "create a password" или "create password" - это регистрация
        for placeholder in input_placeholders:
            if any(keyword in placeholder for keyword in ['create a password', 'create password']):
                return 'registration'
        
        # Если есть поля пароля и email
        if 'password' in input_types and ('email' in input_types or 'email' in all_input_text):
            # Проверяем признаки регистрации
            registration_indicators = [
                'confirm' in all_input_text,  # подтверждение пароля
                'first' in all_input_text,    # имя
                'last' in all_input_text,     # фамилия
                'name' in all_input_text,     # имя
                'phone' in all_input_text,    # телефон
                'birth' in all_input_text,    # дата рождения
                'date' in input_types,        # поле даты (обычно для дня рождения)
                'agree' in text_lower,        # согласие с условиями
                'terms' in text_lower,        # условия использования
                len(inputs) > 2               # больше 2 полей обычно = регистрация
            ]
            
            if any(registration_indicators):
                return 'registration'
            else:
                return 'login'
        
        # Если только email без пароля - возможно подписка
        if 'email' in input_types and 'password' not in input_types:
            if any(keyword in text_lower for keyword in ['subscribe', 'newsletter', 'updates']):
                return 'subscription'
        
        return 'unknown'
    
    async def _search_for_auth_links(self) -> List[Dict[str, Any]]:
        """Ищет ссылки на страницы регистрации/входа и кнопки для модальных окон"""
        
        auth_forms = []
        
        try:
            # Ищем ссылки на регистрацию/вход
            auth_links = await self.browser_tool.page.evaluate("""
                () => {
                    const links = Array.from(document.querySelectorAll('a[href]'));
                    return links
                        .filter(link => {
                            const text = link.textContent.toLowerCase();
                            const href = link.href.toLowerCase();
                            return text.includes('sign up') || text.includes('register') || 
                                   text.includes('login') || text.includes('sign in') ||
                                   href.includes('register') || href.includes('login') ||
                                   href.includes('signup') || href.includes('signin');
                        })
                        .map(link => ({
                            href: link.href,
                            text: link.textContent.trim()
                        }));
                }
            """)
            
            # Ищем кнопки регистрации (могут открывать модальные окна)
            signup_buttons = await self.browser_tool.page.evaluate("""
                () => {
                    const buttons = Array.from(document.querySelectorAll('button, [role="button"], .btn, input[type="button"], a, div[onclick], span[onclick]'));
                    return buttons
                        .filter(btn => {
                            const text = btn.textContent.toLowerCase();
                            const ariaLabel = (btn.getAttribute('aria-label') || '').toLowerCase();
                            const dataTestId = (btn.getAttribute('data-testid') || '').toLowerCase();
                            const className = (btn.className || '').toLowerCase();
                            const id = (btn.id || '').toLowerCase();
                            
                            // Расширенный список ключевых слов для регистрации
                            const signupKeywords = [
                                'sign up', 'signup', 'register', 'registration', 'join', 'create account',
                                'get started', 'start free', 'join now', 'create', 'new account'
                            ];
                            
                            return signupKeywords.some(keyword => 
                                text.includes(keyword) || 
                                ariaLabel.includes(keyword) ||
                                dataTestId.includes(keyword.replace(' ', '')) ||
                                className.includes(keyword.replace(' ', '')) ||
                                id.includes(keyword.replace(' ', ''))
                            );
                        })
                        .map(btn => ({
                            text: btn.textContent.trim(),
                            tagName: btn.tagName,
                            className: btn.className,
                            dataTestId: btn.getAttribute('data-testid') || '',
                            ariaLabel: btn.getAttribute('aria-label') || '',
                            id: btn.id || '',
                            href: btn.href || ''
                        }));
                }
            """)
            
            print(f"🔗 Найдено ссылок на аутентификацию: {len(auth_links)}")
            print(f"🔘 Найдено кнопок регистрации: {len(signup_buttons)}")
            
            # Добавляем диагностику если кнопки не найдены или есть проблемы
            if len(signup_buttons) == 0:
                print("🔍 Кнопки регистрации не найдены, запускаем диагностику...")
                await self._debug_page_elements("sign up")
                await self._debug_page_elements("register")
            
            # Пробуем кликнуть по кнопкам регистрации для открытия модальных окон
            for button_info in signup_buttons[:2]:  # Ограничиваем количество
                try:
                    print(f"🔘 Пробуем кликнуть по кнопке: {button_info['text']}")
                    
                    # Создаем список селекторов для поиска кнопки
                    selectors = []
                    
                    if button_info['text']:
                        # Селекторы по тексту
                        selectors.extend([
                            f"button:has-text('{button_info['text']}')",
                            f"[role='button']:has-text('{button_info['text']}')",
                            f"div:has-text('{button_info['text']}')",
                            f"a:has-text('{button_info['text']}')",
                            f"span:has-text('{button_info['text']}')"
                        ])
                    
                    if button_info['dataTestId']:
                        selectors.append(f"[data-testid='{button_info['dataTestId']}']")
                    
                    if button_info['ariaLabel']:
                        selectors.append(f"[aria-label='{button_info['ariaLabel']}']")
                    
                    if button_info['className']:
                        # Разбиваем классы и создаем селекторы
                        classes = button_info['className'].split()
                        for cls in classes[:3]:  # Берем первые 3 класса
                            if cls:
                                selectors.append(f".{cls}")
                    
                    # Добавляем общие селекторы для кнопок регистрации
                    selectors.extend([
                        "[data-testid*='signup']",
                        "[data-testid*='register']",
                        "[aria-label*='sign up']",
                        "[aria-label*='register']",
                        "button[class*='signup']",
                        "button[class*='register']",
                        ".signup-btn",
                        ".register-btn",
                        "#signup",
                        "#register"
                    ])
                    
                    button_clicked = False
                    
                    # Пробуем каждый селектор
                    for selector in selectors:
                        try:
                            # Ищем элемент
                            elements = await self.browser_tool.page.query_selector_all(selector)
                            
                            for element in elements:
                                try:
                                    # Проверяем видимость элемента
                                    is_visible = await element.is_visible()
                                    is_enabled = await element.is_enabled()
                                    
                                    print(f"🔍 Элемент {selector}: видимый={is_visible}, активный={is_enabled}")
                                    
                                    if not is_visible:
                                        # Пробуем прокрутить к элементу
                                        try:
                                            await element.scroll_into_view_if_needed()
                                            await self.browser_tool.page.wait_for_timeout(1000)
                                            is_visible = await element.is_visible()
                                            print(f"🔄 После скроллинга: видимый={is_visible}")
                                        except:
                                            pass
                                    
                                    if is_visible and is_enabled:
                                        # Обычный клик
                                        print(f"✅ Кликаем по элементу: {selector}")
                                        await element.click(timeout=5000)
                                        button_clicked = True
                                        break
                                    elif is_enabled:
                                        # Принудительный клик если элемент не видим но активен
                                        print(f"🔧 Принудительный клик по элементу: {selector}")
                                        await element.click(force=True, timeout=5000)
                                        button_clicked = True
                                        break
                                    else:
                                        # JavaScript клик как последняя попытка
                                        print(f"⚡ JavaScript клик по элементу: {selector}")
                                        await element.evaluate("el => el.click()")
                                        button_clicked = True
                                        break
                                        
                                except Exception as click_error:
                                    print(f"⚠️ Ошибка клика по {selector}: {click_error}")
                                    continue
                            
                            if button_clicked:
                                break
                                
                        except Exception as selector_error:
                            print(f"⚠️ Ошибка селектора {selector}: {selector_error}")
                            continue
                    
                    if not button_clicked:
                        print(f"❌ Не удалось кликнуть ни по одному селектору для кнопки: {button_info['text']}")
                        print("🔍 Запускаем дополнительную диагностику...")
                        await self._debug_page_elements(button_info['text'] or "sign up")
                        continue
                    
                    # Ждем появления модального окна или новой формы
                    print("⏳ Ждем появления модального окна...")
                    await self.browser_tool.page.wait_for_timeout(3000)
                    
                    # Ищем новые формы, которые могли появиться
                    modal_forms = await self.browser_tool.page.evaluate("""
                        () => Array.from(document.querySelectorAll('form')).map((form, index) => {
                            const inputs = Array.from(form.querySelectorAll('input, select, textarea')).map(input => ({
                                name: input.name || '',
                                type: input.type || 'text',
                                required: input.required || false,
                                placeholder: input.placeholder || ''
                            }));
                            
                            return {
                                index: index + 1,
                                action: form.action || '',
                                method: form.method || 'GET',
                                inputs: inputs,
                                form_text: form.textContent?.trim().substring(0, 200) || '',
                                nearby_text: form.parentElement?.textContent?.trim().substring(0, 300) || ''
                            };
                        })
                    """)
                    
                    print(f"📋 Найдено форм после клика: {len(modal_forms)}")
                    
                    # Проверяем новые формы
                    for form in modal_forms:
                        purpose = await self._classify_form_purpose(form)
                        if purpose in ['registration', 'login']:
                            print(f"✅ Найдена форма {purpose} в модальном окне")
                            auth_forms.append({
                                "form": form,
                                "purpose": purpose,
                                "source_url": "modal_window",
                                "confidence": 0.9,
                                "trigger_button": button_info['text']
                            })
                        
                        # Если форма входа, пробуем найти переключатель на регистрацию
                        if any(f['purpose'] == 'login' for f in auth_forms if f.get('source_url') == 'modal_window'):
                            print("🔄 Ищем переключатель на регистрацию...")
                            
                            # Ищем переключатели режимов
                            mode_switches = await self.browser_tool.page.evaluate("""
                                () => {
                                    const elements = Array.from(document.querySelectorAll('button, a, [role="button"], [role="tab"]'));
                                    return elements
                                        .filter(el => {
                                            const text = el.textContent.toLowerCase();
                                            return text.includes('sign up') || text.includes('register') || 
                                                   text.includes('create') || text.includes('join');
                                        })
                                        .map(el => ({
                                            text: el.textContent.trim(),
                                            tagName: el.tagName,
                                            className: el.className,
                                            href: el.href || '',
                                            role: el.getAttribute('role') || ''
                                        }));
                                }
                            """)
                            
                            # Пробуем переключиться на регистрацию
                            for switch in mode_switches:
                                if any(keyword in switch['text'].lower() for keyword in ['sign up', 'register', 'create']):
                                    print(f"🔄 Переключаемся на регистрацию: {switch['text']}")
                                    
                                    try:
                                        switch_selector = f"button:has-text('{switch['text']}')"
                                        if switch['tagName'] == 'A':
                                            switch_selector = f"a:has-text('{switch['text']}')"
                                        
                                        switch_element = await self.browser_tool.page.query_selector(switch_selector)
                                        if switch_element:
                                            await switch_element.click()
                                            await self.browser_tool.page.wait_for_timeout(2000)
                                            
                                            # Анализируем формы после переключения
                                            updated_forms = await self.browser_tool.page.evaluate("""
                                                () => Array.from(document.querySelectorAll('form')).map((form, index) => {
                                                    const inputs = Array.from(form.querySelectorAll('input, select, textarea')).map(input => ({
                                                        name: input.name || '',
                                                        type: input.type || 'text',
                                                        required: input.required || false,
                                                        placeholder: input.placeholder || ''
                                                    }));
                                                    
                                                    return {
                                                        index: index + 1,
                                                        action: form.action || '',
                                                        method: form.method || 'GET',
                                                        inputs: inputs,
                                                        form_text: form.textContent?.trim().substring(0, 200) || '',
                                                        nearby_text: form.parentElement?.textContent?.trim().substring(0, 300) || ''
                                                    };
                                                })
                                            """)
                                            
                                            for updated_form in updated_forms:
                                                updated_purpose = await self._classify_form_purpose(updated_form)
                                                if updated_purpose == 'registration':
                                                    print(f"✅ Найдена форма регистрации после переключения")
                                                    auth_forms.append({
                                                        "form": updated_form,
                                                        "purpose": updated_purpose,
                                                        "source_url": "modal_window",
                                                        "confidence": 0.95,
                                                        "trigger_button": button_info['text'],
                                                        "switch_button": switch['text']
                                                    })
                                                    break
                                            break
                                    except Exception as e:
                                        print(f"⚠️ Ошибка при переключении: {e}")
                                        continue
                        
                        # Закрываем модальное окно если оно есть
                        try:
                            close_button = await self.browser_tool.page.query_selector(
                                "button[aria-label*='close'], button[aria-label*='Close'], .close, [data-testid*='close']"
                            )
                            if close_button:
                                await close_button.click()
                                await self.browser_tool.page.wait_for_timeout(1000)
                        except:
                            pass
                
                except Exception as e:
                    print(f"⚠️ Ошибка при клике по кнопке {button_info['text']}: {e}")
                    continue
            
            # Переходим по найденным ссылкам и ищем формы
            for link in auth_links[:3]:  # Ограничиваем количество
                try:
                    await self.browser_tool.page.goto(link['href'])
                    await self.browser_tool.page.wait_for_load_state("networkidle", timeout=5000)
                    
                    page_forms = await self.browser_tool.page.evaluate("""
                        () => Array.from(document.querySelectorAll('form')).map((form, index) => {
                            const inputs = Array.from(form.querySelectorAll('input, select, textarea')).map(input => ({
                                name: input.name || '',
                                type: input.type || 'text',
                                required: input.required || false,
                                placeholder: input.placeholder || ''
                            }));
                            
                            return {
                                index: index + 1,
                                action: form.action || '',
                                method: form.method || 'GET',
                                inputs: inputs,
                                form_text: form.textContent?.trim().substring(0, 200) || ''
                            };
                        })
                    """)
                    
                    for form in page_forms:
                        purpose = await self._classify_form_purpose(form)
                        if purpose in ['registration', 'login']:
                            auth_forms.append({
                                "form": form,
                                "purpose": purpose,
                                "source_url": link['href'],
                                "confidence": 0.9
                            })
                
                except Exception as e:
                    print(f"⚠️ Ошибка при переходе по ссылке {link['href']}: {e}")
                    continue
        
        except Exception as e:
            print(f"⚠️ Ошибка при поиске форм аутентификации: {e}")
        
        return auth_forms
    
    async def _attempt_registration(self, auth_forms: List[Dict[str, Any]], persona: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """Попытка регистрации с использованием персоны"""
        
        registration_forms = [f for f in auth_forms if f['purpose'] == 'registration']
        
        if not registration_forms:
            return None
        
        print(f"👤 Попытка регистрации как {persona['name']}...")
        
        for form_data in registration_forms:
            try:
                form = form_data['form']
                source_url = form_data.get('source_url')
                trigger_button = form_data.get('trigger_button')
                switch_button = form_data.get('switch_button')
                
                # Если форма в модальном окне, нужно сначала открыть модальное окно
                if source_url == "modal_window" and trigger_button:
                    print(f"🔘 Открываем модальное окно через кнопку: {trigger_button}")
                    
                    # Создаем расширенный список селекторов для кнопки триггера
                    trigger_selectors = []
                    
                    if trigger_button:
                        trigger_selectors.extend([
                            f"button:has-text('{trigger_button}')",
                            f"[role='button']:has-text('{trigger_button}')",
                            f"div:has-text('{trigger_button}')",
                            f"a:has-text('{trigger_button}')",
                            f"span:has-text('{trigger_button}')"
                        ])
                    
                    # Добавляем общие селекторы
                    trigger_selectors.extend([
                        "[data-testid*='signup']",
                        "[data-testid*='register']",
                        "[aria-label*='sign up']",
                        "[aria-label*='register']",
                        "button[class*='signup']",
                        "button[class*='register']",
                        ".signup-btn",
                        ".register-btn",
                        "#signup",
                        "#register"
                    ])
                    
                    button_clicked = False
                    
                    for selector in trigger_selectors:
                        try:
                            elements = await self.browser_tool.page.query_selector_all(selector)
                            
                            for element in elements:
                                try:
                                    is_visible = await element.is_visible()
                                    is_enabled = await element.is_enabled()
                                    
                                    print(f"🔍 Триггер {selector}: видимый={is_visible}, активный={is_enabled}")
                                    
                                    if not is_visible:
                                        try:
                                            await element.scroll_into_view_if_needed()
                                            await self.browser_tool.page.wait_for_timeout(1000)
                                            is_visible = await element.is_visible()
                                            print(f"🔄 После скроллинга: видимый={is_visible}")
                                        except:
                                            pass
                                    
                                    if is_visible and is_enabled:
                                        print(f"✅ Кликаем по триггеру: {selector}")
                                        await element.click(timeout=5000)
                                        button_clicked = True
                                        break
                                    elif is_enabled:
                                        print(f"🔧 Принудительный клик по триггеру: {selector}")
                                        await element.click(force=True, timeout=5000)
                                        button_clicked = True
                                        break
                                    else:
                                        print(f"⚡ JavaScript клик по триггеру: {selector}")
                                        await element.evaluate("el => el.click()")
                                        button_clicked = True
                                        break
                                        
                                except Exception as click_error:
                                    print(f"⚠️ Ошибка клика по триггеру {selector}: {click_error}")
                                    continue
                            
                            if button_clicked:
                                break
                                
                        except Exception as selector_error:
                            print(f"⚠️ Ошибка селектора триггера {selector}: {selector_error}")
                            continue
                    
                    if not button_clicked:
                        print(f"❌ Не удалось найти или кликнуть кнопку триггер: {trigger_button}")
                        continue
                    
                    # Ждем появления модального окна
                    await self.browser_tool.page.wait_for_timeout(3000)
                        
                    # Если есть переключатель, кликаем по нему
                    if switch_button:
                        print(f"🔄 Переключаемся на регистрацию: {switch_button}")
                        
                        switch_selectors = []
                        
                        if switch_button:
                            switch_selectors.extend([
                                f"button:has-text('{switch_button}')",
                                f"a:has-text('{switch_button}')",
                                f"div:has-text('{switch_button}')",
                                f"span:has-text('{switch_button}')"
                            ])
                        
                        switch_selectors.extend([
                            "[data-testid*='switch']",
                            "[data-testid*='signup']",
                            "[data-testid*='register']",
                            "button[class*='switch']",
                            ".switch-btn"
                        ])
                        
                        switch_clicked = False
                        
                        for selector in switch_selectors:
                            try:
                                elements = await self.browser_tool.page.query_selector_all(selector)
                                
                                for element in elements:
                                    try:
                                        is_visible = await element.is_visible()
                                        is_enabled = await element.is_enabled()
                                        
                                        print(f"🔍 Переключатель {selector}: видимый={is_visible}, активный={is_enabled}")
                                        
                                        if not is_visible:
                                            try:
                                                await element.scroll_into_view_if_needed()
                                                await self.browser_tool.page.wait_for_timeout(1000)
                                                is_visible = await element.is_visible()
                                            except:
                                                pass
                                        
                                        if is_visible and is_enabled:
                                            print(f"✅ Кликаем по переключателю: {selector}")
                                            await element.click(timeout=5000)
                                            switch_clicked = True
                                            break
                                        elif is_enabled:
                                            print(f"🔧 Принудительный клик по переключателю: {selector}")
                                            await element.click(force=True, timeout=5000)
                                            switch_clicked = True
                                            break
                                        else:
                                            print(f"⚡ JavaScript клик по переключателю: {selector}")
                                            await element.evaluate("el => el.click()")
                                            switch_clicked = True
                                            break
                                            
                                    except Exception as click_error:
                                        print(f"⚠️ Ошибка клика по переключателю {selector}: {click_error}")
                                        continue
                                
                                if switch_clicked:
                                    break
                                    
                            except Exception as selector_error:
                                print(f"⚠️ Ошибка селектора переключателя {selector}: {selector_error}")
                                continue
                        
                        if not switch_clicked:
                            print(f"⚠️ Не удалось найти переключатель: {switch_button}")
                            # Продолжаем, возможно форма уже в режиме регистрации
                        else:
                            # Ждем после переключения
                            await self.browser_tool.page.wait_for_timeout(2000)
                
                elif source_url and source_url != "modal_window":
                    # Переходим на страницу с формой
                    await self.browser_tool.page.goto(source_url)
                    await self.browser_tool.page.wait_for_load_state("networkidle", timeout=5000)
                
                # Генерируем уникальные данные для регистрации
                test_data = self._generate_test_data(persona)
                
                # Заполняем форму
                fill_result = await self._fill_form_intelligently(form, test_data)
                
                if fill_result['success']:
                    # Пытаемся отправить форму
                    submit_result = await self._submit_form_safely(form)
                    
                    # Закрываем модальное окно если оно было открыто
                    if source_url == "modal_window":
                        try:
                            close_button = await self.browser_tool.page.query_selector(
                                "button[aria-label*='close'], button[aria-label*='Close'], .close, [data-testid*='close']"
                            )
                            if close_button:
                                await close_button.click()
                                await self.browser_tool.page.wait_for_timeout(1000)
                        except:
                            pass
                    
                    return {
                        "persona": persona['name'],
                        "form_url": source_url or "main_page",
                        "trigger_button": trigger_button,
                        "switch_button": switch_button,
                        "test_data": test_data,
                        "fill_result": fill_result,
                        "submit_result": submit_result,
                        "timestamp": datetime.now().isoformat()
                    }
            
            except Exception as e:
                print(f"⚠️ Ошибка при регистрации: {e}")
                continue
        
        return None
    
    def _generate_test_data(self, persona: Dict[str, Any]) -> Dict[str, str]:
        """Генерирует тестовые данные на основе персоны"""
        
        timestamp = int(time.time())
        random_suffix = ''.join(random.choices(string.ascii_lowercase + string.digits, k=6))
        
        return {
            "email": f"{persona['email_prefix']}.{timestamp}.{random_suffix}@testmail.com",
            "username": f"{persona['email_prefix']}_{random_suffix}",
            "password": "TestPass123!@#",
            "password_confirm": "TestPass123!@#",
            "first_name": persona['first_name'],
            "last_name": persona['last_name'],
            "name": f"{persona['first_name']} {persona['last_name']}",
            "full_name": f"{persona['first_name']} {persona['last_name']}",
            "age": persona['age'],
            "phone": persona['phone'],
            "address": persona['address'],
            "city": persona['city'],
            "country": persona['country'],
            "company": persona['company'],
            "zip": "12345",
            "postal_code": "12345",
            "state": "NY",
            "region": "New York"
        }
    
    async def _fill_form_intelligently(self, form: Dict[str, Any], test_data: Dict[str, str]) -> Dict[str, Any]:
        """Умное заполнение формы на основе анализа полей"""
        
        filled_fields = []
        errors = []
        
        try:
            inputs = form.get('inputs', [])
            
            for input_field in inputs:
                field_name = input_field.get('name', '').lower()
                field_type = input_field.get('type', 'text').lower()
                placeholder = input_field.get('placeholder', '').lower()
                
                # Определяем подходящее значение
                value = self._match_field_to_data(field_name, field_type, placeholder, test_data)
                
                if value:
                    try:
                        # Ищем поле на странице и заполняем его
                        selector = f"input[name='{input_field.get('name')}']"
                        if not input_field.get('name'):
                            selector = f"input[type='{field_type}']"
                        
                        element = await self.browser_tool.page.query_selector(selector)
                        if element:
                            await element.fill(value)
                            filled_fields.append({
                                "field": field_name,
                                "type": field_type,
                                "value": value[:20] + "..." if len(value) > 20 else value
                            })
                        
                    except Exception as e:
                        errors.append(f"Ошибка заполнения поля {field_name}: {e}")
            
            return {
                "success": len(filled_fields) > 0,
                "filled_fields": filled_fields,
                "errors": errors
            }
        
        except Exception as e:
            return {
                "success": False,
                "filled_fields": [],
                "errors": [f"Общая ошибка заполнения формы: {e}"]
            }
    
    def _match_field_to_data(self, field_name: str, field_type: str, placeholder: str, test_data: Dict[str, str]) -> Optional[str]:
        """Сопоставляет поле формы с подходящими тестовыми данными"""
        
        # Объединяем все подсказки
        field_hints = f"{field_name} {field_type} {placeholder}".lower()
        
        # Сопоставление по ключевым словам
        if any(keyword in field_hints for keyword in ['email', 'e-mail']):
            return test_data.get('email')
        elif any(keyword in field_hints for keyword in ['password', 'pass']):
            if 'confirm' in field_hints or 'repeat' in field_hints:
                return test_data.get('password_confirm')
            return test_data.get('password')
        elif any(keyword in field_hints for keyword in ['username', 'user', 'login']):
            return test_data.get('username')
        elif any(keyword in field_hints for keyword in ['first', 'fname']):
            return test_data.get('first_name')
        elif any(keyword in field_hints for keyword in ['last', 'lname', 'surname']):
            return test_data.get('last_name')
        elif any(keyword in field_hints for keyword in ['name']) and 'user' not in field_hints:
            return test_data.get('name')
        elif any(keyword in field_hints for keyword in ['phone', 'tel']):
            return test_data.get('phone')
        elif any(keyword in field_hints for keyword in ['address']):
            return test_data.get('address')
        elif any(keyword in field_hints for keyword in ['city']):
            return test_data.get('city')
        elif any(keyword in field_hints for keyword in ['country']):
            return test_data.get('country')
        elif any(keyword in field_hints for keyword in ['company', 'organization']):
            return test_data.get('company')
        elif any(keyword in field_hints for keyword in ['age']):
            return test_data.get('age')
        elif any(keyword in field_hints for keyword in ['zip', 'postal']):
            return test_data.get('zip')
        elif field_type == 'checkbox':
            return None  # Чекбоксы обрабатываем отдельно
        elif field_type == 'text' and not field_name:
            return "Test input"  # Общий текст для неопознанных полей
        
        return None
    
    async def _submit_form_safely(self, form: Dict[str, Any]) -> Dict[str, Any]:
        """Безопасная отправка формы с анализом результата"""
        
        try:
            # Ищем кнопку отправки
            submit_button = await self.browser_tool.page.query_selector(
                "input[type='submit'], button[type='submit'], button:has-text('Submit'), button:has-text('Register'), button:has-text('Sign up')"
            )
            
            if not submit_button:
                return {"success": False, "error": "Submit button not found"}
            
            # Сохраняем текущий URL
            current_url = self.browser_tool.page.url
            
            # Нажимаем кнопку отправки
            await submit_button.click()
            
            # Ждем изменения страницы или появления сообщений
            try:
                await self.browser_tool.page.wait_for_load_state("networkidle", timeout=10000)
            except:
                pass  # Таймаут не критичен
            
            new_url = self.browser_tool.page.url
            
            # Анализируем результат
            page_content = await self.browser_tool.page.content()
            
            # Ищем сообщения об ошибках или успехе
            success_indicators = ['success', 'welcome', 'registered', 'created', 'thank you']
            error_indicators = ['error', 'invalid', 'failed', 'required', 'already exists']
            
            content_lower = page_content.lower()
            
            has_success = any(indicator in content_lower for indicator in success_indicators)
            has_error = any(indicator in content_lower for indicator in error_indicators)
            
            return {
                "success": has_success and not has_error,
                "url_changed": current_url != new_url,
                "new_url": new_url,
                "has_success_message": has_success,
                "has_error_message": has_error,
                "response_analysis": "Form submitted successfully" if has_success else "Form submission may have failed"
            }
        
        except Exception as e:
            return {
                "success": False,
                "error": f"Form submission error: {e}"
            }
    
    async def _explore_all_forms(self, page_info: PageInfo) -> List[Dict[str, Any]]:
        """Исследует все формы на странице"""
        
        form_results = []
        
        for i, form in enumerate(page_info.forms):
            print(f"📝 Анализирую форму {i+1}/{len(page_info.forms)}...")
            
            form_purpose = await self._classify_form_purpose(form)
            
            # Генерируем подходящие тестовые данные
            if form_purpose == 'contact':
                test_data = self._generate_contact_data()
            elif form_purpose == 'search':
                test_data = self._generate_search_data()
            elif form_purpose == 'subscription':
                test_data = self._generate_subscription_data()
            else:
                test_data = self._generate_test_data(self.user_personas[0])
            
            # Заполняем и анализируем форму
            fill_result = await self._fill_form_intelligently(form, test_data)
            
            form_results.append({
                "form_index": i + 1,
                "purpose": form_purpose,
                "inputs_count": len(form.get('inputs', [])),
                "fill_result": fill_result,
                "test_data_used": test_data
            })
        
        return form_results
    
    def _generate_contact_data(self) -> Dict[str, str]:
        """Генерирует данные для контактных форм"""
        return {
            "name": "Test User",
            "email": f"testcontact.{int(time.time())}@example.com",
            "subject": "Test inquiry from automated testing",
            "message": "This is a test message generated by automated testing system. Please ignore.",
            "phone": "+1234567890",
            "company": "Test Company"
        }
    
    def _generate_search_data(self) -> Dict[str, str]:
        """Генерирует данные для поисковых форм"""
        search_terms = ["test", "example", "demo", "sample", "product"]
        return {
            "search": random.choice(search_terms),
            "query": random.choice(search_terms),
            "q": random.choice(search_terms)
        }
    
    def _generate_subscription_data(self) -> Dict[str, str]:
        """Генерирует данные для форм подписки"""
        return {
            "email": f"testsub.{int(time.time())}@example.com",
            "newsletter": "true"
        }
    
    async def _discover_hidden_functionality(self) -> List[Dict[str, Any]]:
        """Ищет скрытую функциональность на сайте"""
        
        hidden_features = []
        
        try:
            # Поиск скрытых элементов
            hidden_elements = await self.browser_tool.page.evaluate("""
                () => {
                    const elements = document.querySelectorAll('*');
                    const hidden = [];
                    
                    elements.forEach(el => {
                        const style = window.getComputedStyle(el);
                        if (style.display === 'none' || style.visibility === 'hidden' || 
                            style.opacity === '0' || el.hidden) {
                            if (el.tagName && el.innerHTML.length > 0) {
                                hidden.push({
                                    tag: el.tagName,
                                    id: el.id || '',
                                    class: el.className || '',
                                    content: el.innerHTML.substring(0, 100)
                                });
                            }
                        }
                    });
                    
                    return hidden.slice(0, 10); // Ограничиваем количество
                }
            """)
            
            if hidden_elements:
                hidden_features.append({
                    "type": "hidden_elements",
                    "count": len(hidden_elements),
                    "elements": hidden_elements
                })
            
            # Поиск комментариев в HTML
            html_comments = await self.browser_tool.page.evaluate("""
                () => {
                    const walker = document.createTreeWalker(
                        document.body,
                        NodeFilter.SHOW_COMMENT,
                        null,
                        false
                    );
                    
                    const comments = [];
                    let node;
                    
                    while (node = walker.nextNode()) {
                        if (node.nodeValue.trim().length > 5) {
                            comments.push(node.nodeValue.trim());
                        }
                    }
                    
                    return comments.slice(0, 5);
                }
            """)
            
            if html_comments:
                hidden_features.append({
                    "type": "html_comments",
                    "comments": html_comments
                })
            
            # Поиск data-атрибутов
            data_attributes = await self.browser_tool.page.evaluate("""
                () => {
                    const elements = document.querySelectorAll('[data-*]');
                    const dataAttrs = [];
                    
                    elements.forEach(el => {
                        Array.from(el.attributes).forEach(attr => {
                            if (attr.name.startsWith('data-')) {
                                dataAttrs.push({
                                    element: el.tagName,
                                    attribute: attr.name,
                                    value: attr.value
                                });
                            }
                        });
                    });
                    
                    return dataAttrs.slice(0, 10);
                }
            """)
            
            if data_attributes:
                hidden_features.append({
                    "type": "data_attributes",
                    "attributes": data_attributes
                })
        
        except Exception as e:
            hidden_features.append({
                "type": "error",
                "message": f"Error discovering hidden functionality: {e}"
            })
        
        return hidden_features
    
    async def _analyze_user_flows(self, page_info: PageInfo, max_depth: int) -> List[Dict[str, Any]]:
        """Анализирует возможные пользовательские потоки"""
        
        user_flows = []
        
        # Анализируем основные ссылки для построения потоков
        main_links = page_info.links[:10]  # Ограничиваем количество
        
        for link in main_links:
            try:
                if link.startswith('http') and 'javascript:' not in link:
                    flow_result = await self._trace_user_flow(link, max_depth=2)
                    if flow_result:
                        user_flows.append(flow_result)
            except Exception as e:
                continue
        
        return user_flows
    
    async def _trace_user_flow(self, start_url: str, max_depth: int) -> Optional[Dict[str, Any]]:
        """Отслеживает пользовательский поток начиная с URL"""
        
        try:
            await self.browser_tool.page.goto(start_url)
            await self.browser_tool.page.wait_for_load_state("networkidle", timeout=5000)
            
            page_title = await self.browser_tool.page.title()
            
            # Ищем интерактивные элементы
            interactive_elements = await self.browser_tool.page.evaluate("""
                () => {
                    const buttons = Array.from(document.querySelectorAll('button, input[type="button"], input[type="submit"]'));
                    const links = Array.from(document.querySelectorAll('a[href]')).slice(0, 5);
                    
                    return {
                        buttons: buttons.map(btn => ({
                            text: btn.textContent?.trim() || btn.value || '',
                            type: btn.type || 'button'
                        })).slice(0, 3),
                        links: links.map(link => ({
                            text: link.textContent?.trim() || '',
                            href: link.href
                        }))
                    };
                }
            """)
            
            return {
                "start_url": start_url,
                "page_title": page_title,
                "interactive_elements": interactive_elements,
                "depth_explored": 1
            }
        
        except Exception as e:
            return None
    
    async def _security_analysis(self) -> List[Dict[str, Any]]:
        """Анализ безопасности сайта"""
        
        security_findings = []
        
        try:
            # Проверка заголовков безопасности
            response = await self.browser_tool.page.evaluate("""
                async () => {
                    try {
                        const response = await fetch(window.location.href);
                        const headers = {};
                        for (let [key, value] of response.headers.entries()) {
                            headers[key] = value;
                        }
                        return headers;
                    } catch (e) {
                        return {};
                    }
                }
            """)
            
            # Проверяем важные заголовки безопасности
            security_headers = [
                'x-frame-options',
                'x-content-type-options',
                'x-xss-protection',
                'strict-transport-security',
                'content-security-policy'
            ]
            
            missing_headers = []
            for header in security_headers:
                if header not in response:
                    missing_headers.append(header)
            
            if missing_headers:
                security_findings.append({
                    "type": "missing_security_headers",
                    "severity": "medium",
                    "headers": missing_headers
                })
            
            # Проверка на наличие форм без CSRF защиты
            forms_without_csrf = await self.browser_tool.page.evaluate("""
                () => {
                    const forms = Array.from(document.querySelectorAll('form'));
                    return forms.filter(form => {
                        const csrfInput = form.querySelector('input[name*="csrf"], input[name*="token"]');
                        return !csrfInput && form.method.toLowerCase() === 'post';
                    }).length;
                }
            """)
            
            if forms_without_csrf > 0:
                security_findings.append({
                    "type": "forms_without_csrf",
                    "severity": "high",
                    "count": forms_without_csrf
                })
        
        except Exception as e:
            security_findings.append({
                "type": "security_analysis_error",
                "error": str(e)
            })
        
        return security_findings
    
    async def _performance_analysis(self) -> Dict[str, Any]:
        """Анализ производительности"""
        
        try:
            # Получаем метрики производительности
            performance_metrics = await self.browser_tool.page.evaluate("""
                () => {
                    const navigation = performance.getEntriesByType('navigation')[0];
                    const resources = performance.getEntriesByType('resource');
                    
                    return {
                        page_load_time: navigation ? navigation.loadEventEnd - navigation.fetchStart : 0,
                        dom_content_loaded: navigation ? navigation.domContentLoadedEventEnd - navigation.fetchStart : 0,
                        resources_count: resources.length,
                        largest_resource: resources.length > 0 ? Math.max(...resources.map(r => r.transferSize || 0)) : 0
                    };
                }
            """)
            
            return {
                "metrics": performance_metrics,
                "analysis": "Performance analysis completed",
                "recommendations": self._generate_performance_recommendations(performance_metrics)
            }
        
        except Exception as e:
            return {
                "error": f"Performance analysis failed: {e}"
            }
    
    def _generate_performance_recommendations(self, metrics: Dict[str, Any]) -> List[str]:
        """Генерирует рекомендации по производительности"""
        
        recommendations = []
        
        if metrics.get('page_load_time', 0) > 3000:
            recommendations.append("Page load time is over 3 seconds - consider optimization")
        
        if metrics.get('resources_count', 0) > 50:
            recommendations.append("High number of resources - consider bundling and minification")
        
        if metrics.get('largest_resource', 0) > 1000000:  # 1MB
            recommendations.append("Large resources detected - consider compression and lazy loading")
        
        return recommendations
    
    async def _save_exploration_report(self, report: Dict[str, Any]):
        """Сохраняет отчет об исследовании"""
        
        os.makedirs("exploration_reports", exist_ok=True)
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"exploration_reports/smart_exploration_{timestamp}.json"
        
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(report, f, ensure_ascii=False, indent=2)
        
        print(f"💾 Отчет сохранен: {filename}")
    
    async def _debug_page_elements(self, search_text: str = "sign up") -> None:
        """Отладочный метод для анализа элементов на странице"""
        try:
            print(f"🔍 Диагностика элементов с текстом '{search_text}'...")
            
            # Получаем информацию о всех потенциальных кнопках
            elements_info = await self.browser_tool.page.evaluate(f"""
                (searchText) => {{
                    const elements = Array.from(document.querySelectorAll('*'));
                    const matches = elements.filter(el => {{
                        const text = el.textContent?.toLowerCase() || '';
                        const ariaLabel = (el.getAttribute('aria-label') || '').toLowerCase();
                        const dataTestId = (el.getAttribute('data-testid') || '').toLowerCase();
                        return text.includes(searchText.toLowerCase()) || 
                               ariaLabel.includes(searchText.toLowerCase()) ||
                               dataTestId.includes('signup') || dataTestId.includes('register');
                    }});
                    
                    return matches.slice(0, 10).map(el => {{
                        const rect = el.getBoundingClientRect();
                        const style = window.getComputedStyle(el);
                        
                        return {{
                            tagName: el.tagName,
                            text: el.textContent?.trim().substring(0, 50) || '',
                            className: el.className || '',
                            id: el.id || '',
                            dataTestId: el.getAttribute('data-testid') || '',
                            ariaLabel: el.getAttribute('aria-label') || '',
                            visible: rect.width > 0 && rect.height > 0,
                            display: style.display,
                            visibility: style.visibility,
                            opacity: style.opacity,
                            zIndex: style.zIndex,
                            position: style.position,
                            top: rect.top,
                            left: rect.left,
                            width: rect.width,
                            height: rect.height,
                            inViewport: rect.top >= 0 && rect.left >= 0 && 
                                       rect.bottom <= window.innerHeight && 
                                       rect.right <= window.innerWidth
                        }};
                    }});
                }}
            """, search_text)
            
            print(f"📊 Найдено {len(elements_info)} потенциальных элементов:")
            for i, info in enumerate(elements_info):
                print(f"  {i+1}. {info['tagName']} - '{info['text']}'")
                print(f"     Видимый: {info['visible']}, В области просмотра: {info['inViewport']}")
                print(f"     CSS: display={info['display']}, visibility={info['visibility']}, opacity={info['opacity']}")
                print(f"     Позиция: ({info['left']}, {info['top']}) размер: {info['width']}x{info['height']}")
                if info['className']:
                    print(f"     Классы: {info['className']}")
                if info['dataTestId']:
                    print(f"     data-testid: {info['dataTestId']}")
                print()
                
        except Exception as e:
            print(f"⚠️ Ошибка при диагностике элементов: {e}") 