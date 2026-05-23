import allure
import requests
import jsonschema

from .schemas.pet_schema import PET_SCHEMA

BASE_URL = 'http://5.181.109.28:9090/api/v3'


@allure.feature("Pet")
class TestPet:
    """ Tests for the pet functional """

    @allure.title("Попытка удалить несуществующего питомца")
    def test_delete_nonexistent_pet(self, pet_id=9999):
        with allure.step("Отправка запроса на удаление несуществующего питомца"):
            response = requests.delete(url=f"{BASE_URL}/pet/{pet_id}")

        with allure.step("Проверка статус-кода ответа"):
            assert response.status_code == 200, "Код ответа не совпал с ER"

        with allure.step("Проверка текстового содержимого ответа"):
            assert response.text == "Pet deleted", "Текст ошибки не совпал с ER"

    @allure.title("Попытка обновить несуществующего питомца")
    def test_update_nonexistent_pet(self):
        pet_id = 9999
        with allure.step("Отправка запроса на обновление несуществующего питомца"):
            body_send_request = {
                "id": pet_id,
                "name": "Non-existent Pet",
                "status": "available"
            }

            response = requests.put(url=f"{BASE_URL}/pet", json=body_send_request)

        with allure.step("Проверка статус-кода ответа"):
            assert response.status_code == 404, "Код ответа не совпал с ER"

        with allure.step("Проверка текстового содержимого ответа"):
            assert response.text == "Pet not found", "Текст ошибки не совпал с ER"

    @allure.title("Попытка получить данные несуществующего питомца")
    def test_get_nonexistent_pet(self):
        pet_id = 9999
        with allure.step("Отправка запроса на получение данных несуществующего питомца"):
            response = requests.get(url=f"{BASE_URL}/pet/{pet_id}")

        with allure.step("Проверка статус-кода ответа"):
            assert response.status_code == 404, "Статус кода не совпал с ER"

        with allure.step("Проверка текстового содержимого ответа"):
            assert response.text == "Pet not found", "Текст ошибки не совпал с ER"

    @allure.title("Добавление нового питомца с неполными данными")
    def test_add_new_pet(self):
        with allure.step("Отправление запроса на добавление нового питомца"):
            body_send_request = {
                "id": 1,
                "name": "Buddy",
                "status": "available"
            }

            response = requests.post(url=f"{BASE_URL}/pet", json=body_send_request)

        with allure.step("Проверка статус-кода ответа"):
            assert response.status_code == 200, "Статус кода не совпал с ER"

        with allure.step("Валидация JSON-схемы"):
            response_json = response.json()
            jsonschema.validate(response_json, PET_SCHEMA)

        with allure.step("Проверка на соответствие отправленных и полученных значений"):
            assert response_json["id"] == body_send_request["id"], "ID не совпал с ER"
            assert response_json["name"] == body_send_request["name"], "Имя питомца не совпало с ER"
            assert response_json["status"] == body_send_request["status"], "Статус не воспал с ER"

    @allure.title("Добавление нового питомца с полными данными")
    def test_add_new_pet_with_full_datas(self):
        with allure.step("Отправление запроса на добавление нового питомца"):
            body_send_request = {
                "id": 10,
                "name": "doggie",
                "category": {
                    "id": 1,
                    "name": "Dogs"
                },
                "photoUrls": ["string"],
                "tags": [{
                    "id": 0,
                    "name": "string"
                }],
                "status": "available"
            }

            response = requests.post(url=f"{BASE_URL}/pet", json=body_send_request)

        with allure.step("Проверка статус-кода ответа"):
            assert response.status_code == 200, "Статус кода не совпал с ER"

        with allure.step("Валидация JSON-схемы"):
            response_json = response.json()
            jsonschema.validate(response_json, PET_SCHEMA)

        with allure.step("Проверка на соответствие отправленных и полученных значений"):
            assert response_json["id"] == body_send_request["id"], "ID не совпал с ER"
            assert response_json["name"] == body_send_request["name"], "Имя питомца не совпало с ER"
            assert response_json["category"] == body_send_request["category"], "Категория не совпала с ER"
            assert response_json["photoUrls"] == body_send_request["photoUrls"], "Ссылка на фото не совпала с ER"
            assert response_json["tags"] == body_send_request["tags"], "Теги не совпали с ER"
            assert response_json["status"] == body_send_request["status"], "Статус не совпал с ER"

    @allure.title("Получение информации о питомце по ID")
    def test_get_pet_by_id(self, create_pet):
        with allure.step("Получение ID созданного питомца"):
            pet_id = create_pet["id"]

        with allure.step("Проверка статуса ответа и полученного ID питомца"):
            response = requests.get(url=f"{BASE_URL}/pet/{pet_id}")
            assert response.status_code == 200, "Статус-код не совпал с ER"
            assert response.json()["id"] == pet_id, "ID питомца не совпал с ER"

    @allure.title("Обновление информации о питомце по ID")
    def test_update_pet_by_id(self, create_pet):
        with allure.step("Получение ID созданного питомца"):
            pet_id = create_pet["id"]

        with allure.step("Обновление данных по ID"):
            body_send_request = {
                "id": pet_id,
                "name": "Buddy Updated",
                "status": "sold"
            }

            response = requests.put(url=f"{BASE_URL}/pet", json=body_send_request)

        with allure.step("Валидация JSON-схемы"):
            response_json = response.json()
            jsonschema.validate(response_json, PET_SCHEMA)

        with allure.step("Проверка статус-кода ответа"):
            assert response.status_code == 200, "Статус-код не совпал с ER"

        with allure.step("Проверка обновлённых данных ответа"):
            assert response_json["id"] == pet_id, "ID обновлённого питомца не совпало с ER"
            assert response_json["name"] == body_send_request["name"], "Имя не совпало с обновлённым именем питомца"
            assert response_json["status"] == body_send_request["status"], "Статус питомца не совпал с обновлёным"

    @allure.title("Удаление питомца по ID")
    def test_delete_pet_by_id(self, create_pet):
        with allure.step("Получение ID созданного питомца"):
            pet_id = create_pet["id"]

        with allure.step("Удаление питомца по заданному ID"):
            response_delete = requests.delete(url=f"{BASE_URL}/pet/{pet_id}")

        with allure.step("Проверка статус-кода удаления питомца"):
            assert response_delete.status_code == 200, "Статус-код ответа на удаление питомца не совпал с ER"

        with allure.step("Проверка на удаление существующего питомца"):
            response_get = requests.get(url=f"{BASE_URL}/pet/{pet_id}")
            assert response_get.status_code == 404, "Питомец не удалился, статус-код ответа не совпал с ER"
