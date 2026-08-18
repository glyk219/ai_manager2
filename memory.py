from database import save_message, load_messages


current_client = None


def set_client(client_id):

    global current_client

    current_client = client_id


def load_history():

    if current_client is None:
        raise ValueError("Клиент не выбран")

    return load_messages(current_client)


def add_message(role, text):

    if current_client is None:
        raise ValueError("Клиент не выбран")

    save_message(
        current_client,
        role,
        text
    )


def build_prompt(system_prompt):

    if current_client is None:
        raise ValueError("Клиент не выбран")

    prompt = system_prompt.strip()

    prompt += "\n\nИстория общения:\n"

    history = load_messages(
        current_client,
        limit=20
    )

    for role, text, created_at in history:

        prompt += f"{role}: {text}\n"

    return prompt