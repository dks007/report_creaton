# dashboard/models.py
import datetime
from django.contrib.auth.models import User
from django.db import models
 

class CustomerMapping(models.Model):
    id = models.BigAutoField(primary_key=True)
    customer_id = models.ForeignKey('CustomerMaster', on_delete=models.CASCADE)
    region_id = models.ForeignKey('RegionMaster', on_delete=models.CASCADE)
    project_id = models.ForeignKey('ProjectMaster', on_delete=models.CASCADE)
    opp_no = models.CharField(max_length=100, null=True)
    success_service_id = models.ForeignKey('SuccessServiceMaster', on_delete=models.SET_NULL, null=True)
    csm_id = models.ForeignKey('CSMMaster', on_delete=models.SET_NULL, null=True)
    psm_id = models.ForeignKey('PSMMaster', on_delete=models.SET_NULL, null=True)
    sdm_id = models.ForeignKey('SDMMaster', on_delete=models.SET_NULL, null=True)
    industry_id = models.ForeignKey('IndustryMaster', on_delete=models.SET_NULL, null=True)
    success_elements_id = models.ForeignKey('SuccessElementsMaster', on_delete=models.SET_NULL, null=True)
    description = models.TextField(null=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    created_date = models.DateTimeField(auto_now_add=True, null=False)
    updated_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='updated_by_user', null=True, blank=True)
    updated_date = models.DateTimeField(auto_now_add=True, null=False)
    status = models.CharField(max_length=255, null=True)

    def __str__(self):
        return f"CustomerMapping {self.id} - {self.customer_id.customer_name} - {self.project_id.project_name}"


class CSMMaster(models.Model):
    id = models.AutoField(primary_key=True)
    csm_name = models.CharField(max_length=255, null=False)
    csm_email = models.CharField(max_length=255, null=False)
    created_by = models.CharField(max_length=255, null=True)
    created_date = models.DateTimeField(auto_now_add=True, null=False)
    updated_by = models.CharField(max_length=255, null=False)
    updated_date = models.DateTimeField(auto_now=True, null=False)
    status = models.CharField(max_length=255, null=False)


class SDMMaster(models.Model):
    id = models.AutoField(primary_key=True)
    sdm_name = models.CharField(max_length=255, null=False)
    sdm_email = models.CharField(max_length=255, null=False)
    created_by = models.CharField(max_length=255, null=True)
    created_date = models.DateTimeField(auto_now_add=True, null=False)
    updated_by = models.CharField(max_length=255, null=False)
    updated_date = models.DateTimeField(auto_now=True, null=False)
    status = models.CharField(max_length=255, null=False)


class PSMMaster(models.Model):
    id = models.AutoField(primary_key=True)
    psm_name = models.CharField(max_length=255, null=False)
    psm_email = models.CharField(max_length=255, null=False)
    created_by = models.CharField(max_length=255, null=True)
    created_date = models.DateTimeField(auto_now_add=True, null=False)
    updated_by = models.CharField(max_length=255, null=False)
    updated_date = models.DateTimeField(auto_now=True, null=False)
    status = models.CharField(max_length=255, null=False)


class IndustryMaster(models.Model):
    id = models.AutoField(primary_key=True)
    industry_type_name = models.CharField(max_length=255, null=False)
    industry_description = models.TextField(null=False)
    created_by = models.CharField(max_length=255, null=True)
    created_date = models.DateTimeField(auto_now_add=True, null=False)
    updated_by = models.CharField(max_length=255, null=False)
    updated_date = models.DateTimeField(auto_now=True, null=False)
    status = models.CharField(max_length=255, null=False)


class RegionMaster(models.Model):
    id = models.AutoField(primary_key=True)
    region_name = models.CharField(max_length=255, null=False)
    created_by = models.CharField(max_length=255, null=False)
    created_date = models.DateTimeField(auto_now_add=True, null=False)
    updated_by = models.CharField(max_length=255, null=False)
    updated_date = models.DateTimeField(auto_now=True, null=False)
    status = models.CharField(max_length=255, null=False)


class CustomerMaster(models.Model):
    id = models.AutoField(primary_key=True)
    customer_id = models.CharField(max_length=255, null=False)
    customer_name = models.CharField(max_length=255, null=False)
    created_by = models.CharField(max_length=255, null=False)
    created_date = models.DateTimeField(auto_now_add=True, null=False)
    updated_by = models.CharField(max_length=255, null=False)
    updated_date = models.DateTimeField(auto_now=True, null=False)
    status = models.CharField(max_length=255, null=False)


class SuccessElementsMaster(models.Model):
    id = models.AutoField(primary_key=True)
    success_element_name = models.CharField(max_length=255, null=False)
    created_by = models.CharField(max_length=255, null=False)
    created_date = models.DateTimeField(auto_now_add=True, null=False)
    updated_by = models.CharField(max_length=255, null=False)
    updated_date = models.DateTimeField(auto_now=True, null=False)
    status = models.CharField(max_length=255, null=False)


class SuccessServiceMaster(models.Model):
    id = models.AutoField(primary_key=True)
    success_service_name = models.CharField(max_length=255, null=False)
    created_by = models.CharField(max_length=255, null=False)
    created_date = models.DateTimeField(auto_now_add=True, null=False)
    updated_by = models.CharField(max_length=255, null=False)
    updated_date = models.DateTimeField(auto_now=True, null=False)
    status = models.CharField(max_length=255, null=False)


class ProjectMaster(models.Model):
    id = models.AutoField(primary_key=True)
    project_name = models.CharField(max_length=255, null=False)
    project_logo_id = models.IntegerField(null=True, blank=True)
    created_by = models.CharField(max_length=255, null=False)
    created_date = models.DateTimeField(auto_now_add=True, null=False)
    updated_by = models.CharField(max_length=255, null=False)
    updated_date = models.DateTimeField(auto_now=True, null=False)
    status = models.CharField(max_length=255, null=False)


class MenuCardMaster(models.Model):
    id = models.AutoField(primary_key=True)
    menu_card = models.CharField(max_length=10, null=False)
    menu_description = models.TextField(null=False)
    template_file_name = models.CharField(max_length=255, null=True)
    template_file_path = models.TextField(null=True)
    template_file_type = models.CharField(max_length=10, null=True)
    template_file_size = models.IntegerField(null=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='menu_card_created_by', null=True, blank=True)
    created_date = models.DateTimeField(default=datetime.date.today(), blank=True)
    updated_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='menu_card_updated_by', null=True, blank=True)
    updated_date = models.DateTimeField(default=datetime.date.today(), blank=True)
    status = models.CharField(max_length=255, null=True, blank=True)

    def __str__(self):
        return f"MenuCardMaster {self.id} - {self.menu_card}"


class SdoMaster(models.Model):
    # id = models.AutoField(primary_key=True)
    sdo_name = models.CharField(max_length=255, null=False)
    sdo_email = models.CharField(max_length=255, null=True, blank=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sdo_created_by', null=True, blank=True)
    created_date = models.DateTimeField(default=datetime.date.today(), null=False)
    updated_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sdo_updated_by', null=True, blank=True)
    updated_date = models.DateTimeField(default=datetime.date.today(), null=False)
    status = models.CharField(max_length=255, null=True, blank=True)

    def __str__(self):
        return f"SdoMaster - {self.sdo_name}"


class MenuSdoMapping(models.Model):
    id = models.AutoField(primary_key=True)

    menu_card_id = models.ForeignKey(MenuCardMaster, on_delete=models.CASCADE)
    sdo_id = models.ForeignKey(SdoMaster, on_delete=models.CASCADE)
    status = models.CharField(max_length=255, null=True)

    def __str__(self):
        return f"MenuSdoMapping {self.id} - MenuCard: {self.menu_card_id.menu_card}, Sdo: {self.sdo_id.sdo_name}"


class ExpertMaster(models.Model):
    id = models.AutoField(primary_key=True)
    expert_account_id = models.CharField(max_length=255, null=False)
    expert_name = models.CharField(max_length=255, null=False)
    expert_email = models.CharField(max_length=255, null=False)
    created_by = models.CharField(max_length=255, null=False)
    created_date = models.DateTimeField(auto_now_add=True, null=True)
    updated_by = models.CharField(max_length=255, null=False)
    updated_date = models.DateTimeField(auto_now_add=True, null=False)
    status = models.CharField(max_length=255, null=False)

    def __str__(self):
        return f"ExpertMaster {self.id} - {self.expert_name}"


class CreatorMaster(models.Model):
    id = models.AutoField(primary_key=True)
    creator_account_id = models.CharField(max_length=255, null=False)
    creator_name = models.CharField(max_length=255, null=False)
    creator_email = models.CharField(max_length=255, null=False)
    created_by = models.CharField(max_length=255, null=False)
    created_date = models.DateTimeField(auto_now_add=True, null=True)
    updated_by = models.CharField(max_length=255, null=False)
    updated_date = models.DateTimeField(auto_now_add=True, null=False)
    status = models.CharField(max_length=255, null=False)

    def __str__(self):
        return f"CreatorMaster {self.id} - {self.creator_name}"


class LogoMaster(models.Model):
    id = models.AutoField(primary_key=True)
    logo_file_name = models.CharField(max_length=8, null=False)
    logo_file_type = models.CharField(max_length=10, null=True)
    logo_file_size = models.IntegerField(null=False)
    logo_url = models.CharField(max_length=255, null=False)
    logo = models.BinaryField(null=True)
    created_by = models.CharField(max_length=255, null=True)
    created_date = models.DateTimeField(auto_now_add=True, null=True)
    updated_by = models.CharField(max_length=255, null=False)
    updated_date = models.DateTimeField(auto_now_add=True, null=False)
    status = models.CharField(max_length=255, null=False)

    def __str__(self):
        return f"LogoMaster {self.id} - {self.logo_file_name}"


class StatusMaster(models.Model):
    id = models.AutoField(primary_key=True)
    status_name = models.CharField(max_length=255, null=False)
    created_by = models.CharField(max_length=255, null=True)
    created_date = models.DateTimeField(auto_now_add=True, null=False)
    updated_by = models.CharField(max_length=255, null=False)
    updated_date = models.DateTimeField(auto_now_add=True, null=False)
    status_description = models.CharField(max_length=255, null=False)

    def __str__(self):
        return f"StatusMaster {self.id} - {self.status_name}"


class ReportStatusMaster(models.Model):
    id = models.AutoField(primary_key=True)
    report_status_name = models.CharField(max_length=255, null=False)
    status_description = models.CharField(max_length=255, null=True)
    created_by = models.CharField(max_length=255, null=False)
    created_date = models.DateTimeField(auto_now_add=True, null=False)
    updated_by = models.CharField(max_length=255, null=False)
    updated_date = models.DateTimeField(auto_now_add=True, null=False)

    def __str__(self):
        return f"ReportStatusMaster {self.id} - {self.report_status_name}"


class SuccessReport(models.Model):
    id = models.AutoField(primary_key=True)
    jira_key = models.CharField(max_length=100, null=False)
    menu_card_id = models.ForeignKey(MenuCardMaster, on_delete=models.CASCADE)
    customer_id = models.ForeignKey(CustomerMaster, on_delete=models.CASCADE)
    expert_id = models.ForeignKey(ExpertMaster, on_delete=models.CASCADE)
    product = models.CharField(max_length=5, null=True)
    capability = models.CharField(max_length=5, null=True)
    sub_capability = models.CharField(max_length=5, null=True)
    logo_id = models.ForeignKey(LogoMaster, on_delete=models.CASCADE)
    status_id = models.ForeignKey(StatusMaster, on_delete=models.CASCADE)
    error_msg = models.CharField(max_length=255, null=True)
    download_link = models.TextField(null=True)
    creator_id = models.ForeignKey(CreatorMaster, on_delete=models.SET_NULL, null=True)
    approved_by_sdo = models.CharField(max_length=10, null=True)
    approved_sdo_date = models.DateField(null=True)
    approved_by_csm = models.CharField(max_length=10, null=True)
    approved_csm_date = models.DateField(null=True)
    approved_by_sdm = models.CharField(max_length=10, null=True)
    approved_sdm_date = models.DateField(null=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='success_report_created_by')
    created_date = models.DateTimeField(auto_now_add=True, null=True)
    updated_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='success_report_updated_by')
    updated_date = models.DateTimeField(auto_now_add=True, null=True)
    report_status_id = models.ForeignKey(ReportStatusMaster, on_delete=models.CASCADE)

    def __str__(self):
        return f"SuccessReport {self.id} - Jira Key: {self.jira_key}, Customer: {self.customer_id.customer_name}, Expert: {self.expert_id.expert_name}"


class ProductMaster(models.Model):
    id = models.AutoField(primary_key=True)
    product_name = models.CharField(max_length=255, null=False)
    created_by = models.CharField(max_length=255, null=False)
    created_date = models.DateTimeField(auto_now_add=True, null=False)
    updated_by = models.CharField(max_length=255, null=False)
    updated_date = models.DateTimeField(auto_now=True, null=False)
    status = models.CharField(max_length=255, null=False)


class CapabilityMaster(models.Model):
    id = models.AutoField(primary_key=True)
    capability_name = models.CharField(max_length=255, null=False)
    created_by = models.CharField(max_length=255, null=False)
    created_date = models.DateTimeField(auto_now_add=True, null=False)
    updated_by = models.CharField(max_length=255, null=False)
    updated_date = models.DateTimeField(auto_now=True, null=False)
    status = models.CharField(max_length=255, null=False)


class SubCapabilityMaster(models.Model):
    id = models.AutoField(primary_key=True)
    capability = models.ForeignKey(CapabilityMaster, on_delete=models.CASCADE)
    sub_capability_name = models.CharField(max_length=255, null=False)
    created_by = models.CharField(max_length=255, null=False)
    created_date = models.DateTimeField(auto_now_add=True, null=False)
    updated_by = models.CharField(max_length=255, null=False)
    updated_date = models.DateTimeField(auto_now=True, null=False)
    status = models.CharField(max_length=255, null=False)
