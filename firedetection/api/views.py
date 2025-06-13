# views.py
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import FireEvent
import base64
import numpy as np
import cv2
from rest_framework.generics import ListAPIView, RetrieveAPIView
from rest_framework.permissions import AllowAny
from .serializers import FireEventSerializer
import json

class FireDetectionAPI(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        data = json.loads(request.body)
        
        # Декодируем изображение
        frame_data = data['frame'].split(',')[1]
        frame_bytes = base64.b64decode(frame_data)
        frame_np = np.frombuffer(frame_bytes, dtype=np.uint8)
        frame = cv2.imdecode(frame_np, cv2.IMREAD_COLOR)
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        
        # Создаем запись
        fire_event = FireEvent(
            detection_type=data.get('detection_type', 'fire'),
            confidence=float(data.get('confidence', 0)),
            x1=int(data['coordinates']['x1']),
            y1=int(data['coordinates']['y1']),
            x2=int(data['coordinates']['x2']),
            y2=int(data['coordinates']['y2'])
        )
        
        # Сохраняем сначала модель, чтобы получить detection_time
        fire_event.save()
        
        # Затем сохраняем изображение
        fire_event.save_image_from_frame(frame_rgb)
        fire_event.save()
        
        return Response({'status': 'success', 'event_id': fire_event.id}, status=status.HTTP_201_CREATED)
        

class FireEventList(ListAPIView):
    """Список всех событий о пожарах"""
    queryset = FireEvent.objects.all()
    serializer_class = FireEventSerializer
    permission_classes = [ListAPIView]
    
    def get_queryset(self):
        queryset = super().get_queryset()
        # Фильтрация по типу обнаружения (если указан параметр)
        detection_type = self.request.query_params.get('type')
        if detection_type:
            queryset = queryset.filter(detection_type=detection_type)
        return queryset

class FireEventDetail(RetrieveAPIView):
    """Детальная информация о конкретном событии"""
    queryset = FireEvent.objects.all()
    serializer_class = FireEventSerializer
    permission_classes = [ListAPIView]

