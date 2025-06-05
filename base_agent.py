import asyncio
from typing import Dict, List, Any, Optional
from langchain_openai import ChatOpenAI
from langchain.schema import HumanMessage, SystemMessage
from browser_tool import PlaywrightBrowserTool, PageInfo
from config import Config
import json
from datetime import datetime
import os

class WebAnalysisAgent:
    """Базовый агент для анализа веб-сайтов"""
    
    def __init__(self):
        Config.validate()
        self.llm = ChatOpenAI(
            temperature=0.1,
            api_key=Config.OPENAI_API_KEY,
            model="gpt-4o-mini"
        )
        self.browser_tool = PlaywrightBrowserTool()
        
    async def analyze_website(self, url: str) -> Dict[str, Any]:
        """Анализирует веб-сайт и возвращает подробный отчет"""
        
        print(f"🔍 Начинаю анализ сайта: {url}")
        
        async with self.browser_tool:
            # Шаг 1: Загружаем главную страницу
            main_page = await self.browser_tool.navigate_to_page(url)
            print(f"📄 Загружена главная страница: {main_page.title}")
            
            # Шаг 2: Анализируем структуру страницы с помощью AI
            structure_analysis = await self._analyze_page_structure(main_page)
            print("🏗️ Структура страницы проанализирована")
            
            # Шаг 3: Ищем потенциальные тест-кейсы
            test_cases = await self._identify_test_cases(main_page)
            print(f"🧪 Сгенерировано {len(test_cases)} тест-кейсов:")
            
            # Выводим краткую статистику по тест-кейсам
            high_priority = len([tc for tc in test_cases if tc.get("priority") == "high"])
            medium_priority = len([tc for tc in test_cases if tc.get("priority") == "medium"])
            low_priority = len([tc for tc in test_cases if tc.get("priority") == "low"])
            
            print(f"   📊 Приоритеты: {high_priority} высокий, {medium_priority} средний, {low_priority} низкий")
            
            # Показываем типы тест-кейсов
            test_types = {}
            for tc in test_cases:
                tc_type = tc.get("type", "unknown")
                test_types[tc_type] = test_types.get(tc_type, 0) + 1
            
            print(f"   🔍 Типы тестов: {', '.join([f'{k}({v})' for k, v in test_types.items()])}")
            
            # Если есть формы, показываем их анализ
            if main_page.forms:
                form_test = next((tc for tc in test_cases if tc.get("type") == "form_validation"), None)
                if form_test and "forms_summary" in form_test:
                    form_types = form_test["forms_summary"]["form_types"]
                    if form_types:
                        print(f"   📝 Типы форм: {', '.join([f'{k}({v})' for k, v in form_types.items()])}")
            
            total_time = self._calculate_total_testing_time(test_cases)
            if total_time != "0 minutes":
                print(f"   ⏱️ Ориентировочное время тестирования: {total_time}")
            
            # Шаг 4: Проверяем ссылки (первые 10 для демо)
            links_to_check = main_page.links[:10]
            broken_links = await self._check_links(links_to_check)
            print(f"🔗 Проверено {len(links_to_check)} ссылок, найдено {len(broken_links)} битых")
            
            # Шаг 5: Ищем потенциальные баги
            potential_bugs = await self._identify_potential_bugs(main_page)
            print(f"🐛 Найдено {len(potential_bugs)} потенциальных багов")
            
            # Формируем итоговый отчет
            report = {
                "url": url,
                "timestamp": datetime.now().isoformat(),
                "page_info": {
                    "title": main_page.title,
                    "status_code": main_page.status_code,
                    "load_time": main_page.load_time,
                    "links_count": len(main_page.links),
                    "images_count": len(main_page.images),
                    "forms_count": len(main_page.forms)
                },
                "structure_analysis": structure_analysis,
                "test_cases": {
                    "summary": {
                        "total_test_cases": len(test_cases),
                        "high_priority": len([tc for tc in test_cases if tc.get("priority") == "high"]),
                        "medium_priority": len([tc for tc in test_cases if tc.get("priority") == "medium"]),
                        "low_priority": len([tc for tc in test_cases if tc.get("priority") == "low"]),
                        "estimated_total_time": self._calculate_total_testing_time(test_cases)
                    },
                    "test_cases": test_cases
                },
                "broken_links": broken_links,
                "potential_bugs": potential_bugs,
                "errors": main_page.errors or []
            }
            
            # Сохраняем отчет
            await self._save_report(report)
            
            return report
    
    async def _analyze_page_structure(self, page_info: PageInfo) -> Dict[str, Any]:
        """Анализирует структуру страницы с помощью AI"""
        
        prompt = f"""
        Analyze the structure of this web page and provide detailed assessment:
        
        URL: {page_info.url}
        Title: {page_info.title}
        Links count: {len(page_info.links)}
        Images count: {len(page_info.images)}
        Forms count: {len(page_info.forms)}
        
        Meta tags: {json.dumps(page_info.meta_tags, ensure_ascii=False, indent=2)}
        
        Page content (first 2000 characters):
        {page_info.content[:2000]}
        
        Forms on page:
        {json.dumps(page_info.forms, ensure_ascii=False, indent=2)}
        
        Analyze:
        1. Site type (e-commerce, blog, corporate site, etc.)
        2. Main sections and functionality
        3. SEO quality (meta tags, structure)
        4. Accessibility issues
        5. Potential UX problems
        
        Respond in JSON format with keys: site_type, main_sections, seo_quality, accessibility_issues, ux_issues
        Use only English language for all descriptions and analysis.
        """
        
        messages = [
            SystemMessage(content="You are a web analysis and testing expert. Analyze sites thoroughly and professionally. Use English only."),
            HumanMessage(content=prompt)
        ]
        
        response = self.llm.invoke(messages)
        
        try:
            return json.loads(response.content)
        except json.JSONDecodeError:
            return {"analysis": response.content, "format": "text"}
    
    async def _identify_test_cases(self, page_info: PageInfo) -> List[Dict[str, Any]]:
        """Определяет потенциальные тест-кейсы"""
        
        test_cases = []
        
        # Группируем тест-кейсы для форм в один комплексный тест
        if page_info.forms:
            form_details = self._analyze_forms(page_info.forms)
            
            test_cases.append({
                "type": "form_validation",
                "title": f"Forms Validation Testing ({len(page_info.forms)} forms)",
                "description": f"Comprehensive validation testing for all {len(page_info.forms)} forms on the page",
                "forms_summary": form_details["summary"],
                "steps": self._generate_form_test_steps(form_details),
                "priority": "high" if form_details["has_required_fields"] else "medium",
                "estimated_time": f"{len(page_info.forms) * 5}-{len(page_info.forms) * 10} minutes",
                "forms_breakdown": form_details["breakdown"]
            })
        
        # Тест-кейсы для ссылок
        if page_info.links:
            link_categories = self._categorize_links(page_info.links)
            test_cases.append({
                "type": "navigation",
                "title": "Navigation and Links Testing",
                "description": f"Testing functionality of {len(page_info.links)} links across different categories",
                "link_categories": link_categories,
                "steps": [
                    "Test internal navigation links",
                    "Verify external links open correctly",
                    "Check anchor links functionality",
                    "Validate download links if present",
                    "Test social media links",
                    "Ensure all links have proper target attributes"
                ],
                "priority": "high",
                "estimated_time": f"{max(10, len(page_info.links) // 2)} minutes"
            })
        
        # Тест-кейсы для изображений
        if page_info.images:
            test_cases.append({
                "type": "media",
                "title": "Media Content and Accessibility Testing",
                "description": f"Testing {len(page_info.images)} images for loading, accessibility, and responsiveness",
                "steps": [
                    "Verify all images load correctly",
                    "Check alt-text presence and quality",
                    "Test image responsiveness on different screen sizes",
                    "Validate image file formats and sizes",
                    "Check lazy loading implementation if present"
                ],
                "priority": "medium",
                "estimated_time": f"{len(page_info.images) // 2 + 5} minutes"
            })
        
        # Добавляем тест-кейсы для производительности
        test_cases.append({
            "type": "performance",
            "title": "Page Performance Testing",
            "description": "Testing page loading speed and performance metrics",
            "steps": [
                "Measure page load time",
                "Check Core Web Vitals (LCP, FID, CLS)",
                "Test performance on different network speeds",
                "Analyze resource loading optimization",
                "Verify caching implementation"
            ],
            "priority": "medium",
            "estimated_time": "15-20 minutes"
        })
        
        # Добавляем тест-кейсы для доступности
        test_cases.append({
            "type": "accessibility",
            "title": "Accessibility (a11y) Testing",
            "description": "Testing website accessibility compliance",
            "steps": [
                "Check keyboard navigation",
                "Verify screen reader compatibility",
                "Test color contrast ratios",
                "Validate ARIA labels and roles",
                "Check focus indicators",
                "Test with accessibility tools (axe, WAVE)"
            ],
            "priority": "high",
            "estimated_time": "20-30 minutes"
        })
        
        # Используем AI для генерации дополнительных тест-кейсов
        ai_test_cases = await self._generate_ai_test_cases(page_info)
        test_cases.extend(ai_test_cases)
        
        return test_cases
    
    def _analyze_forms(self, forms: List[Dict]) -> Dict[str, Any]:
        """Анализирует формы и группирует их по типам с подробными описаниями"""
        
        form_types = {
            "login": [],
            "registration": [],
            "contact": [],
            "search": [],
            "newsletter": [],
            "shopping": [],
            "filter": [],
            "other": []
        }
        
        has_required_fields = False
        total_inputs = 0
        detailed_forms = []
        
        for i, form in enumerate(forms):
            form_info = {
                "index": i + 1,
                "action": form.get("action", "not specified"),
                "method": form.get("method", "GET"),
                "inputs": form.get("inputs", []),
                "buttons": form.get("buttons", []),
                "input_count": len(form.get("inputs", [])),
                "button_count": len(form.get("buttons", [])),
                "classes": form.get("classes", ""),
                "form_text": form.get("form_text", ""),
                "nearby_text": form.get("nearby_text", "")
            }
            
            total_inputs += form_info["input_count"]
            
            # Проверяем наличие обязательных полей
            if any(inp.get('required') for inp in form_info["inputs"]):
                has_required_fields = True
            
            # Определяем назначение формы и добавляем описание
            form_type, description = self._categorize_form_with_description(form_info)
            form_info["description"] = description
            form_info["purpose"] = self._determine_form_purpose(form_info)
            
            form_types[form_type].append(form_info)
            detailed_forms.append(form_info)
        
        return {
            "summary": {
                "total_forms": len(forms),
                "total_inputs": total_inputs,
                "form_types": {k: len(v) for k, v in form_types.items() if v},
                "forms_with_inputs": len([f for f in detailed_forms if f["input_count"] > 0]),
                "forms_with_buttons_only": len([f for f in detailed_forms if f["input_count"] == 0 and f["button_count"] > 0])
            },
            "has_required_fields": has_required_fields,
            "breakdown": form_types,
            "detailed_analysis": detailed_forms
        }
    
    def _categorize_form_with_description(self, form_info: Dict) -> tuple[str, str]:
        """Определяет тип формы и её описание по характеристикам"""
        
        action = form_info.get("action", "").lower()
        inputs = form_info.get("inputs", [])
        buttons = form_info.get("buttons", [])
        form_text = form_info.get("form_text", "").lower()
        nearby_text = form_info.get("nearby_text", "").lower()
        classes = form_info.get("classes", "").lower()
        
        # Анализируем поля формы
        input_types = [inp.get("type", "").lower() for inp in inputs]
        input_names = [inp.get("name", "").lower() for inp in inputs]
        button_texts = [btn.get("text", "").lower() for btn in buttons]
        
        # Определяем тип формы по различным признакам
        
        # Формы входа/логина
        if "password" in input_types:
            if any("confirm" in name or "repeat" in name for name in input_names):
                return "registration", "Registration form with password confirmation"
            else:
                return "login", "Login form with username/email and password"
        
        # Формы поиска
        if (any("search" in name or "query" in name or "q" == name for name in input_names) or
            any("search" in text for text in button_texts) or
            "search" in classes):
            return "search", "Search form for finding content"
        
        # Формы подписки на рассылку
        if ("email" in input_types and len(inputs) == 1) or "newsletter" in classes:
            return "newsletter", "Newsletter subscription form"
        
        # Формы обратной связи
        if (any("message" in name or "comment" in name for name in input_names) or
            any("textarea" == inp.get("type") for inp in inputs)):
            return "contact", "Contact or feedback form"
        
        # Формы фильтрации (часто встречаются в каталогах)
        if ("filter" in classes or "form-horizontal" in classes or
            any("filter" in text or "sort" in text for text in button_texts)):
            return "filter", "Filter or sorting form for catalog/listing"
        
        # Формы покупок/корзины
        if (any("add to basket" in text or "add to cart" in text or "buy" in text for text in button_texts) or
            any("basket" in text or "cart" in text for text in button_texts)):
            return "shopping", f"Shopping form - {button_texts[0] if button_texts else 'Add to cart'}"
        
        # Если форма содержит только кнопки без полей ввода
        if len(inputs) == 0 and len(buttons) > 0:
            button_text = button_texts[0] if button_texts else "button action"
            return "other", f"Action form with button: '{button_text}'"
        
        # Общие формы
        if len(inputs) > 0:
            return "other", f"Form with {len(inputs)} input field(s)"
        
        return "other", "Form without clear purpose"
    
    def _determine_form_purpose(self, form_info: Dict) -> str:
        """Определяет назначение формы на основе контекста"""
        
        buttons = form_info.get("buttons", [])
        inputs = form_info.get("inputs", [])
        form_text = form_info.get("form_text", "")
        nearby_text = form_info.get("nearby_text", "")
        
        # Если есть кнопки, используем их текст для определения назначения
        if buttons:
            button_text = buttons[0].get("text", "")
            if button_text:
                return f"Purpose: {button_text}"
        
        # Если есть поля ввода, анализируем их
        if inputs:
            input_types = [inp.get("type", "") for inp in inputs]
            if "email" in input_types:
                return "Purpose: Email-related action"
            if "password" in input_types:
                return "Purpose: Authentication"
            if len(inputs) == 1 and inputs[0].get("type") == "text":
                placeholder = inputs[0].get("placeholder", "")
                if placeholder:
                    return f"Purpose: {placeholder}"
        
        # Анализируем текст формы
        if "search" in form_text.lower():
            return "Purpose: Search functionality"
        
        return "Purpose: General form interaction"
    
    def _generate_form_test_steps(self, form_details: Dict) -> List[str]:
        """Генерирует шаги тестирования для форм с учетом их типов и назначения"""
        
        steps = [
            "Identify and catalog all forms on the page",
            "Test form submission with valid data",
            "Test form validation with invalid/empty data"
        ]
        
        breakdown = form_details["breakdown"]
        summary = form_details["summary"]
        
        # Добавляем информацию о типах форм
        if summary.get("forms_with_buttons_only", 0) > 0:
            steps.append(f"Test {summary['forms_with_buttons_only']} button-only forms (action forms)")
        
        if breakdown["login"]:
            steps.extend([
                f"Test login forms ({len(breakdown['login'])} forms): valid/invalid credentials",
                "Test password visibility toggle if present",
                "Test 'Remember me' functionality if present"
            ])
        
        if breakdown["registration"]:
            steps.extend([
                f"Test registration forms ({len(breakdown['registration'])} forms): password confirmation",
                "Test email format validation",
                "Test username availability if applicable"
            ])
        
        if breakdown["contact"]:
            steps.extend([
                f"Test contact forms ({len(breakdown['contact'])} forms): required field validation",
                "Test message length limits",
                "Test email notification functionality"
            ])
        
        if breakdown["search"]:
            steps.extend([
                f"Test search forms ({len(breakdown['search'])} forms): empty search",
                "Test search with special characters",
                "Test search results functionality"
            ])
        
        if breakdown["newsletter"]:
            steps.extend([
                f"Test newsletter forms ({len(breakdown['newsletter'])} forms): email validation",
                "Test subscription confirmation process"
            ])
        
        if breakdown["shopping"]:
            steps.extend([
                f"Test shopping forms ({len(breakdown['shopping'])} forms): add to cart functionality",
                "Test quantity selection if available",
                "Test cart update and removal",
                "Verify product information is correctly passed"
            ])
        
        if breakdown["filter"]:
            steps.extend([
                f"Test filter forms ({len(breakdown['filter'])} forms): filter application",
                "Test filter combinations",
                "Test filter reset functionality"
            ])
        
        if breakdown["other"]:
            steps.append(f"Test other forms ({len(breakdown['other'])} forms): custom validation rules")
        
        steps.extend([
            "Test form accessibility (keyboard navigation, screen readers)",
            "Test form responsiveness on different screen sizes",
            "Verify CSRF protection if applicable"
        ])
        
        return steps
    
    def _categorize_links(self, links: List[str]) -> Dict[str, List[str]]:
        """Категоризирует ссылки по типам"""
        
        categories = {
            "internal": [],
            "external": [],
            "anchor": [],
            "download": [],
            "social": [],
            "email": [],
            "phone": []
        }
        
        social_domains = ["facebook.com", "twitter.com", "instagram.com", "linkedin.com", "youtube.com", "tiktok.com"]
        
        for link in links:
            link_lower = link.lower()
            
            if link.startswith("#"):
                categories["anchor"].append(link)
            elif link.startswith("mailto:"):
                categories["email"].append(link)
            elif link.startswith("tel:"):
                categories["phone"].append(link)
            elif any(domain in link_lower for domain in social_domains):
                categories["social"].append(link)
            elif link_lower.endswith(('.pdf', '.doc', '.docx', '.zip', '.rar')):
                categories["download"].append(link)
            elif link.startswith("http") and not any(domain in link_lower for domain in ["localhost", "127.0.0.1"]):
                categories["external"].append(link)
            else:
                categories["internal"].append(link)
        
        # Удаляем пустые категории
        return {k: v for k, v in categories.items() if v}
    
    async def _generate_ai_test_cases(self, page_info: PageInfo) -> List[Dict[str, Any]]:
        """Генерирует тест-кейсы с помощью AI"""
        
        # Подготавливаем контекст для более точного анализа
        context_info = {
            "title": page_info.title,
            "forms_count": len(page_info.forms),
            "links_count": len(page_info.links),
            "images_count": len(page_info.images),
            "has_errors": bool(page_info.errors),
            "load_time": page_info.load_time
        }
        
        prompt = f"""
        Based on the detailed analysis of this web page, suggest 1-2 SPECIFIC and UNIQUE test cases that are NOT covered by standard form/navigation/media testing.

        Website: {page_info.title}
        URL: {page_info.url}
        Context: {json.dumps(context_info, indent=2)}

        Page content sample (analyze for specific functionality):
        {page_info.content[:1500]}

        IMPORTANT REQUIREMENTS:
        1. Focus on SPECIFIC functionality visible in the content
        2. Avoid generic test cases (no basic form/link/image testing)
        3. Look for unique features like: shopping carts, user profiles, search filters, interactive elements, etc.
        4. Consider the website type and industry-specific testing needs
        5. Each test case should be actionable and specific to THIS website

        RESPONSE FORMAT - Return ONLY valid JSON array:
        [
            {{
                "type": "specific_functionality_type",
                "title": "Specific Test Case Title",
                "description": "Detailed description of what makes this test unique to this site",
                "steps": ["specific step 1", "specific step 2", "specific step 3"],
                "priority": "medium",
                "rationale": "Why this test is important for THIS specific website"
            }}
        ]

        If no specific functionality is found, return exactly: []

        CRITICAL: Return ONLY the JSON array, no additional text or explanations.
        """
        
        messages = [
            SystemMessage(content="You are a senior QA engineer specializing in website-specific testing. Focus on unique functionality rather than generic tests. Be selective and only suggest tests that add real value. CRITICAL: Always respond with valid JSON format only, no additional text."),
            HumanMessage(content=prompt)
        ]
        
        try:
            response = self.llm.invoke(messages)
            response_content = response.content.strip()
            
            # Попытка извлечь JSON из ответа
            json_content = response_content
            
            # Если ответ содержит markdown блоки кода, извлекаем JSON
            if "```json" in response_content:
                json_start = response_content.find("```json") + 7
                json_end = response_content.find("```", json_start)
                if json_end != -1:
                    json_content = response_content[json_start:json_end].strip()
            elif "```" in response_content:
                json_start = response_content.find("```") + 3
                json_end = response_content.find("```", json_start)
                if json_end != -1:
                    json_content = response_content[json_start:json_end].strip()
            
            # Если ответ начинается не с [ или {, ищем первое вхождение
            if not json_content.startswith(('[', '{')):
                bracket_pos = json_content.find('[')
                brace_pos = json_content.find('{')
                if bracket_pos != -1 and (brace_pos == -1 or bracket_pos < brace_pos):
                    json_content = json_content[bracket_pos:]
                elif brace_pos != -1:
                    json_content = json_content[brace_pos:]
            
            ai_test_cases = json.loads(json_content)
            
            # Валидируем и фильтруем результаты
            validated_cases = []
            for case in ai_test_cases:
                if self._validate_test_case(case):
                    validated_cases.append(case)
            
            return validated_cases
            
        except json.JSONDecodeError as e:
            print(f"⚠️ AI test case generation failed - invalid JSON response")
            print(f"   Debug: JSON error at position {e.pos}: {e.msg}")
            print(f"   Response preview: {response.content[:200]}...")
            return []
        except Exception as e:
            print(f"⚠️ AI test case generation error: {str(e)}")
            return []
    
    def _validate_test_case(self, test_case: Dict[str, Any]) -> bool:
        """Валидирует тест-кейс на корректность и уникальность"""
        
        required_fields = ["type", "title", "description", "steps", "priority"]
        
        # Проверяем наличие обязательных полей
        if not all(field in test_case for field in required_fields):
            return False
        
        # Проверяем, что это не дублирующий тест-кейс
        generic_keywords = [
            "form validation", "link testing", "image loading", 
            "navigation testing", "basic functionality"
        ]
        
        title_lower = test_case["title"].lower()
        description_lower = test_case["description"].lower()
        
        # Отклоняем слишком общие тест-кейсы
        if any(keyword in title_lower or keyword in description_lower for keyword in generic_keywords):
            return False
        
        # Проверяем, что есть конкретные шаги
        if len(test_case["steps"]) < 2:
            return False
        
        return True
    
    async def _check_links(self, links: List[str]) -> List[Dict[str, Any]]:
        """Проверяет ссылки на работоспособность"""
        
        broken_links = []
        
        for link in links:
            try:
                result = await self.browser_tool.check_link(link)
                if result["status"] == "error" or (result["status_code"] and result["status_code"] >= 400):
                    broken_links.append(result)
                    
                # Добавляем небольшую задержку между запросами
                await asyncio.sleep(0.5)
                
            except Exception as e:
                broken_links.append({
                    "url": link,
                    "status": "error",
                    "error": str(e)
                })
        
        return broken_links
    
    async def _identify_potential_bugs(self, page_info: PageInfo) -> List[Dict[str, Any]]:
        """Ищет потенциальные баги на странице"""
        
        bugs = []
        
        # Проверяем отсутствие заголовка
        if not page_info.title or len(page_info.title.strip()) == 0:
            bugs.append({
                "type": "seo",
                "severity": "medium",
                "description": "Missing page title",
                "recommendation": "Add descriptive page title"
            })
        
        # Проверяем мета-описание
        if "description" not in page_info.meta_tags:
            bugs.append({
                "type": "seo",
                "severity": "low",
                "description": "Missing meta description",
                "recommendation": "Add meta description tag"
            })
        
        # Проверяем формы без action
        for i, form in enumerate(page_info.forms):
            if not form.get("action"):
                bugs.append({
                    "type": "functionality",
                    "severity": "high",
                    "description": f"Form #{i+1} missing action attribute",
                    "recommendation": "Specify URL for form processing"
                })
        
        # Проверяем время загрузки
        if page_info.load_time and page_info.load_time > 3.0:
            bugs.append({
                "type": "performance",
                "severity": "medium",
                "description": f"Slow page loading: {page_info.load_time:.2f}s",
                "recommendation": "Optimize page loading speed"
            })
        
        # Используем AI для поиска дополнительных проблем
        ai_bugs = await self._ai_bug_detection(page_info)
        bugs.extend(ai_bugs)
        
        return bugs
    
    async def _ai_bug_detection(self, page_info: PageInfo) -> List[Dict[str, Any]]:
        """Использует AI для поиска потенциальных багов"""
        
        prompt = f"""
        Analyze this web page for potential bugs and issues:
        
        Title: {page_info.title}
        Status code: {page_info.status_code}
        Load time: {page_info.load_time}
        Errors: {page_info.errors}
        
        Find potential problems and return them in JSON format:
        [
            {{
                "type": "issue_type",
                "severity": "high/medium/low",
                "description": "problem description",
                "recommendation": "fix recommendation"
            }}
        ]
        
        Use only English language for all descriptions and recommendations.
        """
        
        messages = [
            SystemMessage(content="You are a web testing expert. Find real problems and bugs. Use English only."),
            HumanMessage(content=prompt)
        ]
        
        response = self.llm.invoke(messages)
        
        try:
            return json.loads(response.content)
        except json.JSONDecodeError:
            return []
    
    async def _save_report(self, report: Dict[str, Any]):
        """Сохраняет отчет в файл"""
        
        # Создаем директорию для отчетов
        os.makedirs(Config.REPORTS_DIR, exist_ok=True)
        
        # Генерируем имя файла
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        domain = report["url"].replace("https://", "").replace("http://", "").replace("/", "_")
        filename = f"{Config.REPORTS_DIR}/report_{domain}_{timestamp}.json"
        
        # Сохраняем отчет
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(report, f, ensure_ascii=False, indent=2)
        
        print(f"📊 Отчет сохранен: {filename}")
        
        return filename
    
    def _calculate_total_testing_time(self, test_cases: List[Dict[str, Any]]) -> str:
        """Вычисляет общее время тестирования"""
        
        total_min_minutes = 0
        total_max_minutes = 0
        
        for test_case in test_cases:
            estimated_time = test_case.get("estimated_time", "")
            if estimated_time:
                # Парсим время вида "15-20 minutes" или "10 minutes"
                if "-" in estimated_time:
                    try:
                        min_time, max_time = estimated_time.split("-")
                        total_min_minutes += int(min_time.strip())
                        total_max_minutes += int(max_time.split()[0].strip())
                    except:
                        pass
                else:
                    try:
                        time_value = int(estimated_time.split()[0])
                        total_min_minutes += time_value
                        total_max_minutes += time_value
                    except:
                        pass
        
        if total_min_minutes == total_max_minutes:
            return f"{total_min_minutes} minutes"
        else:
            return f"{total_min_minutes}-{total_max_minutes} minutes" 