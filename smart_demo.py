#!/usr/bin/env python3
"""
Демонстрация умного агента для глубокого исследования веб-сайтов
"""

import asyncio
import sys
from smart_exploration_agent import SmartExplorationAgent
from datetime import datetime

def print_banner():
    """Выводит красивый баннер"""
    print("=" * 80)
    print("🤖 УМНЫЙ АГЕНТ ДЛЯ ГЛУБОКОГО ИССЛЕДОВАНИЯ ВЕБ-САЙТОВ")
    print("=" * 80)
    print("🚀 Возможности:")
    print("   • Автоматическая регистрация с разными персонами")
    print("   • Интеллектуальное заполнение форм")
    print("   • Поиск скрытой функциональности")
    print("   • Анализ безопасности и производительности")
    print("   • Исследование пользовательских потоков")
    print("=" * 80)
    print()

def get_demo_sites():
    """Возвращает список демонстрационных сайтов"""
    return {
        "1": {
            "name": "HTTPBin Forms",
            "url": "https://httpbin.org/forms/post",
            "description": "Сайт с различными формами для тестирования",
            "features": ["Формы", "POST запросы", "Валидация"]
        },
        "2": {
            "name": "Books to Scrape",
            "url": "http://books.toscrape.com",
            "description": "E-commerce сайт с книгами",
            "features": ["Каталог", "Поиск", "Навигация"]
        },
        "3": {
            "name": "Example.com",
            "url": "https://example.com",
            "description": "Простой демонстрационный сайт",
            "features": ["Базовая структура", "Простота"]
        },
        "4": {
            "name": "JSONPlaceholder",
            "url": "https://jsonplaceholder.typicode.com",
            "description": "API для тестирования",
            "features": ["REST API", "JSON", "Тестовые данные"]
        }
    }

def display_demo_sites():
    """Отображает доступные демонстрационные сайты"""
    sites = get_demo_sites()
    
    print("🌐 Доступные демонстрационные сайты:")
    print("-" * 50)
    
    for key, site in sites.items():
        print(f"{key}. {site['name']}")
        print(f"   URL: {site['url']}")
        print(f"   Описание: {site['description']}")
        print(f"   Особенности: {', '.join(site['features'])}")
        print()
    
    print("5. Ввести свой URL")
    print()

def get_user_choice():
    """Получает выбор пользователя"""
    while True:
        try:
            choice = input("Выберите сайт для исследования (1-5): ").strip()
            if choice in ['1', '2', '3', '4', '5']:
                return choice
            else:
                print("❌ Пожалуйста, выберите число от 1 до 5")
        except KeyboardInterrupt:
            print("\n👋 До свидания!")
            sys.exit(0)

def get_custom_url():
    """Получает пользовательский URL"""
    while True:
        try:
            url = input("Введите URL для исследования: ").strip()
            if url:
                if not url.startswith(('http://', 'https://')):
                    url = 'https://' + url
                return url
            else:
                print("❌ URL не может быть пустым")
        except KeyboardInterrupt:
            print("\n👋 До свидания!")
            sys.exit(0)

def get_exploration_depth():
    """Получает глубину исследования"""
    while True:
        try:
            depth = input("Глубина исследования (1-5, по умолчанию 3): ").strip()
            if not depth:
                return 3
            depth = int(depth)
            if 1 <= depth <= 5:
                return depth
            else:
                print("❌ Глубина должна быть от 1 до 5")
        except ValueError:
            print("❌ Введите число от 1 до 5")
        except KeyboardInterrupt:
            print("\n👋 До свидания!")
            sys.exit(0)

async def run_smart_exploration(url: str, depth: int):
    """Запускает умное исследование сайта"""
    
    print(f"🚀 Начинаю умное исследование сайта: {url}")
    print(f"📊 Глубина исследования: {depth}")
    print(f"⏰ Время начала: {datetime.now().strftime('%H:%M:%S')}")
    print("-" * 80)
    
    try:
        # Создаем агента
        agent = SmartExplorationAgent()
        
        # Запускаем исследование
        report = await agent.deep_explore_website(url, max_depth=depth)
        
        print("-" * 80)
        print("✅ ИССЛЕДОВАНИЕ ЗАВЕРШЕНО!")
        print("-" * 80)
        
        # Выводим краткую статистику
        print_exploration_summary(report)
        
        return report
        
    except Exception as e:
        print(f"❌ Ошибка при исследовании: {e}")
        return None

def print_exploration_summary(report: dict):
    """Выводит краткую сводку по исследованию"""
    
    print("📊 КРАТКАЯ СВОДКА:")
    print(f"   🌐 URL: {report.get('url', 'N/A')}")
    print(f"   📄 Обнаружено форм аутентификации: {report.get('auth_forms_discovered', 0)}")
    print(f"   👥 Попыток регистрации: {len(report.get('registration_attempts', []))}")
    print(f"   📝 Форм протестировано: {len(report.get('form_interactions', []))}")
    print(f"   🕵️ Скрытых функций найдено: {len(report.get('hidden_functionality', []))}")
    print(f"   🛤️ Пользовательских потоков: {len(report.get('user_flows', []))}")
    print(f"   🔒 Проблем безопасности: {len(report.get('security_findings', []))}")
    
    # Детали по регистрации
    reg_attempts = report.get('registration_attempts', [])
    if reg_attempts:
        print("\n👥 ПОПЫТКИ РЕГИСТРАЦИИ:")
        for attempt in reg_attempts:
            persona = attempt.get('persona', 'Unknown')
            success = attempt.get('submit_result', {}).get('success', False)
            status = "✅ Успешно" if success else "❌ Неудачно"
            print(f"   • {persona}: {status}")
    
    # Детали по формам
    form_interactions = report.get('form_interactions', [])
    if form_interactions:
        print("\n📝 АНАЛИЗ ФОРМ:")
        for form in form_interactions:
            purpose = form.get('purpose', 'unknown')
            filled = len(form.get('fill_result', {}).get('filled_fields', []))
            print(f"   • Форма {form.get('form_index', '?')} ({purpose}): заполнено {filled} полей")
    
    # Проблемы безопасности
    security_findings = report.get('security_findings', [])
    if security_findings:
        print("\n🔒 ПРОБЛЕМЫ БЕЗОПАСНОСТИ:")
        for finding in security_findings:
            finding_type = finding.get('type', 'unknown')
            severity = finding.get('severity', 'unknown')
            print(f"   • {finding_type} (серьезность: {severity})")
    
    # Скрытая функциональность
    hidden_functionality = report.get('hidden_functionality', [])
    if hidden_functionality:
        print("\n🕵️ СКРЫТАЯ ФУНКЦИОНАЛЬНОСТЬ:")
        for feature in hidden_functionality:
            feature_type = feature.get('type', 'unknown')
            if feature_type == 'hidden_elements':
                count = feature.get('count', 0)
                print(f"   • Скрытых элементов: {count}")
            elif feature_type == 'html_comments':
                count = len(feature.get('comments', []))
                print(f"   • HTML комментариев: {count}")
            elif feature_type == 'data_attributes':
                count = len(feature.get('attributes', []))
                print(f"   • Data-атрибутов: {count}")

def show_detailed_results_menu(report: dict):
    """Показывает меню для просмотра детальных результатов"""
    
    while True:
        print("\n" + "=" * 50)
        print("📋 ДЕТАЛЬНЫЕ РЕЗУЛЬТАТЫ")
        print("=" * 50)
        print("1. Анализ главной страницы")
        print("2. Попытки регистрации")
        print("3. Взаимодействие с формами")
        print("4. Скрытая функциональность")
        print("5. Пользовательские потоки")
        print("6. Анализ безопасности")
        print("7. Анализ производительности")
        print("8. Полный JSON отчет")
        print("9. Вернуться в главное меню")
        print()
        
        try:
            choice = input("Выберите раздел (1-9): ").strip()
            
            if choice == '1':
                show_main_page_analysis(report)
            elif choice == '2':
                show_registration_attempts(report)
            elif choice == '3':
                show_form_interactions(report)
            elif choice == '4':
                show_hidden_functionality(report)
            elif choice == '5':
                show_user_flows(report)
            elif choice == '6':
                show_security_analysis(report)
            elif choice == '7':
                show_performance_analysis(report)
            elif choice == '8':
                show_full_json_report(report)
            elif choice == '9':
                break
            else:
                print("❌ Выберите число от 1 до 9")
                
        except KeyboardInterrupt:
            print("\n👋 До свидания!")
            sys.exit(0)

def show_main_page_analysis(report: dict):
    """Показывает анализ главной страницы"""
    analysis = report.get('main_page_analysis', {})
    
    print("\n🔍 АНАЛИЗ ГЛАВНОЙ СТРАНИЦЫ:")
    print("-" * 40)
    
    if isinstance(analysis, dict):
        for key, value in analysis.items():
            print(f"{key}: {value}")
    else:
        print(analysis)
    
    input("\nНажмите Enter для продолжения...")

def show_registration_attempts(report: dict):
    """Показывает попытки регистрации"""
    attempts = report.get('registration_attempts', [])
    
    print("\n👥 ПОПЫТКИ РЕГИСТРАЦИИ:")
    print("-" * 40)
    
    if not attempts:
        print("Попыток регистрации не было")
    else:
        for i, attempt in enumerate(attempts, 1):
            print(f"\n{i}. Персона: {attempt.get('persona', 'Unknown')}")
            print(f"   URL формы: {attempt.get('form_url', 'N/A')}")
            
            fill_result = attempt.get('fill_result', {})
            filled_fields = fill_result.get('filled_fields', [])
            print(f"   Заполнено полей: {len(filled_fields)}")
            
            for field in filled_fields:
                print(f"     • {field.get('field', 'unknown')}: {field.get('value', 'N/A')}")
            
            submit_result = attempt.get('submit_result', {})
            success = submit_result.get('success', False)
            print(f"   Результат отправки: {'✅ Успешно' if success else '❌ Неудачно'}")
    
    input("\nНажмите Enter для продолжения...")

def show_form_interactions(report: dict):
    """Показывает взаимодействие с формами"""
    interactions = report.get('form_interactions', [])
    
    print("\n📝 ВЗАИМОДЕЙСТВИЕ С ФОРМАМИ:")
    print("-" * 40)
    
    if not interactions:
        print("Форм для взаимодействия не найдено")
    else:
        for interaction in interactions:
            form_index = interaction.get('form_index', '?')
            purpose = interaction.get('purpose', 'unknown')
            inputs_count = interaction.get('inputs_count', 0)
            
            print(f"\nФорма {form_index} ({purpose}):")
            print(f"   Полей ввода: {inputs_count}")
            
            fill_result = interaction.get('fill_result', {})
            filled_fields = fill_result.get('filled_fields', [])
            errors = fill_result.get('errors', [])
            
            print(f"   Заполнено полей: {len(filled_fields)}")
            if errors:
                print(f"   Ошибок: {len(errors)}")
    
    input("\nНажмите Enter для продолжения...")

def show_hidden_functionality(report: dict):
    """Показывает скрытую функциональность"""
    hidden = report.get('hidden_functionality', [])
    
    print("\n🕵️ СКРЫТАЯ ФУНКЦИОНАЛЬНОСТЬ:")
    print("-" * 40)
    
    if not hidden:
        print("Скрытой функциональности не обнаружено")
    else:
        for feature in hidden:
            feature_type = feature.get('type', 'unknown')
            print(f"\n• {feature_type.upper()}:")
            
            if feature_type == 'hidden_elements':
                elements = feature.get('elements', [])
                print(f"  Найдено скрытых элементов: {len(elements)}")
                for elem in elements[:3]:  # Показываем первые 3
                    print(f"    - {elem.get('tag', 'unknown')} (class: {elem.get('class', 'none')})")
            
            elif feature_type == 'html_comments':
                comments = feature.get('comments', [])
                print(f"  Найдено комментариев: {len(comments)}")
                for comment in comments[:3]:  # Показываем первые 3
                    print(f"    - {comment[:50]}...")
            
            elif feature_type == 'data_attributes':
                attributes = feature.get('attributes', [])
                print(f"  Найдено data-атрибутов: {len(attributes)}")
                for attr in attributes[:3]:  # Показываем первые 3
                    print(f"    - {attr.get('attribute', 'unknown')}: {attr.get('value', 'N/A')}")
    
    input("\nНажмите Enter для продолжения...")

def show_user_flows(report: dict):
    """Показывает пользовательские потоки"""
    flows = report.get('user_flows', [])
    
    print("\n🛤️ ПОЛЬЗОВАТЕЛЬСКИЕ ПОТОКИ:")
    print("-" * 40)
    
    if not flows:
        print("Пользовательских потоков не обнаружено")
    else:
        for i, flow in enumerate(flows, 1):
            print(f"\n{i}. {flow.get('page_title', 'Без названия')}")
            print(f"   URL: {flow.get('start_url', 'N/A')}")
            
            interactive = flow.get('interactive_elements', {})
            buttons = interactive.get('buttons', [])
            links = interactive.get('links', [])
            
            print(f"   Кнопок: {len(buttons)}")
            print(f"   Ссылок: {len(links)}")
    
    input("\nНажмите Enter для продолжения...")

def show_security_analysis(report: dict):
    """Показывает анализ безопасности"""
    security = report.get('security_findings', [])
    
    print("\n🔒 АНАЛИЗ БЕЗОПАСНОСТИ:")
    print("-" * 40)
    
    if not security:
        print("Проблем безопасности не обнаружено")
    else:
        for finding in security:
            finding_type = finding.get('type', 'unknown')
            severity = finding.get('severity', 'unknown')
            
            print(f"\n• {finding_type.upper()} (серьезность: {severity})")
            
            if finding_type == 'missing_security_headers':
                headers = finding.get('headers', [])
                print(f"  Отсутствующие заголовки: {', '.join(headers)}")
            
            elif finding_type == 'forms_without_csrf':
                count = finding.get('count', 0)
                print(f"  Форм без CSRF защиты: {count}")
    
    input("\nНажмите Enter для продолжения...")

def show_performance_analysis(report: dict):
    """Показывает анализ производительности"""
    performance = report.get('performance_insights', {})
    
    print("\n⚡ АНАЛИЗ ПРОИЗВОДИТЕЛЬНОСТИ:")
    print("-" * 40)
    
    metrics = performance.get('metrics', {})
    if metrics:
        load_time = metrics.get('page_load_time', 0)
        dom_loaded = metrics.get('dom_content_loaded', 0)
        resources = metrics.get('resources_count', 0)
        
        print(f"Время загрузки страницы: {load_time:.2f} мс")
        print(f"DOM загружен за: {dom_loaded:.2f} мс")
        print(f"Количество ресурсов: {resources}")
        
        recommendations = performance.get('recommendations', [])
        if recommendations:
            print("\nРекомендации:")
            for rec in recommendations:
                print(f"  • {rec}")
    else:
        print("Данные о производительности недоступны")
    
    input("\nНажмите Enter для продолжения...")

def show_full_json_report(report: dict):
    """Показывает полный JSON отчет"""
    import json
    
    print("\n📄 ПОЛНЫЙ JSON ОТЧЕТ:")
    print("-" * 40)
    print(json.dumps(report, ensure_ascii=False, indent=2))
    input("\nНажмите Enter для продолжения...")

async def main():
    """Главная функция"""
    
    print_banner()
    
    while True:
        try:
            display_demo_sites()
            choice = get_user_choice()
            
            # Определяем URL для исследования
            if choice == '5':
                url = get_custom_url()
            else:
                sites = get_demo_sites()
                url = sites[choice]['url']
            
            # Получаем глубину исследования
            depth = get_exploration_depth()
            
            # Запускаем исследование
            report = await run_smart_exploration(url, depth)
            
            if report:
                # Показываем детальные результаты
                show_detailed_results_menu(report)
            
            # Спрашиваем, хочет ли пользователь продолжить
            print("\n" + "=" * 50)
            continue_choice = input("Хотите исследовать другой сайт? (y/n): ").strip().lower()
            if continue_choice not in ['y', 'yes', 'д', 'да']:
                break
                
        except KeyboardInterrupt:
            print("\n👋 До свидания!")
            break
        except Exception as e:
            print(f"❌ Произошла ошибка: {e}")
            continue

if __name__ == "__main__":
    asyncio.run(main()) 