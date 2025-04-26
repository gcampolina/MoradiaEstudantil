from django.db import models
from django.contrib.auth.models import AbstractUser, User
from django.conf import settings


class Evento(models.Model):
    titulo = models.CharField(max_length=200)
    descricao = models.TextField()
    data = models.DateField()
    criado_por = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    class Meta:
        ordering = ['-id']

    def __str__(self):
        return f"{self.titulo} ({self.data.strftime('%d/%m/%Y')})"


class CustomUser(AbstractUser):
     foto = models.ImageField(
        upload_to='fotos_perfil/',
        blank=True,
        null=True,
        default='fotos_perfil/default.png'
      )
     
     tipo = (
         ('VISITANTE','Visitante'),
         ('RESIDENTE','Residente'),
         ('SÍNDICO','Síndico'),
         ('COORDENADOR','Coordenador')
     )

     
     tipo = models.CharField(max_length=100, choices=tipo, default='VISITANTE')

     def __str__(self):
        return self.username