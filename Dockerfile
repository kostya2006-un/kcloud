FROM python:3.10

EXPOSE 8000
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Устанавливаем зависимости системы
RUN apt update && apt install -y \
    gcc \
    libpq-dev \
    dos2unix \
    gettext \
    && rm -rf /var/lib/apt/lists/*

# Устанавливаем рабочую директорию
WORKDIR /app/

# Копируем файлы проекта
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY ./kcloud .

COPY ./server.dev.sh ./server.dev.sh

RUN chmod +x ./server.dev.sh && dos2unix ./server.dev.sh