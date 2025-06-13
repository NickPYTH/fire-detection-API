from django.urls import path
from .views import FireDetectionAPI, FireEventList, FireEventDetail
from .models import FireEvent

urlpatterns = [
    # API для обработки событий от скрипта
    path('fire-detection/', FireDetectionAPI.as_view(), name='fire-detection'),
    
    # API для просмотра событий
    path('events/', FireEventList.as_view(), name='fire-event-list'),
    path('events/<int:pk>/', FireEventDetail.as_view(), name='fire-event-detail'),
    
    # Дополнительные маршруты (по необходимости)
    path('events/latest/', FireEventList.as_view(queryset=FireEvent.objects.order_by('-detection_time')[:5]), 
         name='latest-fire-events'),
]