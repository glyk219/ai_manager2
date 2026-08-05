from ai_client import ask_ai
from prompts import SYSTEM_PROMPT
from memory import add_message, build_prompt, load_history

print("AI Business Manager")
print("Введите 'выход' для завершения.\n")

load_history()

while True:
    user = input("Клиент: ")

    if user.lower() == "выход":
        break

    add_message("Клиент", user)

    prompt = build_prompt(SYSTEM_PROMPT)

    answer = ask_ai(prompt)

    add_message("Менеджер", answer)

    print("\nМенеджер:\n")
    print(answer)