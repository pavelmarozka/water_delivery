import os
from datetime import datetime

summary = f"""# 🛠 Проект: Формирование маршрутного листа

**Последнее обновление:** {datetime.now().strftime('%Y-%m-%d %H:%M')}

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

{os.popen("tree app -I '__pycache__'").read()}

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

"""

with open("project_summary.md", "w", encoding="utf-8") as f:
    f.write(summary)

print("✅ Файл project_summary.md успешно сгенерирован!")
