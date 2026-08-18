import requests


URL = "http://localhost:11434/api/generate"

MODEL = "qwen2.5:1.5b"


def ask_ai(prompt: str) -> str:

    print("\nОтправляем запрос в Ollama...")

    try:

        response = requests.post(
            URL,
            json={
                "model": MODEL,
                "prompt": prompt,
                "stream": False,
                "options": {
                    "num_predict": 100
                }
            },
            timeout=120
        )

    except requests.exceptions.ConnectionError:

        return (
            "Ошибка: Ollama не запущена. "
            "Запустите Ollama и попробуйте снова."
        )

    except requests.exceptions.Timeout:

        return (
            "Ошибка: Ollama слишком долго "
            "не отвечает."
        )

    print(
        "HTTP статус:",
        response.status_code
    )

    if response.status_code != 200:

        return (
            f"Ошибка Ollama: "
            f"HTTP {response.status_code}"
        )

    try:

        result = response.json()

    except ValueError:

        return "Ошибка: Ollama вернула неправильный JSON."

    if "response" not in result:

        print("Ответ Ollama:")

        print(result)

        return "Ошибка: в ответе Ollama нет поля response."

    return result["response"].strip()