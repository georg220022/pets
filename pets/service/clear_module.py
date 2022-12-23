import os

from rest_framework import status
from rest_framework.response import Response

from django.db import IntegrityError, transaction
from pets.settings import MEDIA_ROOT
from api.models import Pets, Photos
from typing import Union


def delete_file(list_name_file: list) -> None:
    # Удаление наверное на сигналах лучше было бы
    # Но я и так тестовое затянул, так что вот:
    for obj in list_name_file:
        path = str(MEDIA_ROOT) + "/" + obj
        if os.path.isfile(path):
            os.remove(path)
        else:
            # Представим что тут логгирование
            # или записываем файлы которые не удалось
            # найти и удалить
            print("Не удалось найти файл")
            pass


def deleter(white_list: list) -> Union[int, list] | str:
    query_pet = Pets.objects.filter(id__in=white_list)
    list_id_pet = [str(obj.id) for obj in query_pet]
    query_photo = Photos.objects.filter(pet_id__in=list_id_pet)
    list_name_file = [obj.image.name for obj in query_photo]
    print(list_name_file)
    with transaction.atomic():
        query_photo.delete()
        query_pet.delete()
    count_deleted_pet = len(list_id_pet)
    white_lists = [str(obj) for obj in white_list]
    not_found_pet_id = list(set(white_lists) - set(list_id_pet))
    err_list = [dict(id=obj, error="Нет записи") for obj in not_found_pet_id]
    delete_file(list_name_file)
    return count_deleted_pet, err_list
