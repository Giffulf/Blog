# Blog API 🚀  

FastAPI-приложение для блога с возможностью создания постов, комментариев и аутентификации пользователей.  

[![FastAPI](https://img.shields.io/badge/FastAPI-005571?style=flat&logo=fastapi)](https://fastapi.tiangolo.com/)
[![Python](https://img.shields.io/badge/Python-3.9+-blue?logo=python)](https://python.org)
[![Docker](https://img.shields.io/badge/Docker-2496ED?logo=docker)](https://docker.com)
[![License](https://img.shields.io/badge/license-MIT-green)](LICENSE)

## 📌 О проекте  

Проект был создан в рамках учебной практики.

Бэкенд для блога с:  
- JWT-аутентификацией  
- CRUD для постов и комментариев  
- Документацией Swagger/Redoc  
- Поддержкой Docker  

## 🛠 Быстрый старт  

### 1. Установка (без Docker)  

bash
# Создать виртуальное окружение
python -m venv .venv

# Активировать (Windows)
.venv\Scripts\activate.bat

# Установить зависимости
pip install -r requirements.txt

# Запустить сервер
fastapi dev main.py

### 2. Запуск через Docker  

bash
# Собрать и запустить контейнер
docker-compose up -d --build

# Остановить контейнер
docker-compose down

После запуска откройте:  
- Документация: [http://localhost:8000/docs](http://localhost:8000/docs)  
- Redoc: [http://localhost:8000/redoc](http://localhost:8000/redoc)  
