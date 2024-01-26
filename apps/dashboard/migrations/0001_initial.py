# Generated by Django 4.2.7 on 2024-01-23 05:05

import datetime
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion

class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='CapabilityMaster',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('capability_name', models.CharField(max_length=255)),
                ('capability_description', models.TextField(blank=True, null=True)),
                ('created_date', models.DateTimeField(auto_now_add=True)),
                ('updated_date', models.DateTimeField(auto_now=True)),
                ('created_by', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='capability_created_by', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='CreatorMaster',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('creator_account_id', models.CharField(max_length=255)),
                ('creator_name', models.CharField(max_length=255)),
                ('creator_email', models.CharField(max_length=255)),
                ('created_date', models.DateTimeField(auto_now_add=True, null=True)),
                ('updated_date', models.DateTimeField(auto_now_add=True)),
                ('created_by', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='creator_created_by', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='CSMMaster',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('csm_name', models.CharField(max_length=255)),
                ('csm_email', models.CharField(max_length=255)),
                ('created_date', models.DateTimeField(auto_now_add=True)),
                ('updated_date', models.DateTimeField(auto_now=True)),
                ('created_by', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='csm_created_by', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='CustomerMaster',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('customer_id', models.CharField(max_length=255)),
                ('customer_name', models.CharField(max_length=255)),
                ('created_date', models.DateTimeField(auto_now_add=True)),
                ('updated_date', models.DateTimeField(auto_now=True)),
                ('created_by', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='customer_created_by', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='ExpertMaster',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('expert_account_id', models.CharField(max_length=255)),
                ('expert_name', models.CharField(max_length=255)),
                ('expert_email', models.CharField(max_length=255)),
                ('created_date', models.DateTimeField(auto_now_add=True, null=True)),
                ('updated_date', models.DateTimeField(auto_now_add=True)),
                ('created_by', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='expert_created_by', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='LogoMaster',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('logo_file_name', models.CharField(max_length=8)),
                ('logo_file_type', models.CharField(max_length=10, null=True)),
                ('logo_file_size', models.IntegerField()),
                ('logo_url', models.CharField(max_length=255)),
                ('logo', models.BinaryField(null=True)),
                ('created_date', models.DateTimeField(auto_now_add=True, null=True)),
                ('updated_date', models.DateTimeField(auto_now_add=True)),
                ('created_by', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='logo_created_by', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='MenuCardMaster',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('menu_card', models.CharField(max_length=10)),
                ('menu_description', models.TextField()),
                ('template_file_name', models.CharField(max_length=255, null=True)),
                ('template_file_path', models.TextField(null=True)),
                ('template_file_type', models.CharField(max_length=10, null=True)),
                ('template_file_size', models.IntegerField(null=True)),
                ('created_date', models.DateTimeField(auto_now_add=True)),
                ('updated_date', models.DateTimeField(auto_now_add=True)),
                ('created_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='menu_card_created_by', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='ProductMaster',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('product_name', models.CharField(max_length=255)),
                ('product_description', models.TextField(blank=True, null=True)),
                ('created_date', models.DateTimeField(auto_now_add=True)),
                ('updated_date', models.DateTimeField(auto_now=True)),
                ('created_by', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='product_created_by', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='ReportStatusMaster',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('report_status_name', models.CharField(max_length=255)),
                ('status_description', models.CharField(blank=True, max_length=255, null=True)),
                ('created_date', models.DateTimeField(auto_now_add=True)),
                ('updated_date', models.DateTimeField(auto_now_add=True)),
                ('created_by', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='report_status_created_by', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='StatusMaster',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('status_name', models.CharField(max_length=255)),
                ('created_date', models.DateTimeField(auto_now_add=True)),
                ('updated_date', models.DateTimeField(auto_now_add=True)),
                ('status_description', models.CharField(blank=True, max_length=255, null=True)),
                ('created_by', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='status_created_by', to=settings.AUTH_USER_MODEL)),
                ('updated_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='status_updated_by', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='SubCapabilityMaster',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('sub_capability_name', models.CharField(max_length=255)),
                ('sub_capability_description', models.TextField(blank=True, null=True)),
                ('created_date', models.DateTimeField(auto_now_add=True)),
                ('updated_date', models.DateTimeField(auto_now=True)),
                ('capability', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='dashboard.capabilitymaster')),
                ('created_by', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='sub_capability_created_by', to=settings.AUTH_USER_MODEL)),
                ('status', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='sub_capability_status', to='dashboard.statusmaster')),
                ('updated_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='sub_capability_updated_by', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='SuccessServiceMaster',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('success_service_name', models.CharField(max_length=255)),
                ('created_date', models.DateTimeField(auto_now_add=True)),
                ('updated_date', models.DateTimeField(auto_now=True)),
                ('created_by', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='success_service_created_by', to=settings.AUTH_USER_MODEL)),
                ('status', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='success_service_status', to='dashboard.statusmaster')),
                ('updated_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='success_service_updated_by', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='SuccessReport',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('parent_key', models.CharField(blank=True, max_length=100, null=True)),
                ('jira_key', models.CharField(max_length=100)),
                ('error_msg', models.CharField(max_length=255, null=True)),
                ('download_link', models.TextField(null=True)),
                ('approved_by_sdo', models.CharField(max_length=10, null=True)),
                ('approved_sdo_date', models.DateField(null=True)),
                ('approved_by_csm', models.CharField(max_length=10, null=True)),
                ('approved_csm_date', models.DateField(null=True)),
                ('approved_by_sdm', models.CharField(max_length=10, null=True)),
                ('approved_sdm_date', models.DateField(null=True)),
                ('created_date', models.DateTimeField(auto_now_add=True, null=True)),
                ('updated_date', models.DateTimeField(auto_now_add=True, null=True)),
                ('capability', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='dashboard.capabilitymaster')),
                ('created_by', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='success_report_created_by', to=settings.AUTH_USER_MODEL)),
                ('creator', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='dashboard.creatormaster')),
                ('customer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='dashboard.customermaster')),
                ('expert', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='dashboard.expertmaster')),
                ('logo', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='dashboard.logomaster')),
                ('menu_card', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='dashboard.menucardmaster')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='dashboard.productmaster')),
                ('report_status', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='dashboard.reportstatusmaster')),
                ('status', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='dashboard.statusmaster')),
                ('sub_capability', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='dashboard.subcapabilitymaster')),
                ('updated_by', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='success_report_updated_by', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='SuccessElementsMaster',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('success_element_name', models.CharField(max_length=255)),
                ('created_date', models.DateTimeField(auto_now_add=True)),
                ('updated_date', models.DateTimeField(auto_now=True)),
                ('created_by', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='success_element_created_by', to=settings.AUTH_USER_MODEL)),
                ('status', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='success_element_status', to='dashboard.statusmaster')),
                ('updated_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='success_element_updated_by', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='SdoMaster',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sdo_name', models.CharField(max_length=255)),
                ('sdo_email', models.CharField(blank=True, max_length=255, null=True)),
                ('created_date', models.DateTimeField(default=datetime.date(2024, 1, 23))),
                ('updated_date', models.DateTimeField(default=datetime.date(2024, 1, 23))),
                ('created_by', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='sdo_created_by', to=settings.AUTH_USER_MODEL)),
                ('status', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='sdo_status', to='dashboard.statusmaster')),
                ('updated_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='sdo_updated_by', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='SDMMaster',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('sdm_name', models.CharField(max_length=255)),
                ('sdm_email', models.CharField(max_length=255)),
                ('created_date', models.DateTimeField(auto_now_add=True)),
                ('updated_date', models.DateTimeField(auto_now=True)),
                ('created_by', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='sdm_created_by', to=settings.AUTH_USER_MODEL)),
                ('status', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='sdm_status', to='dashboard.statusmaster')),
                ('updated_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='sdm_updated_by', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='reportstatusmaster',
            name='status',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='report_status_status', to='dashboard.statusmaster'),
        ),
        migrations.AddField(
            model_name='reportstatusmaster',
            name='updated_by',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='report_status_updated_by', to=settings.AUTH_USER_MODEL),
        ),
        migrations.CreateModel(
            name='RegionMaster',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('region_name', models.CharField(max_length=255)),
                ('created_date', models.DateTimeField(auto_now_add=True)),
                ('updated_date', models.DateTimeField(auto_now=True)),
                ('created_by', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='region_created_by', to=settings.AUTH_USER_MODEL)),
                ('status', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='region_status', to='dashboard.statusmaster')),
                ('updated_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='region_updated_by', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='PSMMaster',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('psm_name', models.CharField(max_length=255)),
                ('psm_email', models.CharField(max_length=255)),
                ('created_date', models.DateTimeField(auto_now_add=True)),
                ('updated_date', models.DateTimeField(auto_now=True)),
                ('created_by', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='psm_created_by', to=settings.AUTH_USER_MODEL)),
                ('status', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='psm_status', to='dashboard.statusmaster')),
                ('updated_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='psm_updated_by', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='ProjectMaster',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('project_name', models.CharField(max_length=255)),
                ('project_logo_id', models.IntegerField(blank=True, null=True)),
                ('created_date', models.DateTimeField(auto_now_add=True)),
                ('updated_date', models.DateTimeField(auto_now=True)),
                ('created_by', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='project_created_by', to=settings.AUTH_USER_MODEL)),
                ('status', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='project_status', to='dashboard.statusmaster')),
                ('updated_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='project_updated_by', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='productmaster',
            name='status',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='product_status', to='dashboard.statusmaster'),
        ),
        migrations.AddField(
            model_name='productmaster',
            name='updated_by',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='product_updated_by', to=settings.AUTH_USER_MODEL),
        ),
        migrations.CreateModel(
            name='MenuSdoMapping',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('created_date', models.DateTimeField(default=datetime.date(2024, 1, 23))),
                ('updated_date', models.DateTimeField(default=datetime.date(2024, 1, 23))),
                ('created_by', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='menusdo_created_by', to=settings.AUTH_USER_MODEL)),
                ('menu_card', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='dashboard.menucardmaster')),
                ('sdo', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='dashboard.sdomaster')),
                ('status', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='menusdo_status', to='dashboard.statusmaster')),
                ('updated_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='menusdo_updated_by', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='menucardmaster',
            name='status',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='menu_card_status', to='dashboard.statusmaster'),
        ),
        migrations.AddField(
            model_name='menucardmaster',
            name='updated_by',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='menu_card_updated_by', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='logomaster',
            name='status',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='logo_status', to='dashboard.statusmaster'),
        ),
        migrations.AddField(
            model_name='logomaster',
            name='updated_by',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='logo_updated_by', to=settings.AUTH_USER_MODEL),
        ),
        migrations.CreateModel(
            name='IndustryMaster',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('industry_type_name', models.CharField(max_length=255)),
                ('industry_description', models.TextField(blank=True, null=True)),
                ('created_date', models.DateTimeField(auto_now_add=True)),
                ('updated_date', models.DateTimeField(auto_now=True)),
                ('created_by', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='industry_created_by', to=settings.AUTH_USER_MODEL)),
                ('status', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='industry_status', to='dashboard.statusmaster')),
                ('updated_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='industry_updated_by', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='expertmaster',
            name='status',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='expert_status', to='dashboard.statusmaster'),
        ),
        migrations.AddField(
            model_name='expertmaster',
            name='updated_by',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='expert_updated_by', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='customermaster',
            name='status',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='customer_status', to='dashboard.statusmaster'),
        ),
        migrations.AddField(
            model_name='customermaster',
            name='updated_by',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='customer_updated_by', to=settings.AUTH_USER_MODEL),
        ),
        migrations.CreateModel(
            name='CustomerMapping',
            fields=[
                ('id', models.BigAutoField(primary_key=True, serialize=False)),
                ('opp_no', models.CharField(max_length=100, null=True)),
                ('description', models.TextField(blank=True, null=True)),
                ('created_date', models.DateTimeField(auto_now_add=True)),
                ('updated_date', models.DateTimeField(auto_now_add=True)),
                ('created_by', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='created_by_user', to=settings.AUTH_USER_MODEL)),
                ('csm', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='dashboard.csmmaster')),
                ('customer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='dashboard.customermaster')),
                ('industry', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='dashboard.industrymaster')),
                ('project', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='dashboard.projectmaster')),
                ('psm', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='dashboard.psmmaster')),
                ('region', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='dashboard.regionmaster')),
                ('sdm', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='dashboard.sdmmaster')),
                ('status', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='dashboard.statusmaster')),
                ('success_elements', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='dashboard.successelementsmaster')),
                ('success_service', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='dashboard.successservicemaster')),
                ('updated_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='updated_by_user', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='csmmaster',
            name='status',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='csm_status', to='dashboard.statusmaster'),
        ),
        migrations.AddField(
            model_name='csmmaster',
            name='updated_by',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='csm_updated_by', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='creatormaster',
            name='status',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='creator_status', to='dashboard.statusmaster'),
        ),
        migrations.AddField(
            model_name='creatormaster',
            name='updated_by',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='creator_updated_by', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='capabilitymaster',
            name='status',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='capabilty_status', to='dashboard.statusmaster'),
        ),
        migrations.AddField(
            model_name='capabilitymaster',
            name='updated_by',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='capability_updated_by', to=settings.AUTH_USER_MODEL),
        ),
    ]
