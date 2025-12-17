# 🧪 QA Automation Portfolio

<div align="center">
  
![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Pytest](https://img.shields.io/badge/Pytest-0A9EDC?style=for-the-badge&logo=pytest&logoColor=white)
![Selenium](https://img.shields.io/badge/Selenium-43B02A?style=for-the-badge&logo=selenium&logoColor=white)
![Allure](https://img.shields.io/badge/Allure-FF6A6A?style=for-the-badge)
![GitHub Actions](https://img.shields.io/badge/GitHub_Actions-2088FF?style=for-the-badge&logo=github-actions&logoColor=white)
![Docker](https://img.shields.io/badge/Docker-2496ED?style=for-the-badge&logo=docker&logoColor=white)

**Профессиональный набор автоматизированных тестов QA Engineer**

<img width="1917" height="992" alt="изображение" src="https://github.com/user-attachments/assets/067d663e-6ec8-4e77-88b8-f00b6473d697" />

<img width="1920" height="955" alt="изображение" src="https://github.com/user-attachments/assets/f390097e-ce32-4fe2-a458-914ea6e407dd" />

</div>

## 📋 Оглавление
- [🚀 Быстрый старт](#-быстрый-старт)
- [📊 Что реализовано](#-что-реализовано)
- [🏗️ Архитектура проекта](#️-архитектура-проекта)
- [🎯 Ключевые особенности](#-ключевые-особенности)
- [📈 Примеры отчётов](#-примеры-отчётов)
- [🛠 Технологический стек](#-технологический-стек)
- [📁 Структура проекта](#-структура-проекта)
- [🤝 Контакты](#-контакты)

## 🚀 Быстрый старт

### 1️⃣ Локальный запуск
```bash
# 1. Клонировать репозиторий
git clone https://github.com/<ТВОЙ_USERNAME>/QA.git
cd QA

# 2. Установить зависимости
pip install -r requirements.txt

# 3. Запустить API тесты
pytest -v --alluredir=allure-results

# 4. Сгенерировать отчёт
allure generate allure-results -o allure-report --clean
allure open allure-report
```

### 2️⃣ Запуск в Docker
```bash
# Собрать образ и запустить тесты
docker build -t qa-tests .
docker run --rm -v $(pwd)/allure-report:/app/allure-report qa-tests
```

### 3️⃣ Просмотр результатов CI/CD
1. Перейдите на вкладку **Actions** в репозитории
2. Выберите последний успешный workflow
3. Скачайте артефакт **allure-report** для просмотра отчёта тестирования API

## 📊 Что реализовано

### ✅ **API тестирование (13 тестов)**
| Модуль | Эндпоинты | Тестов | Статус |
|--------|-----------|--------|--------|
| **Pet API** | `POST/GET/PUT/DELETE /pet` | 8 | ✅ |
| **Store API** | `POST/GET/DELETE /store/order` | 3 | ✅ |
| **User API** | `POST/GET /user` | 1 | ✅ |

### 🖥️ **UI тестирование (21 тест)**
| Страница | Тестов | Технология |
|----------|--------|------------|
| [the-internet.herokuapp.com](https://the-internet.herokuapp.com) | 21 | Selenium WebDriver |

### 🔄 **CI/CD Pipeline**
- **Автоматический запуск** тестов при каждом push/pull request
- **Генерация Allure отчётов** с историей запусков
- **Артефакты сборки** для скачивания результатов

## 🏗️ Архитектура проекта

```mermaid
graph TB
    A[GitHub Push/PR] --> B[GitHub Actions]
    B --> C[Setup Python 3.11]
    C --> D[Install Dependencies]
    D --> E[Run API Tests]
    E --> F[Generate Allure Report]
    F --> G[Upload Artifacts]
    G --> H[🚀 Success / ❌ Failure]
    
    I[Local Development] --> J[Pytest Runner]
    J --> K[API: PetStore]
    J --> L[UI: Selenium]
    K --> M[Allure Results]
    L --> M
    M --> N[Allure Report]
```

## 🎯 Ключевые особенности

### 🧪 **Комплексное покрытие тестами**
- **Положительные и негативные сценарии**
- **Валидация ответов** (статус коды, схемы JSON)
- **Автоматическая очистка** тестовых данных
- **Параметризованные тесты** для разных статусов

### 📊 **Профессиональные отчёты**
- **Allure Framework** с графиками и историей
- **Группировка тестов** по эпикам, фичам, стори
- **Вложения** (JSON запросы/ответы, скриншоты)
- **Метрики производительности**

### 🔧 **Надёжная инфраструктура**
- **Изоляция тестов** через Docker
- **Повторные попытки** для флакки-тестов
- **Генерация тестовых данных** через Faker
- **Конфигурация через переменные окружения**

## 📈 Примеры отчётов

<img width="1919" height="953" alt="изображение" src="https://github.com/user-attachments/assets/5dc187b7-19dc-4feb-8558-c785807d9bcf" />


### 🎨 **Визуализация результатов**
| График | Описание |
|--------|----------|
| **📈 Тренды** | История прохождения тестов по запускам |
| **📋 Категории** | Распределение по severity (Blocker, Critical, Normal) |
| **⏱️ Тайминги** | Время выполнения каждого теста |
| **🧩 Группировки** | Тесты по фичам и стори |

## 🛠 Технологический стек

| Категория | Технологии |
|-----------|------------|
| **Язык/Фреймворк** | Python 3.11, Pytest 7.4.4 |
| **API тестирование** | Requests, Allure-Pytest |
| **UI тестирование** | Selenium 4, WebDriver Manager |
| **Отчётность** | Allure Framework, Pytest-HTML |
| **CI/CD** | GitHub Actions, Docker |
| **Утилиты** | Faker, Python-dotenv, Retrying |
| **Мониторинг** | Allure History, Custom Logging |


## Структура Проекта

<img width="7904" height="1603" alt="deepseek_mermaid_20251217_23df2f" src="https://github.com/user-attachments/assets/46be3787-2cb5-493f-8757-5b9938e160c4" />


## 🤝 Контакты

<div align="center">

**Григорий Захаров**  
QA Automation Engineer//Fullstack dev

[![Email](https://img.shields.io/badge/Email-zakharov9933@gmail.com-D14836?style=flat&logo=gmail&logoColor=white)](mailto:zakharov9933@gmail.com)
[![GitHub](https://img.shields.io/badge/GitHub-GrigoryZakharov-181717?style=flat&logo=github&logoColor=white)](https://github.com/GrigoryZakharov)
[![LinkedIn](https://img.shields.io/badge/LinkedIn-grigory--zakharov-0077B5?style=flat&logo=linkedin&logoColor=white)](https://www.linkedin.com/in/grigory-zakharov-577561389/)

</div>

---

<div align="center">
  
⭐ **Если этот проект был полезен, поставь звезду на GitHub!** ⭐

</div>
