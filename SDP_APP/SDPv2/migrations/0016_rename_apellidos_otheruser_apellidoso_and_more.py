# Generated by Django 5.0.9 on 2024-09-27 02:54

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('SDPv2', '0015_rename_apellidos_proffessor_apellidosp_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='otheruser',
            old_name='apellidos',
            new_name='apellidosO',
        ),
        migrations.RenameField(
            model_name='otheruser',
            old_name='nombres',
            new_name='nombresO',
        ),
    ]