from django.contrib import admin
from .models import FireEvent

@admin.register(FireEvent)
class FireEventAdmin(admin.ModelAdmin):
    pass
    