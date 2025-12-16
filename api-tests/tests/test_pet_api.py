import pytest
import allure
from utils.api_client import PetStoreClient
from utils.data_generator import PetDataGenerator

@allure.epic("PetStore API")
@allure.feature("Pet Management")
class TestPetAPI:
    
    @pytest.fixture(autouse=True)
    def setup(self):
        """Фикстура на каждый тест"""
        self.client = PetStoreClient()
        self.generator = PetDataGenerator()
        self.created_pets = []  # Для очистки после тестов
        
        yield
        
        # Пост-очистка: удаляем созданных питомцев
        for pet_id in self.created_pets:
            try:
                self.client.delete_pet(pet_id)
            except:
                pass
    
    # ========== 1. POSITIVE TESTS ==========
    
    @allure.story("Create Pet")
    @allure.title("Создание валидного питомца")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_create_pet_positive(self):
        """POST /pet - Создание питомца с валидными данными"""
        with allure.step("1. Подготовка тестовых данных"):
            pet_data = self.generator.generate_pet_data()
            pet_id = pet_data["id"]
            allure.attach(str(pet_data), name="Pet Data", attachment_type=allure.attachment_type.JSON)
        
        with allure.step("2. Отправка запроса на создание"):
            response = self.client.create_pet(pet_data)
        
        with allure.step("3. Проверка статуса кода"):
            assert response.status_code == 200, f"Expected 200, got {response.status_code}"
            allure.attach(str(response.json()), name="Response", attachment_type=allure.attachment_type.JSON)
        
        with allure.step("4. Проверка структуры ответа"):
            response_json = response.json()
            assert "id" in response_json
            assert response_json["id"] == pet_id
            assert response_json["name"] == pet_data["name"]
            assert response_json["status"] == pet_data["status"]
        
        with allure.step("5. Сохранение ID для последующих тестов"):
            self.created_pets.append(pet_id)
            allure.attach(str(pet_id), name="Created Pet ID", attachment_type=allure.attachment_type.TEXT)
    
    @allure.story("Get Pet")
    @allure.title("Получение существующего питомца по ID")
    def test_get_pet_by_id_positive(self):
        """GET /pet/{petId} - Получение созданного питомца"""
        with allure.step("1. Сначала создаем питомца"):
            pet_data = self.generator.generate_pet_data()
            create_response = self.client.create_pet(pet_data)
            assert create_response.status_code == 200
            created_pet = create_response.json()
            pet_id = created_pet["id"]
            self.created_pets.append(pet_id)
        
        with allure.step("2. Получение питомца по ID"):
            response = self.client.get_pet_by_id(pet_id)
        
        with allure.step("3. Проверка ответа"):
            assert response.status_code == 200
            retrieved_pet = response.json()
            assert retrieved_pet["id"] == pet_id
            assert retrieved_pet["name"] == pet_data["name"]
            # Добавляем сравнение в Allure отчет
            allure.attach(
                f"Expected: {pet_data['name']}\nGot: {retrieved_pet['name']}",
                name="Name Verification",
                attachment_type=allure.attachment_type.TEXT
            )
    
    @allure.story("Find Pets")
    @allure.title("Поиск питомцев по статусу")
    @pytest.mark.parametrize("status", ["available", "pending", "sold"])
    def test_find_pets_by_status(self, status):
        """GET /pet/findByStatus - Поиск по разным статусам"""
        with allure.step(f"1. Поиск питомцев со статусом '{status}'"):
            response = self.client.find_pets_by_status(status)
        
        with allure.step("2. Проверка ответа"):
            assert response.status_code == 200
            pets = response.json()
            assert isinstance(pets, list)
            
            # Проверяем что все питомцы имеют нужный статус
            for pet in pets[:5]:  # Проверяем первые 5
                assert pet["status"] == status, f"Pet {pet['id']} has status {pet['status']}, expected {status}"
            
            allure.attach(f"Found {len(pets)} pets with status '{status}'", 
                         name="Results Count", 
                         attachment_type=allure.attachment_type.TEXT)
    
    # ========== 2. NEGATIVE TESTS ==========
    
    @allure.story("Negative Tests")
    @allure.title("Получение несуществующего питомца")
    @allure.severity(allure.severity_level.NORMAL)
    def test_get_nonexistent_pet(self):
        """GET /pet/{petId} - Запрос несуществующего питомца"""
        with allure.step("1. Используем заведомо несуществующий ID"):
            non_existent_id = -999999999
        
        with allure.step("2. Попытка получения питомца"):
            response = self.client.get_pet_by_id(non_existent_id)
        
        with allure.step("3. Проверка ошибки 404"):
            assert response.status_code == 404
            error_data = response.json()
            assert "message" in error_data
            assert "Pet not found" in error_data["message"]
            allure.attach(str(error_data), name="Error Response", attachment_type=allure.attachment_type.JSON)
    
    @allure.story("Negative Tests")
    @allure.title("Создание питомца с невалидными данными")
    def test_create_pet_invalid_data(self):
        """POST /pet - Создание с невалидными данными"""
        with allure.step("1. Подготовка невалидных данных"):
            invalid_data = self.generator.generate_invalid_pet_data()
            allure.attach(str(invalid_data), name="Invalid Data", attachment_type=allure.attachment_type.JSON)
        
        with allure.step("2. Отправка запроса"):
            response = self.client.create_pet(invalid_data)
        
        with allure.step("3. Проверка ошибки"):
            # Petstore может вернуть 405 или 500 для невалидных данных
            assert response.status_code in [400, 405, 500]
            allure.attach(f"Status code: {response.status_code}", 
                         name="Response Code", 
                         attachment_type=allure.attachment_type.TEXT)
    
    # ========== 3. INTEGRATION TESTS ==========
    
    @allure.story("Integration Tests")
    @allure.title("Полный цикл CRUD операций")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_pet_crud_workflow(self):
        """Полный тест: Create → Read → Update → Delete"""
        
        # 1. CREATE
        with allure.step("1. CREATE - Создание питомца"):
            pet_data = self.generator.generate_pet_data()
            create_response = self.client.create_pet(pet_data)
            assert create_response.status_code == 200
            created_pet = create_response.json()
            pet_id = created_pet["id"]
            self.created_pets.append(pet_id)
            allure.attach(f"Created pet ID: {pet_id}", name="Step 1 - Create", attachment_type=allure.attachment_type.TEXT)
        
        # 2. READ
        with allure.step("2. READ - Получение созданного питомца"):
            get_response = self.client.get_pet_by_id(pet_id)
            assert get_response.status_code == 200
            retrieved_pet = get_response.json()
            assert retrieved_pet["id"] == pet_id
            allure.attach(f"Retrieved pet: {retrieved_pet['name']}", name="Step 2 - Read", attachment_type=allure.attachment_type.TEXT)
        
        # 3. UPDATE
        with allure.step("3. UPDATE - Обновление данных питомца"):
            updated_data = pet_data.copy()
            updated_data["name"] = "Updated_" + updated_data["name"]
            updated_data["status"] = "sold"
            
            update_response = self.client.update_pet(updated_data)
            assert update_response.status_code == 200
            updated_pet = update_response.json()
            assert updated_pet["name"] == updated_data["name"]
            allure.attach(f"Updated name: {updated_pet['name']}", name="Step 3 - Update", attachment_type=allure.attachment_type.TEXT)
        
        # 4. DELETE
        with allure.step("4. DELETE - Удаление питомца"):
            delete_response = self.client.delete_pet(pet_id)
            assert delete_response.status_code == 200
            
            # Удаляем из списка для очистки
            self.created_pets.remove(pet_id)
            
            # Проверяем что питомец удален
            verify_response = self.client.get_pet_by_id(pet_id)
            assert verify_response.status_code == 404
            allure.attach("Pet successfully deleted and verified", name="Step 4 - Delete", attachment_type=allure.attachment_type.TEXT)