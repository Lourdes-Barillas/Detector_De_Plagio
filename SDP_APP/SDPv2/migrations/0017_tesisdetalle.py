# Generated by Django 5.0.9 on 2024-09-28 00:39

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('SDPv2', '0016_rename_apellidos_otheruser_apellidoso_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='TesisDetalle',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('pregunta_investigacion', models.TextField(verbose_name='Pregunta de investigación')),
                ('objetivo_general', models.TextField(verbose_name='Objetivo general')),
                ('resumen', models.TextField(verbose_name='Resumen de la tesis')),
                ('sede', models.CharField(max_length=150, verbose_name='Sede')),
                ('doi', models.URLField(blank=True, null=True, verbose_name='DOI (Enlace)')),
                ('documento', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='detalles', to='SDPv2.documento')),
            ],
            options={
                'verbose_name': 'Tesis Detalle',
                'verbose_name_plural': 'Tesis Detalles',
                'db_table': 'tesis_detalle',
                'ordering': ['documento'],
            },
        ),
    ]
