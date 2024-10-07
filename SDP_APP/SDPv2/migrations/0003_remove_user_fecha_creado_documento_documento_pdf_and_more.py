# Generated by Django 5.0.9 on 2024-09-18 03:29

import SDPv2.models
import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('SDPv2', '0002_sede_documento_dochtml_otheruser_casecreateuser_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='fecha_creado',
        ),
        migrations.AddField(
            model_name='documento',
            name='documento_pdf',
            field=models.FileField(default=12, upload_to=SDPv2.models.upload_to, verbose_name='Documento PDF'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='documento',
            name='autor',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='documento',
            name='enlaceDOI',
            field=models.URLField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='documento',
            name='fechaPublicado',
            field=models.DateField(default=django.utils.timezone.now),
        ),
    ]
