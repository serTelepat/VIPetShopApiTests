import allure
import requests

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
    def test_update_nonexistent_pet(self, pet_id=9999):
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
    def test_get_nonexistent_pet(self, pet_id=9999):
        with allure.step("Отправка запроса на получение данных несуществующего питомца"):
            response = requests.get(url=f"{BASE_URL}/pet/{pet_id}")

        with allure.step("Проверка статус-кода ответа"):
            assert response.status_code == 404, "Статус кода не совпал с ER"

        with allure.step("Проверка текстового содержимого ответа"):
            assert response.text == "Pet not found", "Текст ошибки не совпал с ER"
