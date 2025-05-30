# Generated by Django 4.2.20 on 2025-05-03 08:30

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('main_app', '0002_property_image'),
    ]

    operations = [
        migrations.CreateModel(
            name='Amenity',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('property', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main_app.property')),
            ],
        ),
    ]
