# Generated by Django 5.2 on 2025-04-26 14:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('AppMoradia', '0002_customuser_tipo'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customuser',
            name='tipo',
            field=models.CharField(choices=[('VISITANTE', 'Visitante'), ('RESIDENTE', 'Residente'), ('SÍNDICO', 'Síndico'), ('COORDENADOR', 'Coordenador')], default='Visitante', max_length=100),
        ),
    ]
