from api import PetFriends
from settings import valid_email, valid_password, invalid_password, invalid_email, \
                    empty_email, empty_password, invalid_auth_key, empty_auth_key
import os

pf = PetFriends()


def test_get_api_key_for_invalid_password_failed(email=valid_email, password=invalid_password):
    """Запрос ключа с не верным паролем, ожидаемый результат - FAILED"""

    status, _ = pf.get_api_key(email, password)
    assert status == 200


def test_get_api_key_for_invalid_email_failed(email=invalid_email, password=valid_password):
    """Запрос ключа с не верным E-mail, ожидаемый результат - FAILED"""

    status, _ = pf.get_api_key(email, password)
    assert status == 200



def test_get_all_pets_with_empty_key_failed(filter=''):
    """Запрос списка питомцев с пустым ключом, ожидаемый результат - FAILED"""

    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, _ = pf.get_list_of_pets(empty_auth_key, filter)
    assert status == 200


def test_add_new_pet_with_invalid_auth_key_failed(name='98707707', animal_type='667676776',
                                     age='4', pet_photo='images/cat2.gif'):
    """Запрос на добавление питомца с некорректным ключом, ожидаемый результат - FAILED"""

    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.add_new_pet(invalid_auth_key, name, animal_type, age, pet_photo)
    assert status == 200


def test_add_new_pet_with_empty_auth_key_failed(name='pups', animal_type='cat',
                                     age='4', pet_photo='images/kot1.jpg'):
    """Запрос на добавляем питомца с "пустым" ключом, ожидаемый результат - FAILED"""

    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.add_new_pet(empty_auth_key, name, animal_type, age, pet_photo)
    assert status == 200
    assert result['name'] == name

def test_delete_self_pet_invalid_auth_key_failed():
    """Запрос на удаление питомца с "пустым" ключом, ожидаемый результат - FAILED"""

    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")
    if len(my_pets['pets']) == 0:
        pf.add_new_pet(auth_key, "Cat", "Cat", "7", "images/cat1.jpg")
        _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")
    pet_id = my_pets['pets'][0]['id']
    status, _ = pf.delete_pet(invalid_auth_key, pet_id)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")
    assert status == 200
    assert pet_id not in my_pets.values()



def test_successful_add_photo_pet(pet_photo='images/kot1.jpg'):
    """Запрос на добавление фотографии к карточке питомца, ожидаемый результат - PASSED"""

    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, 'my_pets')

    if len(my_pets['pets']) > 0:
        status, result = pf.add_photo_pet(auth_key, my_pets['pets'][0]['id'], pet_photo)
        assert status == 200
        assert "pet_photo" in result
    else:
        raise Exception("There is no my Pets")


def test_add_photo_pet_with_invalid_key_failed(pet_photo='images/kot1.jpg'):
    """Запрос на добавление фотографии к карточке питомца с некорректным ключом, ожидаемый результат - FAILED"""

    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, 'my_pets')
    if len(my_pets['pets']) > 0:
        status, result = pf.add_photo_pet(invalid_auth_key, my_pets['pets'][0]['id'], pet_photo)
        assert status == 200
        assert "pet_photo" in result
    else:
        raise Exception("There is no my Pets")

def test_succesful_add_new_pet_no_photo_with_valid_data(name='Pusik', animal_type='Dog',
                                     age='3'):
    """Запрос на добавление  питомца без фотографии, ожидаемый результат - PASSED"""

    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.add_new_pet_no_photo(auth_key, name, animal_type, age)
    assert status == 200
    assert result['name'] == name

def test_add_new_pet_no_photo_with_invalid_key_failed(name='Pusik', animal_type='Dog',
                                     age='3'):
    """Запрос на добавление  питомца без фотографии с некорректным ключом, ожидаемый результат - FAILED"""

    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.add_new_pet_no_photo(invalid_auth_key, name, animal_type, age)
    assert status != 200
    assert result['name'] == name

def test_get_all_pets_with_valid_key(filter=''):
    """ Проверяем что запрос всех питомцев возвращает не пустой список.
    Для этого сначала получаем api ключ и сохраняем в переменную auth_key. Далее используя этого ключ
    запрашиваем список всех питомцев и проверяем что список не пустой.
    Доступное значение параметра filter - 'my_pets' либо '' """

    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.get_list_of_pets(auth_key, filter)

    assert status == 200
    assert len(result['pets']) > 0

