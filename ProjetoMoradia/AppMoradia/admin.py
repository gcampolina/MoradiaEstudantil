from django.contrib import admin
from .models import CustomUser, Evento, Aviso, Enquete, Voto



admin.site.register(CustomUser)
admin.site.register(Evento)
admin.site.register(Aviso)
admin.site.register(Enquete)
admin.site.register(Voto)