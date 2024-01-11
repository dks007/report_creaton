# Generated by Django 4.2.7 on 2023-12-31 16:12

import datetime
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('dashboard', '0002_alter_sdomaster_created_date_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='menucardmaster',
            name='created_by',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='menu_card_created_by', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='menucardmaster',
            name='created_date',
            field=models.DateTimeField(blank=True, default=datetime.date(2023, 12, 31)),
        ),
        migrations.AlterField(
            model_name='menucardmaster',
            name='updated_by',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='menu_card_updated_by', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='menucardmaster',
            name='updated_date',
            field=models.DateTimeField(blank=True, default=datetime.date(2023, 12, 31)),
        ),
        migrations.AlterField(
            model_name='sdomaster',
            name='created_date',
            field=models.DateTimeField(default=datetime.date(2023, 12, 31)),
        ),
        migrations.AlterField(
            model_name='sdomaster',
            name='updated_date',
            field=models.DateTimeField(default=datetime.date(2023, 12, 31)),
        ),
    ]