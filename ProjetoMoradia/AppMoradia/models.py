from django.db import models
from django.contrib.auth.models import AbstractUser, User
from django.conf import settings





class Enquete(models.Model):

    STATUS_CHOICES = [
        ('ATIVA', 'Ativa'),
        ('ENCERRADA', 'Encerrada'),
    ]

    pergunta = models.CharField(max_length=255)
    criado_por = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    data_criacao = models.DateTimeField(auto_now_add=True)
    data_encerramento = models.DateTimeField(null=True, blank=True)
    status = models.CharField(max_length=10,choices=STATUS_CHOICES,default='ATIVA')

    def __str__(self):
        return self.pergunta
    
class Voto(models.Model):

    STATUS_CHOICES = [
        ('SIM', 'Sim'),
        ('NÃO', 'Não'),
    ]
    
    enquete = models.ForeignKey(Enquete, related_name='votos', on_delete=models.CASCADE)
    usuario = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    escolha = models.CharField(max_length=10,choices=STATUS_CHOICES)

    def __str__(self):
         return f"Voto do {self.usuario.username} na enquete: {self.enquete.pergunta}"


class Aviso(models.Model):
    titulo = models.CharField(max_length=200)
    descricao = models.TextField()
    data_criacao = models.DateTimeField(auto_now_add=True)
    criado_por = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    
    def __str__(self):
        return self.titulo

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