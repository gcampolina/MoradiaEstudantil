# Generated by Django 5.2 on 2025-04-26 15:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('AppMoradia', '0003_alter_customuser_tipo'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customuser',
            name='tipo',
            field=models.CharField(choices=[('VISITANTE', 'Visitante'), ('RESIDENTE', 'Residente'), ('SÍNDICO', 'Síndico'), ('COORDENADOR', 'Coordenador')], default='VISITANTE', max_length=100),
        ),
    ]
