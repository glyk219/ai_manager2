# Версия 1.1 - добавлена система памяти AI менеджера
import json
import os

HISTORY_FILE = "history.json"

conversation = []


def load_history():
    global conversation

    if os.path.exists(HISTORY_FILE):
        with open(HISTORY_FILE, "r", encoding="utf-8") as file:
            conversation = json.load(file)
    else:
        conversation = []


def save_history():
    with open(HISTORY_FILE, "w", encoding="utf-8") as file:
        json.dump(conversation, file, ensure_ascii=False, indent=4)


def add_message(role: str, text: str):
    conversation.append({
        "role": role,
        "text": text
    })

    save_history()


def build_prompt(system_prompt: str) -> str:
    prompt = system_prompt + "\n\n"

    for message in conversation:
        prompt += f"{message['role']}: {message['text']}\n"

    prompt += "Менеджер:"

    return prompt