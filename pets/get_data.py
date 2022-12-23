import sys
import json
import getopt
import psycopg2

from datetime import datetime as dt


"""
Код подразумевает что в БД не много записей
"""

#Делаем коннект
CONN_POSTGRES = psycopg2.connect(
    database="pet_db",
    user="pet_user",
    password="pet_pass",
    host="postgres",
    port=5432,
)


def err():
    """Вызывается в случае не верных входящих параметров"""
    print(
        """\nДоступны только 3 команды:\n
        python3 get_data.py has-photos: true\n
        python3 get_data.py has-photos: false\n
        python3 get_data.py\n
        Регистр любой, пробелы важны\n"""
    )
    sys.exit(2)


def get_out_json(arg: str, data: list) -> json:
    """Делаем json из данных с БД"""
    final_data = {"pets": list()}
    if arg == "with_photo": # С фото
        for obj in data:
            if isinstance(obj[5][0], str):
                objects = {
                    "id": obj[0],
                    "name": obj[1],
                    "age": obj[2],
                    "type": obj[3],
                    "photos": obj[5],
                    "created_at": obj[4].strftime("%Y-%m-%dT%H:%M:%S"),
                }
                final_data["pets"].append(objects)
    elif arg == "without_photo": # Без фото
        for obj in data:
            if not isinstance(obj[5][0], str):
                objects = {
                    "id": obj[0],
                    "name": obj[1],
                    "age": obj[2],
                    "type": obj[3],
                    "photos": [],
                    "created_at": obj[4].strftime("%Y-%m-%dT%H:%M:%S"),
                }
                final_data["pets"].append(objects)
    else: # если нет ключей то вообще все записи
        for obj in data:
            if not isinstance(obj[5][0], str):
                photo = []
            else:
                photo = obj[5][0]
            objects = {
                "id": obj[0],
                "name": obj[1],
                "age": obj[2],
                "type": obj[3],
                "photos": photo,
                "created_at": obj[4].strftime("%Y-%m-%dT%H:%M:%S"),
            }
            final_data["pets"].append(objects)
    return json.dumps(final_data, indent=4, ensure_ascii=False)


def get_key_args() -> str:
    """Смотрим какие ключи выбрал юзер"""
    try:
        _, args = getopt.getopt(sys.argv[1:], "photo")
        if args:
            arg_1 = args[0].lower()
            arg_2 = args[1].lower()
            if arg_1 != "has-photos:":
                err()
            if arg_2 == "true":
                return "with_photo"
            elif arg_2 == "false":
                return "without_photo"
            else:
                err()
        return "all_data"
    except getopt.GetoptError as e:
        print(f"Ошибка: {e}")
        err()
    except IndexError:
        err()


def get_data_db() -> list:
    """Берем данные из БД"""
    try:
        with CONN_POSTGRES:
            with CONN_POSTGRES.cursor() as cur:
                cur.execute(
                    """
                    SELECT ap.id, ap.name, ap.age, ap.type, ap.created_at, array_agg(api_photos.url)
                    FROM api_pets ap
                    LEFT OUTER JOIN api_photos ON api_photos.pet_id_id = ap.id
                    GROUP BY ap.id
                    """
                )
                data_pet = list(cur)
                return data_pet
    except:
        print("Ошибка чтения из PostgreSQL")


def main() -> json:
    arg = get_key_args()
    data_pet = get_data_db()
    return get_out_json(arg, data_pet)


if __name__ == "__main__":
    print(main())
