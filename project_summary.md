# 🛠 Проект: Формирование маршрутного листа

**Последнее обновление:** 2025-04-05 23:06

## 📌 Описание
Веб-приложение на Flask для учёта доставок с возможностью формирования маршрутных листов и экспорта их в PDF.

## 🧱 Стек
- Flask
- SQLAlchemy
- Flask-Login
- Flask-Migrate
- PDFKit + ReportLab
- Bootstrap 5, HTMX

## 📂 Структура проекта

app
├── auth
│   ├── forms.py
│   ├── __init__.py
│   └── routes.py
├── delivery
│   ├── forms.py
│   ├── __init__.py
│   ├── routes.py
│   └── utils.py
├── __init__.py
├── models.py
├── static
│   ├── css
│   │   └── styles.css
│   └── js
│       └── main.js
├── templates
│   ├── auth
│   │   └── login.html
│   ├── base.html
│   ├── delivery
│   │   ├── add.html
│   │   ├── add_note.html
│   │   ├── edit.html
│   │   ├── list.html
│   │   └── pdf_template.html
│   ├── errors
│   │   ├── 404.html
│   │   └── 500.html
│   └── home.html
└── utils

11 directories, 21 files


## 🔐 Авторизация
- Flask-Login
- Модель пользователя: `User`

## 🚚 Основной функционал
- Добавление/редактирование/удаление маршрутов
- История маршрутов по дням
- Подсчёт итогов
- Генерация PDF

## 🗃 Модели
- `User`
- `DeliveryRecord`

## 📄 PDF
HTML-шаблон + PDFKit

## 🚀 Запуск

python run.py

