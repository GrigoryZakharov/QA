import requests
import logging
from typing import Optional, Dict, Any
from urllib.parse import urljoin

class PetStoreClient:
    """Клиент для работы с Petstore API"""
    
    def __init__(self, base_url: str = "https://petstore.swagger.io/v2/"):
        self.base_url = base_url
        self.session = requests.Session()
        self.session.headers.update({
            "Content-Type": "application/json",
            "api_key": "special-key" # Если требуется API ключ
        })
        logging.basicConfig(level=logging.INFO)
        self.logger = logging.getLogger(__name__)
    
    def _make_request(self, method: str, endpoint: str, **kwargs) -> requests.Response:
        """Базовый метод для запросов"""
        url = urljoin(self.base_url, endpoint)
        self.logger.info(f"{method} {url}")
        
        try:
            response = self.session.request(method, url, **kwargs)
            self.logger.info(f"Response: {response.status_code}")
            return response
        except requests.exceptions.RequestException as e:
            self.logger.error(f"Request failed: {e}")
            raise
    
    # PET методы
    def create_pet(self, pet_data: Dict[str, Any]) -> requests.Response:
        """POST /pet - Создание питомца"""
        return self._make_request("POST", "pet", json=pet_data)
    
    def get_pet_by_id(self, pet_id: int) -> requests.Response:
        """GET /pet/{petId} - Получение питомца"""
        return self._make_request("GET", f"pet/{pet_id}")
    
    def update_pet(self, pet_data: Dict[str, Any]) -> requests.Response:
        """PUT /pet - Обновление питомца"""
        return self._make_request("PUT", "pet", json=pet_data)
    
    def find_pets_by_status(self, status: str) -> requests.Response:
        """GET /pet/findByStatus - Поиск по статусу"""
        return self._make_request("GET", f"pet/findByStatus?status={status}")
    
    def delete_pet(self, pet_id: int) -> requests.Response:
        """DELETE /pet/{petId} - Удаление питомца"""
        return self._make_request("DELETE", f"pet/{pet_id}")
    
    def upload_pet_image(self, pet_id: int, file_path: str) -> requests.Response:
        """POST /pet/{petId}/uploadImage - Загрузка изображения"""
        with open(file_path, 'rb') as file:
            files = {'file': file}
            return self._make_request("POST", f"pet/{pet_id}/uploadImage", files=files)
        
    #Store методы
    def get_store_inventory(self):
        """GET /store/inventory - получение инвенторя"""
        return self._make_request("GET", f"store/inventory")
    
    def place_order(self, order_data):
        """POST /store/order - сделат заказ"""
        return self._make_request("POST", "store/order", json=order_data)
    
    def get_order_by_id(self, order_id):
        """GET /store/order/{order_id}"""
        return self._make_request("GET", f"store/order/{order_id}")
    
    def delete_order(self, order_id):
        """DELETE /store/order/{order_id}"""
        return self._make_request("DELETE", f"store/order/{order_id}")
    
    #User методы
    def create_user(self, user_data):
        """POST /user - сделать пользователя"""
        return self._make_request("POST", f"user", json = user_data)
    
    def get_user_by_username(self, username):
        """GET /user/{username}"""
        return self._make_request("GET", f"user/{username}")
    
    def user_login(self, username, password):
        """GET /user/login"""
        return self._make_request("GET", f"user/login?username={username}&password={password}")
    
    def user_logout(self):
        """GET /user/logout"""
        return self._make_request("GET", "user/logout")
    
    def delete_user_by_username(self, username):
        """DELETE /user/{username}"""
        return self._make_request("DELETE", f"user/{username}")