import requests

URL = "http://localhost:11434/api/generate"

def ask_ai(prompt: str) -> str:
    print("Отправляем запрос в Ollama...")

    response = requests.post(
        URL,
        json={
            "model": "qwen2.5:1.5b",
            "prompt": prompt,
            "stream": False,
            "options": {
                "num_predict": 100
            }
        },
        timeout=120
    )

    print("HTTP статус:", response.status_code)

    result = response.json()

    print("Ответ JSON:")
    print(result)

    return result["response"]