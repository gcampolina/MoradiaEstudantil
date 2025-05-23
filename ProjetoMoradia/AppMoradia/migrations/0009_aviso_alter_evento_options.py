# Generated by Django 5.2 on 2025-04-28 03:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('AppMoradia', '0008_alter_evento_options'),
    ]

    operations = [
        migrations.CreateModel(
            name='Aviso',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('titulo', models.CharField(max_length=200)),
                ('descricao', models.TextField()),
                ('data_criacao', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.AlterModelOptions(
            name='evento',
            options={'ordering': ['-id']},
        ),
    ]
