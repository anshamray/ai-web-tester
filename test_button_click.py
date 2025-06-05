#!/usr/bin/env python3
"""
Тестовый скрипт для проверки улучшенной логики клика по кнопкам
"""

import asyncio
from smart_exploration_agent import SmartExplorationAgent

async def test_button_clicking():
    """Тестирует улучшенную логику клика по кнопкам"""
    
    agent = SmartExplorationAgent()
    
    # Тестируем на imgur.com
    test_url = "https://imgur.com"
    
    print(f"🧪 Тестируем улучшенную логику клика на {test_url}")
    print("=" * 60)
    
    try:
        # Инициализируем браузер
        await agent.browser_tool.start()
        
        # Переходим на страницу
        page_info = await agent.browser_tool.navigate_to_page(test_url)
        print(f"✅ Страница загружена: {page_info.title}")
        
        # Ищем формы аутентификации
        print("\n🔍 Поиск форм аутентификации...")
        auth_forms = await agent._search_for_auth_links()
        
        print(f"\n📊 Результаты:")
        print(f"   Найдено форм аутентификации: {len(auth_forms)}")
        
        for i, form in enumerate(auth_forms):
            print(f"   Форма {i+1}: {form.get('purpose', 'unknown')} - {form.get('source_url', 'main_page')}")
            if form.get('trigger_button'):
                print(f"     Триггер: {form['trigger_button']}")
        
        # Тестируем регистрацию
        if auth_forms:
            print("\n👤 Тестируем регистрацию...")
            personas = agent._create_user_personas()
            
            for persona in personas[:1]:  # Тестируем только первую персону
                result = await agent._attempt_registration(auth_forms, persona)
                if result:
                    print(f"✅ Регистрация {persona['name']}: успешно")
                    print(f"   Заполнено полей: {len(result['fill_result']['filled_fields'])}")
                    print(f"   Отправка формы: {'✅' if result['submit_result']['success'] else '❌'}")
                else:
                    print(f"❌ Регистрация {persona['name']}: неудачно")
        
    except Exception as e:
        print(f"❌ Ошибка при тестировании: {e}")
        import traceback
        traceback.print_exc()
    
    finally:
        # Закрываем браузер
        await agent.browser_tool.close()

if __name__ == "__main__":
    asyncio.run(test_button_clicking()) 