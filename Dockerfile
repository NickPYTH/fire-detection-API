FROM python:3.13
ENV PYTHONUNBUFFERED 1
RUN mkdir /app
WORKDIR /app
COPY . .
RUN pip install --upgrade pip && pip install -r req.txt
WORKDIR firedetection
CMD ["python", "manage.py", "runserver", "0.0.0.0:7777"]