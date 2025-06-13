# models.py
from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator

class FireEvent(models.Model):
    class DetectionType(models.TextChoices):
        FIRE = 'fire', 'Пожар'
        SMOKE = 'smoke', 'Дым'
        UNKNOWN = 'unknown', 'Неизвестно'

    # Основные поля
    detection_time = models.DateTimeField('Время обнаружения', auto_now_add=True)
    detection_type = models.CharField('Тип обнаружения', max_length=10, choices=DetectionType.choices)
    confidence = models.FloatField(
        'Уверенность модели',
        validators=[MinValueValidator(0.0), MaxValueValidator(1.0)],
        default=0.0  # Добавьте это
    )    
    # Координаты
    x1 = models.IntegerField('Координата X1', default=0)
    y1 = models.IntegerField('Координата Y1', default=0)
    x2 = models.IntegerField('Координата X2', default=0)
    y2 = models.IntegerField('Координата Y2', default=0)
    
    # Изображение
    image = models.ImageField('Изображение', upload_to='fire_detections/%Y/%m/%d/', default='fire_detections/default.jpg')  # Добавьте default значение)
    
    # Методы
    def save_image_from_frame(self, frame):
        """Сохраняет кадр в ImageField"""
        from PIL import Image
        from io import BytesIO
        from django.core.files.base import ContentFile
        
        img = Image.fromarray(frame)
        buffer = BytesIO()
        img.save(buffer, format='JPEG')
        
        filename = f"detection_{self.detection_time.strftime('%Y%m%d_%H%M%S')}.jpg"
        self.image.save(filename, ContentFile(buffer.getvalue()))