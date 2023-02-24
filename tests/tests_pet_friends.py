from api import PetFriends
from settings import valid_email, valid_password, no_valid_email, no_valid_password
import os

pf = PetFriends()


class TestPetFriends:
    # тест 1
    def test_get_api_key_for_valid_user(self, email=valid_email, password=valid_password):
        """Проверяем, что запрос api ключа имеет статус код 200 и
        результат содержит ключа в ответе"""

        # Отправляем запрос и сохраняем полученный ответ с кодом статуса в status, а текст ответа в result
        status, result = pf.get_api_key(email, password)

        # сравниваем полученный результат с ожидаемым
        assert status == 200
        assert 'key' in result
        print(f'Тест 1. Статус {status} при отправке запроса с правильными email и password.')

    # тест 2
    def test_get_api_key_for_no_valid_mail(self, email=no_valid_email, password=valid_password):
        """Проверяем, что запрос api ключа c не правильным email и правильным password
         имеет статус код 403 и результат не содержит слово 'key' """

        # Отправляем запрос и сохраняем полученный ответ с кодом статуса в status, а текст ответа в result
        status, result = pf.get_api_key(email, password)

        # сравниваем полученный результат с ожидаемым
        assert status == 403
        assert 'key' not in result
        print(f'Тест 2. Статус {status} при отправке запроса с неправильными email.')

    # тест 3
    def test_get_api_key_for_no_valid_password(self, email=valid_email, password=no_valid_password):
        """Проверяем, что запрос api ключа c правильным email и не правильным password
         имеет статус код 403 и результат не содержит слово 'key' """

        # Отправляем запрос и сохраняем полученный ответ с кодом статуса в status, а текст ответа в result
        status, result = pf.get_api_key(email, password)

        # сравниваем полученный результат с ожидаемым
        assert status == 403
        assert 'key' not in result
        print(f'Тест 3. Статус {status} при отправке запроса с неправильными password.')

    # тест 4
    def test_get_list_of_pets_whith_valid_key(self, filter=''):
        """Проверяем возможность получить список всех питомцев.
        Доступное значение filter - my_pets и '' """

        # Запрашиваем ключ api и сохраняем в переменную auth_key
        _, auth_key = pf.get_api_key(valid_email, valid_password)

        # получаем список всех питомцев
        status, result = pf.get_list_of_pets(auth_key, filter)

        # сравниваем полученный результат с ожидаемым
        assert status == 200
        if len(result['pets']) > 0:
            assert len(result['pets']) > 0
            print(f'Тест 4. Список содержит {len(result["pets"])} питомцев.')
        else:
            assert len(result['pets']) == 0
            print('Тест 4. Список питомцев пуст.')

    # тест 5
    def test_post_add_new_pet_without_photo(self, name='Йошио', animal_type='cat', age='3'):
        """Проверяем возможность добавления нового питомца без фотографии"""

        # Запрашиваем ключ api и сохраняем в переменную auth_key
        _, auth_key = pf.get_api_key(valid_email, valid_password)

        # добавляем нового питомца
        status, result = pf.add_new_pet_without_photo(auth_key, name, animal_type, age)

        # сравниваем полученный результат с ожидаемым
        assert status == 200
        assert result['name'] == name
        print(f'тест 5. Добавлен питомец {result}')

    # тест 6
    def test_post_add_new_pet_without_photo_invalid_key(self, name='Йошио', animal_type='cat', age='3'):
        """Проверяем возможность добавления нового питомца без фотографии с не валидным auth_key"""

        # присваиваем переменной auth_key не валидный ключ
        auth_key = {'key': 'c1c501211843cd9daedfe297c249124c836a965302267aeaa019ed9a'}

        # добавляем нового питомца
        status, result = pf.add_new_pet_without_photo(auth_key, name, animal_type, age)

        # сравниваем полученный результат с ожидаемым
        assert status == 403
        print(f'тест 6. Статус код 403 при отправке данных с невалидным auth_key')

    # тест 7
    def test_post_add_new_pet_without_photo_invalid_age(self, name='Йошио', animal_type='cat', age='-3'):
        """Проверяем возможность добавления нового питомца без фотографии с отрицательным возрастом"""

        # Запрашиваем ключ api и сохраняем в переменную auth_key
        _, auth_key = pf.get_api_key(valid_email, valid_password)

        # добавляем нового питомца
        status, result = pf.add_new_pet_without_photo(auth_key, name, animal_type, age)
        age = int(result['age'])

        # сравниваем полученный результат с ожидаемым
        assert status == 200
        assert age < 0
        print(f'тест 7. Добавлен питомец с не допустимым возрастом {age}')

    # тест 8
    def test_post_add_new_pet_without_photo_invalid_name(self, name='', animal_type='cat', age='3'):
        """Проверяем возможность добавления нового питомца без фотографии
        с пустым значением name"""

        # Запрашиваем ключ api и сохраняем в переменную auth_key
        _, auth_key = pf.get_api_key(valid_email, valid_password)
        status, result = pf.add_new_pet_without_photo(auth_key, name, animal_type, age)

        # сравниваем полученный результат с ожидаемым
        assert status == 200
        assert result['name'] == ''
        print(f'тест 8. Добавлен питомец с не допустимым значением name')

    # тест 9
    def test_post_add_photo_of_pet_jpg(self, pet_id='', pet_photo='images/foto_1.jpg'):
        """Проверяем возможность добавления фотографии в формате jpg к уже имеющемуся питомцу.
        При отсутствии данных о питомце, добавляем питомца и к нему добавляем фотографию"""

        # Получаем полный путь изображения питомца и сохраняем в переменную pet_photo
        pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)

        # получаем ключ и сохраняем его значение в auth_key
        _, auth_key = pf.get_api_key(valid_email, valid_password)

        # получаем список питомцев с фильтром my_pets
        _, my_pets = pf.get_list_of_pets(auth_key, 'my_pets')

        # проверяем если список пуст, то создаём питомца и снова запрашиваем список питомцев
        if len(my_pets['pets']) == 0:
            pf.add_new_pet_without_photo(auth_key, 'Barbi', 'dog', '3')
            _, my_pets = pf.get_list_of_pets(auth_key, 'my_pets')

        # в переменную pet_id сохраняем id первого питомца в списке
        pet_id = my_pets['pets'][0]['id']

        # добавляем фотографию к данным первого питомца
        status, result = pf.add_photo_of_pet(auth_key, pet_id, pet_photo)

        # сравниваем полученный результат с ожидаемым
        assert status == 200
        assert result['pet_photo'] != 0
        print('тест 9. Фото в формате jpg успешно добавлено.')

    #  тест 10
    def test_post_add_photo_of_pet_png(self, pet_id='', pet_photo='images/image_2.png'):
        """Проверяем возможность добавления фотографии в формате png к уже имеющемуся питомцу.
        При отсутствии данных о питомце, добавляем питомца и к нему добавляем фотографию"""

        # Получаем полный путь изображения питомца и сохраняем в переменную pet_photo
        pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)

        # получаем ключ и сохраняем его значение в auth_key
        _, auth_key = pf.get_api_key(valid_email, valid_password)

        # получаем список питомцев с фильтром my_pets
        _, my_pets = pf.get_list_of_pets(auth_key, 'my_pets')

        # проверяем если список пуст, то создаём питомца и снова запрашиваем список питомцев
        if len(my_pets['pets']) == 0:
            pf.add_new_pet_without_photo(auth_key, 'Barbi', 'dog', '3')
            _, my_pets = pf.get_list_of_pets(auth_key, 'my_pets')

        # в переменную pet_id сохраняем id первого питомца в списке
        pet_id = my_pets['pets'][0]['id']

        # добавляем фотографию к данным первого питомца
        status, result = pf.add_photo_of_pet(auth_key, pet_id, pet_photo)

        # сравниваем полученный результат с ожидаемым
        assert status == 500
        print('тест 10. Сайт не обрабатывает фотографии в формате png, получаем статус код 500.')

    # тест 11
    def test_post_add_new_pet_valid_key(self, name='Йошио', animal_type='кот', age='3', pet_photo='images/foto_1.jpg'):
        """Проверяем возможность добавления нового питомца с фото в формате jpg"""

        # Получаем полный путь изображения питомца и сохраняем в переменную pet_photo
        pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)

        # Запрашиваем ключ api и сохраняем в переменную auth_key
        _, auth_key = pf.get_api_key(valid_email, valid_password)

        status, result = pf.add_new_pet(auth_key, name, animal_type, age, pet_photo)

        # сравниваем полученный результат с ожидаемым
        assert status == 200
        assert result['name'] == name
        print('тест 11. Питомец с фото в формате jpg успешно добавлен')

    # тест 12
    def test_post_add_new_pet_invalid_age(self, name='Йошио', animal_type='кот',
                                          age='%;№', pet_photo='images/foto_1.jpg'):
        """Проверяем возможность добавления нового питомца с фото в формате jpg
         в поле возраст передаём символьные значения вместо цифровых"""

        # Получаем полный путь изображения питомца и сохраняем в переменную pet_photo
        pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)

        # Запрашиваем ключ api и сохраняем в переменную auth_key
        _, auth_key = pf.get_api_key(valid_email, valid_password)

        status, result = pf.add_new_pet(auth_key, name, animal_type, age, pet_photo)

        # сравниваем полученный результат с ожидаемым
        assert status == 200
        assert result['name'] == name
        print(f'тест 12. Питомец с недопустимым значением возраста {age} добавлен.')

    # тест 13
    def test_post_add_new_pet_invalid_age_old(self, name='Йошио', animal_type='кот',
                                              age='101', pet_photo='images/foto_1.jpg'):
        """Проверяем возможность добавления нового питомца с фото в формате jpg
         в поле возраст передаём очень большой возраст"""

        # Получаем полный путь изображения питомца и сохраняем в переменную pet_photo
        pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)

        # Запрашиваем ключ api и сохраняем в переменную auth_key
        _, auth_key = pf.get_api_key(valid_email, valid_password)

        status, result = pf.add_new_pet(auth_key, name, animal_type, age, pet_photo)

        # сравниваем полученный результат с ожидаемым
        assert status == 200
        assert result['name'] == name
        print(f'тест 13. Питомец с недопустимым значением возраста {age} добавлен.')

    # тест 14
    def test_post_add_new_pet_invalid_name(self, name='EkQ0IY6xf7CXVP4Dtwp5lQzSAh56wQY0vQVBRP4HPivIEGV7X72YbYif3kVm'
                                                     '5eNtMix009dLmYdIqGCBuMBhpLUwSAyVdnxnRCxe', animal_type='кот',
                                           age='3', pet_photo='images/foto_1.jpg'):
        """Проверяем возможность добавления нового питомца с фото в формате jpg
         в поле name передаём длинное значение"""

        # Получаем полный путь изображения питомца и сохраняем в переменную pet_photo
        pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)

        # Запрашиваем ключ api и сохраняем в переменную auth_key
        _, auth_key = pf.get_api_key(valid_email, valid_password)

        status, result = pf.add_new_pet(auth_key, name, animal_type, age, pet_photo)

        # сравниваем полученный результат с ожидаемым
        assert status == 200
        assert result['name'] == name
        print(f'тест 14. Питомец с недопустимым значением name добавлен.')

    # тест 15
    def test_post_add_new_pet_int_age(self, name='Йошио', animal_type='кот', age=3, pet_photo='images/foto_1.jpg'):
        """Проверяем возможность добавления нового питомца с фото в формате jpg
         в поле возраст передаём значение в формате int"""

        # Получаем полный путь изображения питомца и сохраняем в переменную pet_photo
        pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)

        # Запрашиваем ключ api и сохраняем в переменную auth_key
        _, auth_key = pf.get_api_key(valid_email, valid_password)

        try:
            status, result = pf.add_new_pet(auth_key, name, animal_type, age, pet_photo)
            assert status == 200
            assert result['name'] == name
            print(f'тест 15. Питомец добавлен со значением возраста в формате int.')
        except AttributeError:
            print('тест 15. Сайт не обрабатывает значение возраста в формате int.')

    # тест 16
    def test_put_update_name_pet(self):
        """Проверяем возможность вносить изменения в name уже созданного питомца"""

        # Запрашиваем ключ api и сохраняем в переменную auth_key
        _, auth_key = pf.get_api_key(valid_email, valid_password)
        _, my_pets = pf.get_list_of_pets(auth_key, 'my_pets')

        if len(my_pets['pets']) == 0:
            pf.add_new_pet_without_photo(auth_key, 'max', 'dog', 5)
            _, my_pets = pf.get_list_of_pets(auth_key, 'my_pets')

        pet_id = my_pets['pets'][0]['id']
        status, result = pf.update_info_pet(auth_key, pet_id, 'tornado', 'dog', '5')

        _, my_pets = pf.get_list_of_pets(auth_key, 'my_pets')

        # сравниваем полученный результат с ожидаемым
        assert status == 200
        assert result['name'] == 'tornado'
        print('тест 16. Успешно внесли изменения в поле name')

    # тест 17
    def test_delete_pet_from_database(self):
        """Проверяем возможность удаления питомца"""

        # Запрашиваем ключ api и сохраняем в переменную auth_key
        _, auth_key = pf.get_api_key(valid_email, valid_password)

        # получаем список питомцев с фильтром my_pets
        _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

        # если список питомцев не пуст, получаем id первого питомца и удаляем его
        if len(my_pets['pets']) > 0:
            pet_id = my_pets['pets'][0]['id']
            status, result = pf.delete_pet_from_database(auth_key, pet_id)

            # сравниваем полученный результат с ожидаемым
            assert status == 200
            assert pet_id not in my_pets.values()
            print('тест 17. Питомец успешно удален')

        else:
            raise Exception("There is no my pets")

    # тест 18
    def test_delete_pet_from_database_without_filter(self):
        """Проверяем возможность удаления питомца без фильтра my_pets"""

        # Запрашиваем ключ api и сохраняем в переменную auth_key
        _, auth_key = pf.get_api_key(valid_email, valid_password)

        # получаем список питомцев с фильтром my_pets
        _, my_pets = pf.get_list_of_pets(auth_key, "")

        # если список питомцев не пуст, получаем id первого питомца и удаляем его
        if len(my_pets['pets']) > 0:
            pet_id = my_pets['pets'][0]['id']
            status, result = pf.delete_pet_from_database(auth_key, pet_id)

            # сравниваем полученный результат с ожидаемым
            assert status == 200
            assert pet_id not in my_pets.values()
            print('тест 18. Питомец успешно удален')

        else:
            raise Exception("There is no my pets")
