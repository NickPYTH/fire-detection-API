FROM python:3.13
ENV PYTHONUNBUFFERED 1
RUN mkdir /app
WORKDIR /app
COPY req.txt /app/
RUN pip install --upgrade pip && pip install -r req.txt
ADD . /app/
WORKDIR /app
CMD ["python", "manage.py", "runserver", "0.0.0.0:7777"]