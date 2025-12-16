from faker import Faker
import random
from typing import Dict, Any

fake = Faker()

class PetDataGenerator:
    """Генератор тестовых данных для Petstore"""
    
    @staticmethod
    def generate_pet_data(pet_id: int = None) -> Dict[str, Any]:
        """Генерация валидных данных питомца"""
        statuses = ["available", "pending", "sold"]
        
        return {
            "id": pet_id or random.randint(1000, 9999),
            "category": {
                "id": random.randint(1, 10),
                "name": fake.word()
            },
            "name": fake.first_name(),
            "photoUrls": [
                "https://example.com/photo1.jpg",
                "https://example.com/photo2.jpg"
            ],
            "tags": [
                {
                    "id": random.randint(1, 5),
                    "name": fake.word()
                }
                for _ in range(random.randint(1, 3))
            ],
            "status": random.choice(statuses)
        }
    
    @staticmethod
    def generate_invalid_pet_data() -> Dict[str, Any]:
        """Генерация невалидных данных"""
        return {
            "id": "invalid_id",  # Строка вместо числа
            "name": None,  # None вместо строки
            "status": "invalid_status"  # Невалидный статус
        }
    
    @staticmethod
    def generate_store_order(order_id: int = None):
        return {
            "id": order_id or random.randint(1, 100),
            "petId": 2,
            "quantity": 3,
            "shipDate": "2025-12-16T05:33:17.453Z",
            "status": "placed",
            "complete": "true"
        }
    
    @staticmethod
    def generate_user_data():
        return {
            "id": random.randint(0, 100),
            "username": fake.word(),
            "firstName": fake.first_name(),
            "lastName": fake.last_name(),
            "email": fake.email(),
            "password": fake.password(),
            "phone": fake.phone_number(),
            "userStatus": 0
        }
    
    @staticmethod
    def generate_invalid_user_data():
        """Генерация невалидных данных"""
        return {
            "id": "invalid_id",  # Строка вместо числа
            "name": None,  # None вместо строки
            "email": "invalid_email"  # Невалидный статус
        } 