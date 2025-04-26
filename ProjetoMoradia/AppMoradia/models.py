from django.db import models
from django.contrib.auth.models import AbstractUser, User



class CustomUser(AbstractUser):
     foto = models.ImageField(
        upload_to='fotos_perfil/',
        blank=True,
        null=True,
        default='fotos_perfil/default.png'
    )

     def __str__(self):
        return self.username