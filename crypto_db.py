import os
import sys
import secrets
import apsw

def get_app_data_path():
    """Возвращает путь к папке с данными приложения."""
    if hasattr(sys, '_MEIPASS'):
        if sys.platform.startswith('win'):
            app_data_path = os.path.join(os.environ['LOCALAPPDATA'], 'BunkerGame')
        else:
            home = os.path.expanduser("~")
            app_data_path = os.path.join(home, '.local', 'share', 'BunkerGame')
    else:
        app_data_path = os.path.join(os.path.abspath("."), 'BunkerGame_Data')
    os.makedirs(app_data_path, exist_ok=True)
    return app_data_path


def get_or_create_key():
    """Генерирует ключ шифрования при первом запуске или читает существующий."""
    app_data_path = get_app_data_path()
    key_path = os.path.join(app_data_path, 'game.key')

    if not os.path.exists(key_path):
        new_key = secrets.token_hex(32)
        with open(key_path, 'w') as f:
            f.write(new_key)
        # На Linux сразу закрываем файл от посторонних
        if not sys.platform.startswith('win'):
            os.chmod(key_path, 0o600)
        print(f"Создан новый ключ: {key_path}")
        return new_key
    else:
        with open(key_path, 'r') as f:
            return f.read().strip()

def init_database(db_path):
    """
    Инициализирует базу данных:
    - Если ключа нет — создаёт его и шифрует базу.
    - Если ключ есть — ничего не делает (база уже зашифрована).
    """
    app_data_path = get_app_data_path()
    key_path = os.path.join(app_data_path, 'game.key')

    if os.path.exists(key_path):
        # Ключ есть — значит, база уже зашифрована
        print("Ключ найден, база уже зашифрована.")
        return

    # Ключа нет — это первый запуск
    print("Первый запуск: создаём ключ и шифруем базу...")
    new_key = secrets.token_hex(32)
    with open(key_path, 'w') as f:
        f.write(new_key)
    if not sys.platform.startswith('win'):
        os.chmod(key_path, 0o600)

    # Шифруем базу
    conn = apsw.Connection(db_path)
    conn.pragma("rekey", new_key)
    conn.close()
    print(f"База {db_path} зашифрована. Ключ сохранён в {key_path}")