import requests
import allure
import jsonschema

from schemas.store_schema import ORDER_SCHEMA, INVENTORY_SCHEMA

BASE_URL = "http://5.181.109.28:9090/api/v3"


@allure.feature("Store")
class TestStore:
    """Tests for Store"""

    @allure.title("Размещение заказа")
    def test_create_order(self):
        with allure.step("Отправка запроса на создание заказа"):
            body_send_request = {
                "id": 1,
                "petId": 1,
                "quantity": 1,
                "status": "placed",
                "complete": True
            }

            response = requests.post(url=f"{BASE_URL}/store/order", json=body_send_request)

        with allure.step("Проверка статус-кода ответа"):
            assert response.status_code == 200, "Статус ответа не совпал с ER"

        with allure.step("Проверка данных заказа"):
            response_json = response.json()
            assert response_json["petId"] == body_send_request["petId"], "ID питомца не совпал с отправленным"
            assert response_json["quantity"] == body_send_request["quantity"], "Количество питомцев не совпало с отправленным"
            assert response_json["status"] == body_send_request["status"], "Статус заказа не совпал с отправленным"
            assert response_json["complete"] == body_send_request["complete"], "Заказ не завершён"

    @allure.title("Получение информации о заказе по ID")
    def test_get_order_by_id(self, create_order):
        with allure.step("Получение ID созданного заказа"):
            order_id = create_order["id"]

        with allure.step("Отправка запроса на получение информации заказа по ID"):
            response = requests.get(url=f"{BASE_URL}/store/order/{order_id}")

        with allure.step("Проверка статус-кода ответа на получение"):
            assert response.status_code == 200, "Статус не совпал с ER"

        with allure.step("Валидация JSON-схемы заказа"):
            response_json = response.json()
            jsonschema.validate(response_json, ORDER_SCHEMA)

        with allure.step("Проверка данных полученного заказа"):
            assert response_json["petId"] == create_order["petId"], "ID питомца не совпало в заказе"
            assert response_json["quantity"] == create_order["quantity"], "Количество питомцев не совпало"
            assert response_json["status"] == create_order["status"], "Статус заказа не совпал"
            assert response_json["complete"] == create_order["complete"], "Завершённость заказа не совпала"

    @allure.title("Удаление заказа по ID")
    def test_delete_order_by_id(self, create_order):
        with allure.step("Получения ID удаляемого заказа"):
            order_id = create_order["id"]

        with allure.step("Отправка запроса на удаление заказа по ID"):
            delete_response = requests.delete(url=f"{BASE_URL}/store/order/{order_id}")

        with allure.step("Проверка статус-кода ответа на удаление"):
            assert delete_response.status_code == 200, "Код-статус ответа не совпал, заказ не удалился"

        with allure.step("Попытка получить данные удалённого заказа и проверка статус-кода ответа"):
            get_response = requests.get(url=f"{BASE_URL}/store/order/{order_id}")
            assert get_response.status_code == 404, "Статус-код не совпал с ER"

    @allure.title("Попытка получить информацию о несуществующем заказе")
    def test_get_nonexistent_order_by_id(self):
        with allure.step("Отправка запроса на получение информации о несуществующем заказе"):
            response = requests.get(url=f"{BASE_URL}/store/order/9999")

        with allure.step("Проверка статус-кода ответа"):
            assert response.status_code == 404, "Статус-код не совпал с ER, такой заказ существует"

    @allure.title("Получение инвентаря магазина")
    def test_get_store_inventory(self):
        with allure.step("Отправка запроса на получение ингформации об инвентаре магазина"):
            response = requests.get(url=f"{BASE_URL}/store/inventory")

        with allure.step("Проверка статус-кода ответа"):
            assert response.status_code == 200, "Статус-код не совпал с ER, инвентарь пуст"

        with allure.step("Валидация JSON-схемы инвентаря"):
            response_json = response.json()
            jsonschema.validate(response_json, INVENTORY_SCHEMA)