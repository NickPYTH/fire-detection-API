# Используем официальный образ Python
FROM python:3.9-slim
ENV PYTHONUNBUFFERED 1
RUN mkdir /app
WORKDIR /app
COPY . .

# Устанавливаем системные зависимости для OpenCV и других библиотек
RUN apt-get update && apt-get install -y \
    libgl1 \
    libglib2.0-0 \
    libsm6 \
    libxext6 \
    libxrender-dev \
    && rm -rf /var/lib/apt/lists/*

# Устанавливаем зависимости для работы с изображениями
RUN apt-get update && apt-get install -y \
    ffmpeg \
    libsm6 \
    libxext6 \
    && rm -rf /var/lib/apt/lists/*


RUN pip install --upgrade pip && pip install -r req.txt


WORKDIR firedetection
CMD ["python", "manage.py", "runserver", "0.0.0.0:7777"]