import pytest
import allure
from utils.api_client import PetStoreClient
from utils.data_generator import PetDataGenerator

@allure.epic("PetStore API")
@allure.feature("Store Management")
class TestStoreApi:
    
    @pytest.fixture(autouse=True)
    def setup(self):
        """Фикстура на каждый тест"""
        self.client = PetStoreClient()
        self.generator = PetDataGenerator()
        self.created_orders = []  # Для очистки после тестов
        
        yield
        
        # Пост-очистка: удаляем созданных заказов
        for order_id in self.created_orders:
            try:
                self.client.delete_order(order_id)
            except:
                pass
    
    # ========== 1. POSITIVE TESTS ==========
    
    @allure.story("Check inventory")
    @allure.title("Проверка инвентаря")
    def test_check_inventory(self):
        """GET /store/inventory - получение данных инвентаря"""
        with allure.step("1. Отправка запроса на создание"):
            response = self.client.get_store_inventory()
        
        with allure.step("2. Проверка статуса кода"):
            assert response.status_code == 200, f"Expected 200, got {response.status_code}"
            allure.attach(str(response.json()), name="Response", attachment_type=allure.attachment_type.JSON)

    @allure.story("Place an order")
    @allure.title("Проверка заказа")
    def test_place_order(self):
        with allure.step("1. создания данных заказа"):
            order_data = self.generator.generate_store_order()
            order_ID = order_data["id"]
            allure.attach(str(order_data), name="Order Data", attachment_type=allure.attachment_type.JSON)

        with allure.step("2. Отправка запроса на создание"):
            response = self.client.place_order(order_data)
        
        with allure.step("3. Проверка статуса кода"):
            assert response.status_code == 200, f"Expected 200, got {response.status_code}"
            allure.attach(str(response.json()), name="Response", attachment_type=allure.attachment_type.JSON)
        
        with allure.step("4. Проверка структуры ответа"):
            response_json = response.json()
            assert "id" in response_json
            assert response_json["id"] == order_ID
            assert response_json["quantity"] == order_data["quantity"]
            assert response_json["status"] == order_data["status"]
        
        with allure.step("5. Сохранение ID для последующих тестов"):
            self.created_orders.append(order_ID)
            allure.attach(str(order_ID), name="Created Order ID", attachment_type=allure.attachment_type.TEXT)

    @allure.story("Check order")
    @allure.title("Проверка заказа")
    @allure.severity(allure.severity_level.NORMAL)
    def test_get_order(self):
        """GET /store/order/{orderId} - Запрос заказа"""
        with allure.step("1. Сначала создаем питомца"):
            order_data = self.generator.generate_store_order()
            order_ID = order_data["id"]
            allure.attach(str(order_data), name="Order Data", attachment_type=allure.attachment_type.JSON)
            response = self.client.place_order(order_data)
            self.created_orders.append(order_ID)

        with allure.step("2. Попытка получения заказа"):
            response = self.client.get_order_by_id(order_ID)
        
        with allure.step("3. Проверка 200"):
            assert response.status_code == 200
            retrieved_order = response.json()
            assert retrieved_order["id"] == order_ID
            # Добавляем сравнение в Allure отчет
            allure.attach(
                f"Expected: {order_ID}\nGot: {retrieved_order['id']}",
                name="Name Verification",
                attachment_type=allure.attachment_type.TEXT
            )
    
    @allure.story("DELETE order")
    @allure.title("Удаление заказа")
    @allure.severity(allure.severity_level.NORMAL)
    def test_delete_order(self):
        """GET /store/order/{orderId} - Запрос заказа"""
        with allure.step("1. Сначала создаем заказ"):
            order_data = self.generator.generate_store_order()
            order_ID = order_data["id"]
            allure.attach(str(order_data), name="Order Data", attachment_type=allure.attachment_type.JSON)
            response = self.client.place_order(order_data)
            self.created_orders.append(order_ID)

        with allure.step("2. удаления заказа"):
            response = self.client.delete_order(order_ID)
        
        with allure.step("3. Проверка 200"):
            assert response.status_code == 200
            # Ответ от DELETE может быть разным, проверяем что есть message
            response_json = response.json()
            assert "message" in response_json
            allure.attach(
                f"Delete response: {response_json}",
                name="Delete Response",
                attachment_type=allure.attachment_type.JSON
            )
        with allure.step("4. Проверяем что заказ действительно удален"):
            check_response = self.client.get_order_by_id(order_ID)
            assert check_response.status_code == 404, f"Order {order_ID} should be deleted but still exists"
            allure.attach(f"Order {order_ID} successfully deleted", 
                        name="Verification", 
                        attachment_type=allure.attachment_type.TEXT)