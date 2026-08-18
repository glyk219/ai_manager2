from ai_client import ask_ai
from prompts import SYSTEM_PROMPT

from memory import (
    set_client,
    add_message,
    build_prompt,
    load_history
)

from database import (
    init_db,
    add_client,
    get_all_clients,
    get_client,
    search_clients,
    update_client,
    delete_client,
    load_messages,
    get_client_stats,
    add_order,
    get_order,
    get_client_orders,
    update_order,
    delete_order,
    get_order_details
)
# ============================================================
# ИНИЦИАЛИЗАЦИЯ
# ============================================================

init_db()


# ============================================================
# ВСПОМОГАТЕЛЬНЫЕ ФУНКЦИИ
# ============================================================

def pause():
    input("\nНажмите Enter...")


def print_client(client):

    print("\n========================================")
    print("             КАРТОЧКА КЛИЕНТА")
    print("========================================")

    print(f"ID:       {client[0]}")
    print(f"Имя:      {client[1]}")
    print(f"Телефон:  {client[2] or '-'}")
    print(f"Email:    {client[3] or '-'}")
    print(f"Статус:   {client[4] or '-'}")
    print(f"Заметка:  {client[5] or '-'}")
    print(f"Создан:   {client[6]}")

    print("========================================")


# ============================================================
# ДОБАВЛЕНИЕ КЛИЕНТА
# ============================================================

def add_new_client():

    print("\n========================================")
    print("             НОВЫЙ КЛИЕНТ")
    print("========================================")

    name = input("Имя: ").strip()

    if not name:
        print("\nИмя не может быть пустым.")
        pause()
        return

    phone = input("Телефон: ").strip()
    email = input("Email: ").strip()

    client_id = add_client(
        name,
        phone if phone else None,
        email if email else None
    )

    if client_id is None:

        print("\nТакой клиент уже существует.")

    else:

        print("\nКлиент добавлен.")
        print(f"ID клиента: {client_id}")

    pause()


# ============================================================
# СПИСОК КЛИЕНТОВ
# ============================================================

def show_all_clients():

    print("\n========================================")
    print("             СПИСОК КЛИЕНТОВ")
    print("========================================")

    clients = get_all_clients()

    print(f"\nНайдено клиентов: {len(clients)}")

    if len(clients) == 0:

        print("\nКлиентов пока нет.")
        pause()
        return

    print()

    for client in clients:

        print(
            f"ID: {client[0]} | "
            f"{client[1]} | "
            f"Телефон: {client[2] or '-'} | "
            f"Статус: {client[4] or '-'}"
        )

    pause()


# ============================================================
# ПОИСК
# ============================================================

def search_client():

    print("\n========================================")
    print("              ПОИСК КЛИЕНТА")
    print("========================================")

    text = input(
        "Имя, телефон или Email: "
    ).strip()

    if not text:

        print("\nПоиск отменён.")
        pause()
        return

    clients = search_clients(text)

    if not clients:

        print("\nКлиенты не найдены.")
        pause()
        return

    print(
        f"\nНайдено клиентов: {len(clients)}"
    )

    for client in clients:

        print(
            f"\nID: {client[0]}"
            f"\nИмя: {client[1]}"
            f"\nТелефон: {client[2] or '-'}"
            f"\nEmail: {client[3] or '-'}"
            f"\nСтатус: {client[4] or '-'}"
        )

    print()

    value = input(
        "Введите ID клиента "
        "(Enter — назад): "
    ).strip()

    if not value:
        return

    try:

        client_id = int(value)

    except ValueError:

        print("\nID должен быть числом.")
        pause()
        return

    client = get_client(client_id)

    if client is None:

        print("\nКлиент не найден.")
        pause()
        return

    client_menu(client)


# ============================================================
# ИСТОРИЯ
# ============================================================

def show_history(client):

    print("\n========================================")
    print("             ИСТОРИЯ ЧАТА")
    print("========================================")

    print(f"\nКлиент: {client[1]}")

    messages = load_messages(
        client[0],
        100
    )

    if not messages:

        print("\nИстория пустая.")
        pause()
        return

    for role, text, created_at in messages:

        print("\n----------------------------------------")
        print(f"{created_at}")
        print(f"{role}:")
        print(text)

    print("----------------------------------------")

    pause()

# ============================================================
# ЗАКАЗЫ КЛИЕНТА
# ============================================================

# ============================================================
# ДОБАВЛЕНИЕ ЗАКАЗА
# ============================================================

def add_new_order(client):

    print("\n========================================")
    print("             НОВЫЙ ЗАКАЗ")
    print("========================================")

    print(f"\nКлиент: {client[1]}")

    title = input(
        "\nНазвание заказа: "
    ).strip()

    if not title:

        print("\nНазвание заказа не может быть пустым.")
        pause()
        return

    description = input(
        "Описание заказа: "
    ).strip()

    price_text = input(
        "Стоимость заказа: "
    ).strip()

    try:

        price = float(
            price_text.replace(",", ".")
        )

    except ValueError:

        print("\nОшибка: стоимость должна быть числом.")
        pause()
        return

    if price < 0:

        print("\nСтоимость не может быть отрицательной.")
        pause()
        return

    print("\nСтатус заказа:")

    print("1. Новый")
    print("2. В работе")
    print("3. Готов")
    print("4. Завершён")

    status_choice = input(
        "\nВыберите статус: "
    ).strip()

    statuses = {
        "1": "Новый",
        "2": "В работе",
        "3": "Готов",
        "4": "Завершён"
    }

    status = statuses.get(
        status_choice
    )

    if status is None:

        print("\nНеверный статус.")
        pause()
        return

    order_id = add_order(
        client[0],
        title,
        description if description else None,
        price,
        status
    )

    print("\n========================================")
    print("             ЗАКАЗ СОЗДАН")
    print("========================================")

    print(f"\nНомер заказа: {order_id}")
    print(f"Клиент: {client[1]}")
    print(f"Название: {title}")
    print(f"Стоимость: {price:.2f} ₽")
    print(f"Статус: {status}")

    pause()

# ============================================================
# РЕДАКТИРОВАНИЕ ЗАКАЗА
# ============================================================

# ============================================================
# РЕДАКТИРОВАНИЕ ЗАКАЗА
# ============================================================

def edit_order():

    print("\n========================================")
    print("          РЕДАКТИРОВАНИЕ ЗАКАЗА")
    print("========================================")

    order_id_text = input(
        "\nВведите ID заказа: "
    ).strip()

    try:

        order_id = int(order_id_text)

    except ValueError:

        print("\nОшибка: ID должен быть числом.")
        pause()
        return

    order = get_order(order_id)

    if order is None:

        print("\nЗаказ не найден.")
        pause()
        return

    print("\n----------------------------------------")

    print(f"ID: {order[0]}")
    print(f"Название: {order[2]}")
    print(f"Описание: {order[3] or '-'}")
    print(f"Цена: {order[4]:.2f} ₽")
    print(f"Статус: {order[5]}")

    print("----------------------------------------")

    # --------------------------------------------------------
    # НОВОЕ НАЗВАНИЕ
    # --------------------------------------------------------

    new_title = input(
        f"\nНовое название [{order[2]}]: "
    ).strip()

    if not new_title:

        new_title = order[2]

    # --------------------------------------------------------
    # НОВОЕ ОПИСАНИЕ
    # --------------------------------------------------------

    current_description = order[3] or ""

    new_description = input(
        f"Новое описание [{current_description}]: "
    ).strip()

    if not new_description:

        new_description = current_description

    # --------------------------------------------------------
    # НОВАЯ ЦЕНА
    # --------------------------------------------------------

    while True:

        new_price_text = input(
            f"Новая цена [{order[4]}]: "
        ).strip()

        if not new_price_text:

            new_price = order[4]
            break

        try:

            new_price = float(
                new_price_text.replace(",", ".")
            )

            if new_price < 0:

                print(
                    "\nЦена не может быть отрицательной."
                )

                continue

            break

        except ValueError:

            print(
                "\nВведите число. Например: 7500"
            )

    # --------------------------------------------------------
    # НОВЫЙ СТАТУС
    # --------------------------------------------------------

    print("\nНовый статус:")

    print("1. Новый")
    print("2. В работе")
    print("3. Готов")
    print("4. Завершён")

    status_choice = input(
        f"\nВыберите статус [{order[5]}]: "
    ).strip()

    statuses = {
        "1": "Новый",
        "2": "В работе",
        "3": "Готов",
        "4": "Завершён"
    }

    if not status_choice:

        new_status = order[5]

    else:

        new_status = statuses.get(
            status_choice
        )

        if new_status is None:

            print("\nНеверный статус.")
            pause()
            return

    # --------------------------------------------------------
    # СОХРАНЕНИЕ
    # --------------------------------------------------------

    updated = update_order(
        order_id,
        new_title,
        new_description,
        new_price,
        new_status
    )

    if updated:

        print("\n========================================")
        print("         ЗАКАЗ УСПЕШНО ОБНОВЛЁН")
        print("========================================")

        print(f"\nID заказа: {order_id}")
        print(f"Название: {new_title}")
        print(f"Описание: {new_description or '-'}")
        print(f"Цена: {new_price:.2f} ₽")
        print(f"Статус: {new_status}")

    else:

        print("\nЗаказ не был изменён.")

    pause()

# ============================================================
# УДАЛЕНИЕ ЗАКАЗА
# ============================================================

def remove_order():

    print("\n========================================")
    print("             УДАЛЕНИЕ ЗАКАЗА")
    print("========================================")

    order_id_text = input(
        "\nВведите ID заказа: "
    ).strip()

    try:

        order_id = int(order_id_text)

    except ValueError:

        print("\nОшибка: ID должен быть числом.")
        pause()
        return

    order = get_order(order_id)

    if order is None:

        print("\nЗаказ не найден.")
        pause()
        return

    print("\n----------------------------------------")

    print(f"ID: {order[0]}")
    print(f"Название: {order[2]}")
    print(f"Описание: {order[3] or '-'}")
    print(f"Цена: {order[4]:.2f} ₽")
    print(f"Статус: {order[5]}")

    print("----------------------------------------")

    confirm = input(
        "\nУдалить этот заказ? (да/нет): "
    ).strip().lower()

    if confirm not in ("да", "д", "yes", "y"):

        print("\nУдаление отменено.")
        pause()
        return

    deleted = delete_order(
        order_id
    )

    if deleted:

        print("\nЗаказ успешно удалён.")

    else:

        print("\nЗаказ не был удалён.")

    pause()

# ============================================================
# КАРТОЧКА ЗАКАЗА
# ============================================================

def show_order_card():

    print("\n========================================")
    print("            КАРТОЧКА ЗАКАЗА")
    print("========================================")

    order_id_text = input(
        "\nВведите ID заказа: "
    ).strip()

    try:

        order_id = int(order_id_text)

    except ValueError:

        print("\nОшибка: ID должен быть числом.")
        pause()
        return

    # Получаем заказ
    order = get_order(order_id)

    if order is None:

        print("\nЗаказ не найден.")
        pause()
        return

    # Получаем клиента
    client = get_client(order[1])

    # Получаем параметры 3D-модели
    order_details = get_order_details(order_id)

    print("\n========================================")
    print("              ЗАКАЗ")
    print("========================================")

    print(f"\nID заказа:       {order[0]}")

    if client:

        print(f"ID клиента:      {client[0]}")
        print(f"Клиент:          {client[1]}")
        print(f"Телефон:         {client[2] or '-'}")
        print(f"Email:           {client[3] or '-'}")

    else:

        print("Клиент:          не найден")

    print("----------------------------------------")

    print(f"Название:        {order[2]}")
    print(f"Описание:        {order[3] or '-'}")
    print(f"Стоимость:       {order[4]:.2f} ₽")
    print(f"Статус:          {order[5]}")
    print(f"Создан:          {order[6]}")

    print("----------------------------------------")
    print("        ПАРАМЕТРЫ 3D-МОДЕЛИ")
    print("----------------------------------------")

    if order_details:

        print(
            f"Тип модели:      "
            f"{order_details[2] or '-'}"
        )

        if order_details[3] is not None:

            print(
                f"Размер:          "
                f"{order_details[3]:.1f} см"
            )

        else:

            print("Размер:          -")

        print(
            f"Материал:        "
            f"{order_details[4] or '-'}"
        )

        print(
            f"Цвет:            "
            f"{order_details[5] or '-'}"
        )

        print(
            f"Этап производства: "
            f"{order_details[6] or '-'}"
        )

    else:

        print("3D-параметры ещё не заполнены.")

    print("----------------------------------------")

    pause()

# ============================================================
# РЕДАКТИРОВАНИЕ ПАРАМЕТРОВ 3D-МОДЕЛИ
# ============================================================

def edit_3d_details():

    print("\n========================================")
    print("       ПАРАМЕТРЫ 3D-МОДЕЛИ")
    print("========================================")

    order_id_text = input(
        "\nВведите ID заказа: "
    ).strip()

    try:

        order_id = int(order_id_text)

    except ValueError:

        print("\nОшибка: ID заказа должен быть числом.")
        pause()
        return

    # Проверяем существование заказа
    order = get_order(order_id)

    if order is None:

        print("\nЗаказ не найден.")
        pause()
        return

    # Получаем существующие параметры
    details = get_order_details(order_id)

    if details:

        current_model = details[2] or ""
        current_size = details[3]
        current_material = details[4] or ""
        current_color = details[5] or ""
        current_stage = details[6] or ""

    else:

        current_model = ""
        current_size = None
        current_material = ""
        current_color = ""
        current_stage = ""

    # --------------------------------------------------------
    # ТИП МОДЕЛИ
    # --------------------------------------------------------

    print("\nТип модели:")
    print("1. Фигурка человека")
    print("2. Бюст")
    print("3. Статуэтка")
    print("4. Другое")

    model_choice = input(
        "\nВыберите тип модели: "
    ).strip()

    model_types = {
        "1": "Фигурка человека",
        "2": "Бюст",
        "3": "Статуэтка",
        "4": "Другое"
    }

    if model_choice in model_types:

        model_type = model_types[model_choice]

    elif model_choice == "":

        model_type = current_model

    else:

        print("\nНеверный вариант.")
        pause()
        return

    # --------------------------------------------------------
    # РАЗМЕР
    # --------------------------------------------------------

    while True:

        size_text = input(
            f"\nРазмер в сантиметрах [{current_size or '-'}]: "
        ).strip()

        if not size_text:

            size_cm = current_size
            break

        try:

            size_cm = float(
                size_text.replace(",", ".")
            )

            if size_cm <= 0:

                print("\nРазмер должен быть больше нуля.")
                continue

            break

        except ValueError:

            print(
                "\nВведите число. Например: 15"
            )

    # --------------------------------------------------------
    # МАТЕРИАЛ
    # --------------------------------------------------------

    print("\nМатериал:")
    print("1. Фотополимер")
    print("2. PLA")
    print("3. ABS")
    print("4. Другое")

    material_choice = input(
        "\nВыберите материал: "
    ).strip()

    materials = {
        "1": "Фотополимер",
        "2": "PLA",
        "3": "ABS",
        "4": "Другое"
    }

    if material_choice in materials:

        material = materials[material_choice]

    elif material_choice == "":

        material = current_material

    else:

        print("\nНеверный вариант.")
        pause()
        return

    # --------------------------------------------------------
    # ЦВЕТ
    # --------------------------------------------------------

    color = input(
        f"\nЦвет [{current_color or '-'}]: "
    ).strip()

    if not color:

        color = current_color

    # --------------------------------------------------------
    # ЭТАП ПРОИЗВОДСТВА
    # --------------------------------------------------------

    print("\nЭтап производства:")
    print("1. Получена фотография")
    print("2. Подготовка модели")
    print("3. Проверка модели")
    print("4. Печать")
    print("5. Постобработка")
    print("6. Готово")

    stage_choice = input(
        "\nВыберите этап: "
    ).strip()

    stages = {
        "1": "Получена фотография",
        "2": "Подготовка модели",
        "3": "Проверка модели",
        "4": "Печать",
        "5": "Постобработка",
        "6": "Готово"
    }

    if stage_choice in stages:

        production_stage = stages[stage_choice]

    elif stage_choice == "":

        production_stage = current_stage

    else:

        print("\nНеверный вариант.")
        pause()
        return

    # --------------------------------------------------------
    # СОХРАНЕНИЕ
    # --------------------------------------------------------

    save_order_details(
        order_id,
        model_type,
        size_cm,
        material,
        color,
        production_stage
    )

    print("\n========================================")
    print("     3D-ПАРАМЕТРЫ СОХРАНЕНЫ")
    print("========================================")

    print(f"\nТип модели: {model_type or '-'}")
    print(f"Размер: {size_cm or '-'} см")
    print(f"Материал: {material or '-'}")
    print(f"Цвет: {color or '-'}")
    print(f"Этап: {production_stage or '-'}")

    pause()

# ============================================================
# ЗАКАЗЫ КЛИЕНТА
# ============================================================

def show_orders(client):

    while True:

        print("\n========================================")
        print("              ЗАКАЗЫ КЛИЕНТА")
        print("========================================")

        print(f"\nКлиент: {client[1]}")

        print("\n1. Список заказов")
        print("2. Добавить заказ")
        print("3. Изменить заказ")
        print("4. Удалить заказ")
        print("5. Карточка заказа")
        print("6. Параметры 3D-модели")
        print("7. Назад")

        choice = input(
            "\nВыберите: "
        ).strip()

        if choice == "1":

            orders = get_client_orders(
                client[0]
            )

            print("\n========================================")
            print("             СПИСОК ЗАКАЗОВ")
            print("========================================")

            if not orders:

                print("\nУ клиента пока нет заказов.")

                pause()
                continue

            print(
                f"\nКоличество заказов: {len(orders)}"
            )

            for order in orders:

                print("\n----------------------------------------")

                print(f"ID заказа: {order[0]}")
                print(f"Название: {order[2]}")
                print(f"Описание: {order[3] or '-'}")
                print(f"Цена: {order[4]:.2f} ₽")
                print(f"Статус: {order[5]}")
                print(f"Дата создания: {order[6]}")

            print("----------------------------------------")

            pause()

        elif choice == "2":

            add_new_order(client)

        elif choice == "3":

            edit_order()

        elif choice == "4":

            remove_order()

        elif choice == "5":

            show_order_card()

        elif choice == "6":

            edit_3d_details()

        elif choice == "7":

            return

        else:

            print("\nНеверный пункт.")

# ============================================================
# AI ЧАТ
# ============================================================

def ai_chat(client):

    print("\n========================================")
    print("                AI ЧАТ")
    print("========================================")

    print(f"\nКлиент: {client[1]}")

    print(
        "\nВведите 'выход' для завершения."
    )

    # Очень важно:
    # передаём ID клиента
    set_client(client[0])

    # Загружаем историю
    load_history()

    while True:

        user = input("\nКлиент: ").strip()

        if user.lower() == "выход":

            print("\nДиалог завершён.")

            return

        if not user:

            continue

        # Сохраняем сообщение клиента
        add_message(
            "Клиент",
            user
        )

        # Создаём prompt
        prompt = build_prompt(
            SYSTEM_PROMPT
        )

        # Запрашиваем Ollama
        answer = ask_ai(
            prompt
        )

        # Сохраняем ответ
        add_message(
            "Менеджер",
            answer
        )

        print("\nМенеджер:")
        print(answer)


# ============================================================
# РЕДАКТИРОВАНИЕ
# ============================================================

def edit_client(client):

    while True:

        print("\n========================================")
        print("          РЕДАКТИРОВАНИЕ")
        print("========================================")

        print(f"\nКлиент: {client[1]}")

        print("\n1. Телефон")
        print("2. Email")
        print("3. Статус")
        print("4. Заметка")
        print("5. Назад")

        choice = input(
            "\nВыберите: "
        ).strip()

        if choice == "1":

            phone = input(
                "Новый телефон: "
            ).strip()

            update_client(
                client[0],
                phone,
                client[3],
                client[4],
                client[5]
            )

            client = get_client(
                client[0]
            )

            print("\nТелефон изменён.")

        elif choice == "2":

            email = input(
                "Новый Email: "
            ).strip()

            update_client(
                client[0],
                client[2],
                email,
                client[4],
                client[5]
            )

            client = get_client(
                client[0]
            )

            print("\nEmail изменён.")

        elif choice == "3":

            status = input(
                "Новый статус: "
            ).strip()

            update_client(
                client[0],
                client[2],
                client[3],
                status,
                client[5]
            )

            client = get_client(
                client[0]
            )

            print("\nСтатус изменён.")

        elif choice == "4":

            notes = input(
                "Новая заметка: "
            ).strip()

            update_client(
                client[0],
                client[2],
                client[3],
                client[4],
                notes
            )

            client = get_client(
                client[0]
            )

            print("\nЗаметка изменена.")

        elif choice == "5":

            return client

        else:

            print("\nНеверный пункт.")


# ============================================================
# СТАТИСТИКА
# ============================================================

def show_stats(client):

    print("\n========================================")
    print("              СТАТИСТИКА")
    print("========================================")

    stats = get_client_stats(
        client[0]
    )

    total = stats[0] or 0
    client_messages = stats[1] or 0
    manager_messages = stats[2] or 0
    last_message = stats[3] or "-"

    print(f"\nКлиент: {client[1]}")
    print(f"Всего сообщений: {total}")
    print(f"Сообщений клиента: {client_messages}")
    print(f"Ответов менеджера: {manager_messages}")
    print(f"Последнее сообщение: {last_message}")

    pause()


# ============================================================
# УДАЛЕНИЕ
# ============================================================

def remove_client(client):

    print("\n========================================")
    print("            УДАЛЕНИЕ КЛИЕНТА")
    print("========================================")

    print(
        f"\nВы хотите удалить: {client[1]}"
    )

    print(
        "\nВНИМАНИЕ!"
        "\nИстория сообщений этого клиента "
        "также будет удалена."
    )

    answer = input(
        "\nВведите ДА для удаления: "
    ).strip().lower()

    if answer != "да":

        print("\nУдаление отменено.")
        pause()

        return False

    result = delete_client(
        client[0]
    )

    if result:

        print("\nКлиент удалён.")
        pause()

        return True

    print("\nКлиент не найден.")
    pause()

    return False


# ============================================================
# МЕНЮ КЛИЕНТА
# ============================================================

def client_menu(client):

    while True:

        if client is None:

            print("\nОшибка: клиент не найден.")
            pause()
            return

        print("\n========================================")
        print("             МЕНЮ КЛИЕНТА")
        print("========================================")

        print(f"\nКлиент: {client[1]}")

        print("\n1. AI-диалог")
        print("2. История сообщений")
        print("3. Заказы")
        print("4. Редактировать")
        print("5. Статистика")
        print("6. Удалить клиента")
        print("7. Назад")

        choice = input(
            "\nВыберите: "
        ).strip()

        if choice == "1":

            ai_chat(client)

        elif choice == "2":

            show_history(client)

        elif choice == "3":

            show_orders(client)

        elif choice == "4":

            client = edit_client(
                client
            )
            
        elif choice == "5":

            show_stats(client)

        elif choice == "6":

            deleted = remove_client(client)

            if deleted:
                return

        elif choice == "7":

            return

        else:

            print("\nНеверный пункт.")


# ============================================================
# ОТКРЫТЬ КЛИЕНТА ПО ID
# ============================================================

def open_client_by_id():

    value = input(
        "\nВведите ID клиента: "
    ).strip()

    if not value:

        return

    try:

        client_id = int(value)

    except ValueError:

        print("\nID должен быть числом.")
        pause()
        return

    client = get_client(
        client_id
    )

    if client is None:

        print("\nКлиент не найден.")
        pause()
        return

    client_menu(client)


# ============================================================
# ГЛАВНОЕ МЕНЮ
# ============================================================

def main_menu():

    while True:

        print("\n========================================")
        print("          AI BUSINESS MANAGER")
        print("========================================")

        print("\n1. Добавить клиента")
        print("2. Найти клиента")
        print("3. Список клиентов")
        print("4. Открыть клиента по ID")
        print("5. Выход")

        choice = input(
            "\nВыберите пункт: "
        ).strip()

        if choice == "1":

            add_new_client()

        elif choice == "2":

            search_client()

        elif choice == "3":

            show_all_clients()

        elif choice == "4":

            open_client_by_id()

        elif choice == "5":

            print("\nПрограмма завершена.")

            break

        else:

            print("\nНеверный пункт.")


# ============================================================
# ЗАПУСК
# ============================================================

if __name__ == "__main__":

    main_menu()