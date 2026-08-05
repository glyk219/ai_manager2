import requests

SYSTEM_PROMPT = """
Ты профессиональный менеджер компании AI Business.

Твоя задача — помочь клиенту подобрать решение по автоматизации бизнеса.

Правила:

1. Всегда здоровайся.
2. Будь вежливым.
3. Отвечай простым понятным языком.
4. Задавай не больше двух уточняющих вопросов за один ответ.
5. Не придумывай стоимость услуг.
6. Если информации недостаточно — сначала уточни детали.
7. Предлагай решения только после того, как поймешь задачу клиента.
"""

while True:
    user = input("Клиент: ")
    
    if user.lower() == "выход":
        break
    prompt = f"""
    {SYSTEM_PROMPT}
    Клиент написал:
    {user}
    Ответ клиенту:
    """
    try:
        response = requests.post(
            "http://localhost:11434/api/generate",
            json={
                "model": "qwen2.5:1.5b",
                "prompt": prompt,
                "stream": False
            },
            timeout=60
        )

        response.raise_for_status()

        result = response.json()

        print("\nМенеджер:\n")
        print(response.json()["response"])
    
    except Exception as e:
        print("Ошибка:", e)