# views.py
from rest_framework.views import APIView
from django.http import FileResponse
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
        try:
            # Получаем данные из запроса
            data = request.data
            
            # Проверяем и очищаем base64 данные
            frame_data = data.get('frame', '')
            if not frame_data:
                return Response(
                    {"status": "error", "message": "No frame data provided"},
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            # Удаляем префикс data:image/jpeg;base64, если есть
            if 'base64,' in frame_data:
                frame_data = frame_data.split('base64,')[1]
            
            # Добавляем padding если необходимо
            padding = len(frame_data) % 4
            if padding:
                frame_data += '=' * (4 - padding)
            
            try:
                frame_bytes = base64.b64decode(frame_data)
                frame_np = np.frombuffer(frame_bytes, dtype=np.uint8)
                frame = cv2.imdecode(frame_np, cv2.IMREAD_COLOR)
                if frame is None:
                    raise ValueError("Could not decode image")
                
                frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            except Exception as e:
                logger.error(f"Image decoding error: {str(e)}")
                return Response(
                    {"status": "error", "message": "Invalid image data"},
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            # Создаем запись в базе данных
            fire_event = FireEvent(
                detection_type=data.get('detection_type', 'fire'),
                confidence=float(data.get('confidence', 0)),
                x1=int(data.get('coordinates', {}).get('x1', 0)),
                y1=int(data.get('coordinates', {}).get('y1', 0)),
                x2=int(data.get('coordinates', {}).get('x2', 0)),
                y2=int(data.get('coordinates', {}).get('y2', 0))
            )
            
            # Сохраняем сначала модель, чтобы получить detection_time
            fire_event.save()
            
            # Затем сохраняем изображение
            fire_event.save_image_from_frame(frame_rgb)
            fire_event.save()
            
            return Response(
                {'status': 'success', 'event_id': fire_event.id},
                status=status.HTTP_201_CREATED
            )
            
        except Exception as e:
            logger.error(f"API Error: {str(e)}", exc_info=True)
            return Response(
                {'status': 'error', 'message': str(e)},
                status=status.HTTP_400_BAD_REQUEST
            )      



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

class FireEventImageView(APIView):
    def get(self, request, pk):
        try:
            fire_event = FireEvent.objects.get(pk=pk)
            if not fire_event.image:
                return Response({"error": "Image not found"}, status=404)
            
            return FileResponse(fire_event.image.open(), content_type='image/jpeg')
            
        except FireEvent.DoesNotExist:
            return Response({"error": "Event not found"}, status=404)