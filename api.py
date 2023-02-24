import requests
import json
from requests_toolbelt.multipart.encoder import MultipartEncoder


class PetFriends:
    def __init__(self):
        self.base_url = 'https://petfriends.skillfactory.ru'

    def get_api_key(self, email: str, password: str) -> json:
        """Метод делает запрос к API сервера и возвращает статус
        и результат в формате JSON с уникальным ключом пользователя,
        найденного по указанным email и password"""

        headers = {
            'email': email,
            'password': password
        }
        res = requests.get(self.base_url + '/api/key', headers=headers)
        status = res.status_code
        result = ''
        try:
            result = res.json()
        except json.decoder.JSONDecodeError:
            result = res.text
        return status, result

    def get_list_of_pets(self, auth_key: json, filter: str) -> json:
        """Метод делает запрос к API сервера и возвращает статус запроса
        и список всех доступных питомцев в формате json"""

        headers = {'auth_key': auth_key['key']}
        filter = {'filter': filter}

        res = requests.get(self.base_url + '/api/pets', headers=headers, params=filter)

        status = res.status_code
        result = ''
        try:
            result = res.json()
        except json.decoder.JSONDecodeError:
            result = res.text
        return status, result

    def add_new_pet_without_photo(self, auth_key: str, name: str, animal_type: str, age: int) -> json:
        """Метод отправляет данные на сервер о добавлении нового питомца без фотографии. Возвращает статус запроса
        на сервер и результат в формате json с данными добавленного питомца."""

        data = {
            'name': name,
            'animal_type': animal_type,
            'age': age
        }
        headers = {'auth_key': auth_key['key']}
        res = requests.post(self.base_url + '/api/create_pet_simple', headers=headers, data=data)
        status = res.status_code
        result = ''
        try:
            result = res.json()
        except json.decoder.JSONDecodeError:
            result = res.text
        return status, result

    def add_photo_of_pet(self, auth_key: json, pet_id: str, pet_photo: str) -> json:
        """Метод отправляет данные на сервер о добавлении фотографии в уже существующие данные питомца.
        Возвращает статус запроса на сервер и результат в формате json с данными."""

        data = MultipartEncoder(
            fields={
                'pet_id': pet_id,
                'pet_photo': (pet_photo, open(pet_photo, 'rb'), 'image/jpeg')
            })
        headers = {'auth_key': auth_key['key'], 'Content-Type': data.content_type}

        res = requests.post(self.base_url + '/api/pets/set_photo/' + pet_id, headers=headers, data=data)

        status = res.status_code
        result = ''
        try:
            result = res.json()
        except json.decoder.JSONDecodeError:
            result = res.text
        return status, result

    def add_new_pet(self, auth_key: json, name: str, animal_type: str, age: int, pet_photo: str) -> json:
        """Метод отправляет данные на сервер о добавлении нового питомца. Возвращает статус запроса
        на сервер и результат в формате json с данными добавленного питомца."""

        data = MultipartEncoder(
            fields={
                'name': name,
                'animal_type': animal_type,
                'age': age,
                'pet_photo': (pet_photo, open(pet_photo, 'rb'), 'image/png')
            })
        headers = {'auth_key': auth_key['key'], 'Content-Type': data.content_type}

        res = requests.post(self.base_url + '/api/pets', headers=headers, data=data)

        status = res.status_code
        result = ''
        try:
            result = res.json()
        except json.decoder.JSONDecodeError:
            result = res.text
        return status, result

    def update_info_pet(self, auth_key: json, pet_id, name: str, animal_type: str, age: int) -> json:
        """Метод отправляет данные на сервер об изменении данных питомца. Возвращает статус запроса
        на сервер и результат в формате json с обновленными данными питомца."""

        data = {
            'name': name,
            'animal_type': animal_type,
            'age': age
        }
        headers = {'auth_key': auth_key['key']}

        res = requests.put(self.base_url + '/api/pets/' + pet_id, headers=headers, data=data)
        status = res.status_code
        result = ''
        try:
            result = res.json()
        except json.decoder.JSONDecodeError:
            result = res.text
        return status, result

    def delete_pet_from_database(self, auth_key: json, pet_id: str) -> json:
        """Метод отправляет данные на сервер об удалении существующего питомца.
        Возвращает статус запроса на сервер и результат в формате json с данными добавленного питомца."""

        headers = {'auth_key': auth_key['key']}

        res = requests.delete(self.base_url + '/api/pets/' + pet_id, headers=headers)

        status = res.status_code
        result = ''
        try:
            result = res.json()
        except json.decoder.JSONDecodeError:
            result = res.text
        return status, result
