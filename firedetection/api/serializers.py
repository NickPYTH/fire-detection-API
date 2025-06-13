# serializers.py
from rest_framework import serializers
from .models import FireEvent

class FireEventSerializer(serializers.ModelSerializer):
    image_url = serializers.SerializerMethodField()
    
    class Meta:
        model = FireEvent
        fields = [
            'id',
            'detection_time',
            'detection_type',
            'confidence',
            'image_url',
            'x1', 'y1', 'x2', 'y2',
        ]
    
    def get_image_url(self, obj):
        if obj.image:
            return obj.image.url
        return None