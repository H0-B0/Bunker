import apsw
from crypto_db import get_or_create_key

# Путь к твоей базе (там, где лежит база в проекте или в BunkerGame_Data)
DB_PATH = "base3_2.db"

key = get_or_create_key()
conn = apsw.Connection(DB_PATH)
conn.pragma("rekey", key)
conn.close()
print(f"База {DB_PATH} зашифрована ключом из game.key")