# Generated by Django 5.2 on 2025-05-14 14:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('AppMoradia', '0013_alter_voto_escolha'),
    ]

    operations = [
        migrations.AddField(
            model_name='customuser',
            name='telefone',
            field=models.CharField(blank=True, max_length=11, null=True),
        ),
    ]
