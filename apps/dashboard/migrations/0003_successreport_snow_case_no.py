# Generated by Django 4.2.7 on 2024-02-16 16:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0002_alter_menucardmaster_template_file_name_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='successreport',
            name='snow_case_no',
            field=models.CharField(max_length=10, null=True),
        ),
    ]
