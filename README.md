## Pets app
##### Стек: Python, Django, DRF, Postgres, Nginx, Docker(compose), SQL  
##### Лучше запускать на локальной машине или на пустом облаке, иначе порты или nginx уже настраивать у вас  
#### Если запуск на локальной машине, раздел "Настройка для сервера" - пропустить.  
##### Настройка для сервера:  
для локального запуска пропустить этот раздел  
- открыть pets/pets/.env  
-- Изменить HOST на ip сервера  
-- Если вместо порта используете домен, то заменить PORT на ".ru"  
- открыть pets/nginx.conf  
-- Изменить 3-ю строку порт с 8000 на 80  
-- Изменит 4-ю строку на ip адрес сервера  
  
  
##### Запуск:  
Клонировать репозиторий: ```git clone git@github.com:georg220022/pets.git```  
Перейти в папку с docker-compose, выполнить команду: ```docker-compose up -d```  
Выполнить 3 команды:  
узнать имя контейнера образа pets-web ```docker container ls```  
у меня это pets-web-1  
```
docker exec -it pets-web-1 python3 manage.py makemigrations  
docker exec -it pets-web-1 python3 manage.py migrate  
docker exec -it pets-web-1 python3 add_test_data.py # Будут загруженны тестовые данные (50 шт) БЕЗ фото  
```  
##### Добавить заголовок X-API-KEY  
по умолчанию X-API-KEY = "123456789"  
изменить можно в .env  
  
##### Добавление животного:  
```type может быть "cat" или "dog"```  
POST: http://localhost:8000/pets  
{  
    "name": "Василий",  
    "age": 5,  
    "type": "cat"   
}  
![Иллюстрация к проекту](https://github.com/georg220022/pets/blob/main/img/add_pet.png)    
##### Добавление фото:  
POST: http://localhost:8000/pets/UUID/photo  
В Postman'e: Body -> form-data  
ключ: binary  
значение: прикрепить картинку  
![Иллюстрация к проекту](https://github.com/georg220022/pets/blob/main/img/add_photo.png)   
##### Показать питомцев:  
GET: http://localhost:8000/pets?limit=1&offset=0&has_photos=true  
![Иллюстрация к проекту](https://github.com/georg220022/pets/blob/main/img/get_pets.png)  
##### Удалить питомцев:  
Удаляются все записи и все файлы указанных питомцев:  
DELETE: http://localhost:8000/pets  
![Иллюстрация к проекту](https://github.com/georg220022/pets/blob/main/img/deleted.png)  
#### CLI:  
Все записи: ```docker exec -it pets-web-1 python3 get_data.py```   
С фото: ```docker exec -it pets-web-1 python3 get_data.py has-photos: true```  
Без фото: ```docker exec -it pets-web-1 python3 get_data.py has-photos: false```  
