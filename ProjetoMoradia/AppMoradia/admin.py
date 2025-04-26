from django.contrib import admin
from .models import CustomUser, Evento



admin.site.register(CustomUser)
admin.site.register(Evento)