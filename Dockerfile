FROM python:3.11-slim

# 1. Ставим хром для UI тестов (если они есть)
RUN apt-get update \
    && apt-get install -y --no-install-recommends \
       wget \
       gnupg \
       ca-certificates \
       build-essential \
       gcc \
       libssl-dev \
       libffi-dev \
       python3-dev \
       rustc \
       cargo \
    && wget -q -O - https://dl.google.com/linux/linux_signing_key.pub | gpg --dearmor > /usr/share/keyrings/google-linux-signing-keyring.gpg \
    && echo "deb [signed-by=/usr/share/keyrings/google-linux-signing-keyring.gpg arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main" > /etc/apt/sources.list.d/google.list \
    && apt-get update \
    && apt-get install -y --no-install-recommends google-chrome-stable \
    && rm -rf /var/lib/apt/lists/*

# 2. Рабочая папка
WORKDIR /app

# 3. Копируем зависимости и ставим
COPY requirements.txt .
RUN python -m pip install --upgrade pip setuptools wheel \
    && pip install --no-cache-dir -r requirements.txt

# 4. Копируем ВСЁ
COPY . .

# Ищем все тесты где угодно
CMD sh -c "pytest /app/api-tests -v --alluredir=/app/api-tests/allure-results && \
           allure generate /app/api-tests/allure-results -o /app/api-tests/allure-report --clean"