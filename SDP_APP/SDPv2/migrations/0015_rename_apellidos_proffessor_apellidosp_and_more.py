# Generated by Django 5.0.9 on 2024-09-27 02:14

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('SDPv2', '0014_remove_user_fecha_creado'),
    ]

    operations = [
        migrations.RenameField(
            model_name='proffessor',
            old_name='apellidos',
            new_name='apellidosP',
        ),
        migrations.RenameField(
            model_name='proffessor',
            old_name='nombres',
            new_name='nombresP',
        ),
    ]
