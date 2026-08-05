import requests
import time

url = "http://localhost:11434/api/generate"

data = {
    "model": "qwen2.5:1.5b",
    "prompt": "Скажи только слово: Привет",
    "stream": False
}

print("Отправляем запрос...")

start = time.time()

response = requests.post(url, json=data, timeout=120)

end = time.time()

print("Статус:", response.status_code)
print(f"Время: {end - start:.2f} сек.")
print(response.json())
