# Generated by Django 4.2.7 on 2024-03-13 12:05

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0004_customermaster_logo_successreport_logo_url'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='customermaster',
            name='logo',
        ),
        migrations.AddField(
            model_name='customermapping',
            name='logo',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='customer_logo', to='dashboard.logomaster'),
        ),
    ]
