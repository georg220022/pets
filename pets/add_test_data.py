import sys
import json
import getopt
import psycopg2
from random import randint
import uuid
from datetime import datetime as dt


"""
50 тестовых записей
"""

# Делаем коннект
CONN_POSTGRES = psycopg2.connect(
    database="pet_db",
    user="pet_user",
    password="pet_pass",
    host="postgres",
    port=5432,
)


def main():
    data_pet_list = []
    data_name = ["Вася", "Арчи", "Рекс", "Тишка", "Маша", "Персей"]
    data_age = [3, 5, 8]
    data_type = ["cat", "dog"]
    for _ in range(50):
        data_pet_list.append(
            (
                str(uuid.uuid4()),
                dt.now(),
                data_name[randint(0, 5)],
                data_age[randint(0, 2)],
                data_type[randint(0, 1)],
            )
        )
    try:
        with CONN_POSTGRES:
            with CONN_POSTGRES.cursor() as cur:
                query = "INSERT INTO %s(%s) VALUES(%%s,%%s,%%s,%%s,%%s)" % (
                    "api_pets",
                    "id, created_at, name, age, type",
                )
                print("\nНачинаем заполнение PostgreSQL\n\n")
                cur.executemany(query, data_pet_list)
                CONN_POSTGRES.commit()
    except:
        print("Неполучилось записать данные. Их можно добавить чз постман\n")
    else:
        print("Данные записаны\n")


if __name__ == "__main__":
    main()
