import allure
import requests

BASE_URL = 'http://5.181.109.28:9090/api/v3'


@allure.feature("Pet")
class TestPet:
    """ Tests for the pet shop functional """

    @allure.title("Попытка удалить несуществующего питомца")
    def test_delete_nonexistent_pet(self, pet_id=9999):
        url_path_delete = f"{BASE_URL + '/pet/' + str(pet_id)}"

        with allure.step("Отправка запроса на удаление несуществующего питомца"):
            response = requests.api.request(method="delete", url=f'{url_path_delete}')

        with allure.step("Проверка статус-кода ответа"):
            assert response.status_code == 200, "Код ответа не совпал с ER"

        with allure.step("Проерка текстового содержимого ответа"):
            assert response.text == "Pet deleted", "Текст ошибки не совпал с ER"