# Используем официальный образ Python
FROM python:3.11-slim

# Устанавливаем необходимые системные пакеты
RUN apt-get update && apt-get install -y \
    tesseract-ocr \
    tesseract-ocr-eng \
    tesseract-ocr-jpn \
    libtesseract-dev \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Устанавливаем рабочую директорию
WORKDIR /app

# Копируем файлы проекта в контейнер
COPY . /app

# Устанавливаем зависимости Python
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# Запускаем приложение
CMD ["python", "main.py"]

