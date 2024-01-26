# dashboard/models.py
import datetime
from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone

class StatusMaster(models.Model):
    id = models.AutoField(primary_key=True)
    status_name = models.CharField(max_length=255, null=False)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='status_created_by')
    created_date = models.DateTimeField(auto_now_add=True, null=False)
    updated_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='status_updated_by',  null=True, blank=True)
    updated_date = models.DateTimeField(auto_now_add=True, null=False)
    status_description = models.CharField(max_length=255, null=True, blank=True)

    def __str__(self):
        return f"StatusMaster {self.id} - {self.status_name}"


# customer mapping table
class CustomerMapping(models.Model):
    id = models.BigAutoField(primary_key=True)
    customer = models.ForeignKey('CustomerMaster', on_delete=models.CASCADE)
    region = models.ForeignKey('RegionMaster', on_delete=models.CASCADE,null=True,
                                   blank=True)
    project = models.ForeignKey('ProjectMaster', on_delete=models.CASCADE,null=True,
                                   blank=True)
    opp_no = models.CharField(max_length=100, null=True)
    success_service = models.ForeignKey('SuccessServiceMaster', on_delete=models.SET_NULL, null=True)
    csm = models.ForeignKey('CSMMaster', on_delete=models.SET_NULL, null=True)
    psm = models.ForeignKey('PSMMaster', on_delete=models.SET_NULL, null=True)
    sdm = models.ForeignKey('SDMMaster', on_delete=models.SET_NULL, null=True)
    industry = models.ForeignKey('IndustryMaster', on_delete=models.SET_NULL, null=True)
    success_elements = models.ForeignKey('SuccessElementsMaster', on_delete=models.SET_NULL, null=True)
    description = models.TextField(null=True, blank=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='created_by_user')
    created_date = models.DateTimeField(auto_now_add=True, null=False)
    updated_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='updated_by_user', null=True,
                                   blank=True)
    updated_date = models.DateTimeField(auto_now_add=True, null=False)
    status = models.ForeignKey(StatusMaster, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return f"CustomerMapping {self.id} - {self.customer.customer_name} - {self.project.project_name}"


# csm master
class CSMMaster(models.Model):
    id = models.AutoField(primary_key=True)
    csm_name = models.CharField(max_length=255, null=False)
    csm_email = models.CharField(max_length=255, null=False)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='csm_created_by')
    created_date = models.DateTimeField(auto_now_add=True, null=False)
    updated_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='csm_updated_by', null=True, blank=True)
    updated_date = models.DateTimeField(auto_now=True, null=False)
    status = models.ForeignKey(StatusMaster, on_delete=models.CASCADE, related_name='csm_status', null=True, blank=True)

    def __str__(self):
        return f"{self.id} - {self.csm_name}"


# sdm master
class SDMMaster(models.Model):
    id = models.AutoField(primary_key=True)
    sdm_name = models.CharField(max_length=255, null=False)
    sdm_email = models.CharField(max_length=255, null=False)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sdm_created_by')
    created_date = models.DateTimeField(auto_now_add=True, null=False)
    updated_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sdm_updated_by', null=True, blank=True)
    updated_date = models.DateTimeField(auto_now=True, null=False)
    status = models.ForeignKey(StatusMaster, on_delete=models.CASCADE, related_name='sdm_status', null=True, blank=True)

    def __str__(self):
        return f"{self.id} - {self.sdm_name}"


# psm master
class PSMMaster(models.Model):
    id = models.AutoField(primary_key=True)
    psm_name = models.CharField(max_length=255, null=False)
    psm_email = models.CharField(max_length=255, null=False)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='psm_created_by')
    created_date = models.DateTimeField(auto_now_add=True, null=False)
    updated_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='psm_updated_by', null=True, blank=True)
    updated_date = models.DateTimeField(auto_now=True, null=False)
    status = models.ForeignKey(StatusMaster, on_delete=models.CASCADE, related_name='psm_status', null=True, blank=True)

    def __str__(self):
        return f"{self.id} - {self.psm_name}"


# industry master
class IndustryMaster(models.Model):
    id = models.AutoField(primary_key=True)
    industry_type_name = models.CharField(max_length=255, null=False)
    industry_description = models.TextField(null=True, blank=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='industry_created_by')
    created_date = models.DateTimeField(auto_now_add=True, null=False)
    updated_by = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True, related_name='industry_updated_by')
    updated_date = models.DateTimeField(auto_now=True, null=False)
    status = models.ForeignKey(StatusMaster, on_delete=models.CASCADE, null=True, blank=True, related_name='industry_status')

    def __str__(self):
        return f"{self.id} - {self.industry_type_name}"


# Region master
class RegionMaster(models.Model):
    id = models.AutoField(primary_key=True)
    region_name = models.CharField(max_length=255, null=False)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='region_created_by')
    created_date = models.DateTimeField(auto_now_add=True, null=False)
    updated_by = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True, related_name='region_updated_by')
    updated_date = models.DateTimeField(auto_now=True, null=False)
    status = models.ForeignKey(StatusMaster, on_delete=models.CASCADE, null=True, blank=True, related_name='region_status')

    def __str__(self):
        return f"{self.id} - {self.region_name}"


# customer master
class CustomerMaster(models.Model):
    id = models.AutoField(primary_key=True)
    customer_id = models.CharField(max_length=255, null=False)
    customer_name = models.CharField(max_length=255, null=False)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='customer_created_by')
    created_date = models.DateTimeField(auto_now_add=True, null=False)
    updated_by = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True, related_name='customer_updated_by')
    updated_date = models.DateTimeField(auto_now=True, null=False)
    status = models.ForeignKey(StatusMaster, on_delete=models.CASCADE, null=True, blank=True, related_name='customer_status')

    def __str__(self):
        return f"{self.id} - {self.customer_name}"


# success element master
class SuccessElementsMaster(models.Model):
    id = models.AutoField(primary_key=True)
    success_element_name = models.CharField(max_length=255, null=False)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='success_element_created_by')
    created_date = models.DateTimeField(auto_now_add=True, null=False)
    updated_by = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True, related_name='success_element_updated_by')
    updated_date = models.DateTimeField(auto_now=True, null=False)
    status = models.ForeignKey(StatusMaster, on_delete=models.CASCADE, null=True, blank=True, related_name='success_element_status')

    def __str__(self):
        return f"{self.id} - {self.success_element_name}"


# success service master
class SuccessServiceMaster(models.Model):
    id = models.AutoField(primary_key=True)
    success_service_name = models.CharField(max_length=255, null=False)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='success_service_created_by')
    created_date = models.DateTimeField(auto_now_add=True, null=False)
    updated_by = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True, related_name='success_service_updated_by')
    updated_date = models.DateTimeField(auto_now=True, null=False)
    status = models.ForeignKey(StatusMaster, on_delete=models.CASCADE, null=True, blank=True, related_name='success_service_status')

    def __str__(self):
        return f"{self.id} - {self.success_service_name}"


# project master
class ProjectMaster(models.Model):
    id = models.AutoField(primary_key=True)
    project_name = models.CharField(max_length=255, null=False)
    project_logo_id = models.IntegerField(null=True, blank=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='project_created_by')
    created_date = models.DateTimeField(auto_now_add=True, null=False)
    updated_by = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True, related_name='project_updated_by')
    updated_date = models.DateTimeField(auto_now=True, null=False)
    status = models.ForeignKey(StatusMaster, on_delete=models.CASCADE, null=True, blank=True, related_name='project_status')

    def __str__(self):
        return f"{self.id} - {self.project_name}"


# menu card master
class MenuCardMaster(models.Model):
    id = models.AutoField(primary_key=True)
    menu_card = models.CharField(max_length=10, null=False)
    menu_description = models.TextField()
    template_file_name = models.CharField(max_length=255, null=True)
    template_file_path = models.TextField(null=True)
    template_file_type = models.CharField(max_length=10, null=True)
    template_file_size = models.IntegerField(null=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='menu_card_created_by', null=True,
                                   blank=True)
    created_date = models.DateTimeField(auto_now_add=True, null=False, blank=True)
    updated_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='menu_card_updated_by', null=True,
                                   blank=True)
    updated_date = models.DateTimeField(auto_now_add=True, null=False, blank=True)
    status = models.ForeignKey(StatusMaster, on_delete=models.CASCADE, null=True, blank=True, related_name='menu_card_status')

    def __str__(self):
        return f"MenuCardMaster {self.id} - {self.menu_card}"


# sdo master
class SdoMaster(models.Model):
    sdo_name = models.CharField(max_length=255, null=False)
    sdo_email = models.CharField(max_length=255, null=True, blank=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sdo_created_by')
    created_date = models.DateTimeField(auto_now_add=True, null=False)
    updated_by = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True, related_name='sdo_updated_by')
    updated_date = models.DateTimeField(auto_now_add=True, null=False)
    status = models.ForeignKey(StatusMaster, on_delete=models.CASCADE, null=True, blank=True, related_name='sdo_status')

    def __str__(self):
        return f"SdoMaster - {self.sdo_name}"


# menu sdo mapping
class MenuSdoMapping(models.Model):
    id = models.AutoField(primary_key=True)

    menu_card = models.ForeignKey(MenuCardMaster, on_delete=models.CASCADE)
    sdo = models.ForeignKey(SdoMaster, on_delete=models.CASCADE)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='menusdo_created_by')
    created_date = models.DateTimeField(auto_now_add=True, null=False)
    updated_by = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True, related_name='menusdo_updated_by')
    updated_date = models.DateTimeField(auto_now_add=True, null=False)
    status = models.ForeignKey(StatusMaster, on_delete=models.CASCADE, null=True, blank=True, related_name='menusdo_status')

    def __str__(self):
        return f"MenuSdoMapping {self.id} - MenuCard: {self.menu_card.menu_card}, Sdo: {self.sdo.sdo_name}"


# expert master
class ExpertMaster(models.Model):
    id = models.AutoField(primary_key=True)
    expert_account_id = models.CharField(max_length=255, null=False)
    expert_name = models.CharField(max_length=255, null=False)
    expert_email = models.CharField(max_length=255, null=False)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='expert_created_by')
    created_date = models.DateTimeField(auto_now_add=True, null=True)
    updated_by = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True, related_name='expert_updated_by')
    updated_date = models.DateTimeField(auto_now_add=True, null=False)
    status = models.ForeignKey(StatusMaster, on_delete=models.CASCADE, null=True, blank=True, related_name='expert_status')

    def __str__(self):
        return f"ExpertMaster {self.id} - {self.expert_name}"


# creator master
class CreatorMaster(models.Model):
    id = models.AutoField(primary_key=True)
    creator_account_id = models.CharField(max_length=255, null=False)
    creator_name = models.CharField(max_length=255, null=False)
    creator_email = models.CharField(max_length=255, null=False)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='creator_created_by')
    created_date = models.DateTimeField(auto_now_add=True, null=True)
    updated_by = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True, related_name='creator_updated_by')
    updated_date = models.DateTimeField(auto_now_add=True, null=False)
    status = models.ForeignKey(StatusMaster, on_delete=models.CASCADE, null=True, blank=True, related_name='creator_status')

    def __str__(self):
        return f"CreatorMaster {self.id} - {self.creator_name}"


# Logo master
class LogoMaster(models.Model):
    id = models.AutoField(primary_key=True)
    logo_file_name = models.CharField(max_length=8, null=False)
    logo_file_type = models.CharField(max_length=10, null=True)
    logo_file_size = models.IntegerField(null=False)
    logo_url = models.CharField(max_length=255, null=False)
    logo = models.BinaryField(null=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='logo_created_by')
    created_date = models.DateTimeField(auto_now_add=True, null=True)
    updated_by = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True, related_name='logo_updated_by')
    updated_date = models.DateTimeField(auto_now_add=True, null=False)
    status = models.ForeignKey(StatusMaster, on_delete=models.CASCADE, null=True, blank=True, related_name='logo_status')

    def __str__(self):
        return f"LogoMaster {self.id} - {self.logo_file_name}"


# Report status master
class ReportStatusMaster(models.Model):
    id = models.AutoField(primary_key=True)
    report_status_name = models.CharField(max_length=255, null=False)
    status_description = models.CharField(max_length=255, null=True, blank=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='report_status_created_by')
    created_date = models.DateTimeField(auto_now_add=True, null=False)
    updated_by = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True, related_name='report_status_updated_by')
    updated_date = models.DateTimeField(auto_now_add=True, null=False)
    status = models.ForeignKey(StatusMaster, on_delete=models.CASCADE, null=True, blank=True, related_name='report_status_status')

    def __str__(self):
        return f"ReportStatusMaster {self.id} - {self.report_status_name}"


# Product master
class ProductMaster(models.Model):
    id = models.AutoField(primary_key=True)
    product_name = models.CharField(max_length=255, null=False)
    product_description = models.TextField(null=True, blank=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='product_created_by')
    created_date = models.DateTimeField(auto_now_add=True, null=False)
    updated_by = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True, related_name='product_updated_by')
    updated_date = models.DateTimeField(auto_now=True, null=False)
    status = models.ForeignKey(StatusMaster, on_delete=models.CASCADE, null=True, blank=True, related_name='product_status')

    def __str__(self):
        return f"{self.id} - {self.product_name}"


# capability master
class CapabilityMaster(models.Model):
    id = models.AutoField(primary_key=True)
    capability_name = models.CharField(max_length=255, null=False)
    capability_description = models.TextField(null=True, blank=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='capability_created_by')
    created_date = models.DateTimeField(auto_now_add=True, null=False)
    updated_by = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True, related_name='capability_updated_by')
    updated_date = models.DateTimeField(auto_now=True, null=False)
    status = models.ForeignKey(StatusMaster, on_delete=models.CASCADE, null=True, blank=True, related_name='capabilty_status')

    def __str__(self):
        return f"{self.id} - {self.capability_name}"


# sub capability master
class SubCapabilityMaster(models.Model):
    id = models.AutoField(primary_key=True)
    capability = models.ForeignKey(CapabilityMaster, on_delete=models.CASCADE)
    sub_capability_name = models.CharField(max_length=255, null=False)
    sub_capability_description = models.TextField(null=True, blank=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sub_capability_created_by')
    created_date = models.DateTimeField(auto_now_add=True, null=False)
    updated_by = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True,related_name='sub_capability_updated_by')
    updated_date = models.DateTimeField(auto_now=True, null=False)
    status = models.ForeignKey(StatusMaster, on_delete=models.CASCADE, null=True, blank=True, related_name='sub_capability_status')

    def __str__(self):
        return f"{self.id} - {self.sub_capability_name}"
