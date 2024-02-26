from django.contrib.auth.models import User
from django.db import models


# Base Model appl for all masters
class BaseModel(models.Model):
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    created_date = models.DateTimeField(auto_now_add=True)
    updated_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='+')
    updated_date = models.DateTimeField(auto_now=True)
    status = models.ForeignKey('StatusMaster', on_delete=models.PROTECT, null=True, blank=True)

    class Meta:
        abstract = True


# Expert master
class ExpertMaster(models.Model):
    expert_account_id = models.CharField(max_length=100, null=True, blank=True)
    expert_name = models.CharField(max_length=100, unique=True)
    expert_email = models.CharField(max_length=255, null=True, blank=True)

    def __str__(self):
        return f"ExpertMaster {self.id} - {self.expert_name}"


# Status Master
class StatusMaster(models.Model):
    status_name = models.CharField(max_length=25, unique=True)
    status_description = models.CharField(max_length=255, null=True, blank=True)

    def __str__(self):
        return self.status_name


# customer Master
class CustomerMaster(models.Model):
    customer_id = models.CharField(max_length=100, unique=True)
    customer_name = models.CharField(max_length=100)
    created_by = models.ForeignKey(ExpertMaster, on_delete=models.CASCADE,related_name='customer_created',default=1)
    updated_by = models.ForeignKey(ExpertMaster, on_delete=models.CASCADE, related_name='customer_updated',default=1)

    def __str__(self):
        return self.customer_name


# Customer COntact master
class CustomerContactMaster(models.Model):
    customer_contact = models.CharField(max_length=100, unique=True)
    customer_email = models.CharField(max_length=255, null=True)
    created_by = models.ForeignKey(ExpertMaster, on_delete=models.CASCADE, related_name='customer_created_contacts',default=1)
    updated_by = models.ForeignKey(ExpertMaster, on_delete=models.CASCADE,related_name='customer_updated_contacts',default=1)

    def __str__(self):
        return f"CustomerContact {self.id} - {self.customer_contact}"


# Region Master
class RegionMaster(BaseModel):
    region_name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.region_name


# Project Master
class ProjectMaster(BaseModel):
    project_name = models.CharField(max_length=100, unique=True)
    projectid = models.CharField(max_length=25, null=True)
    project_logo_id = models.IntegerField(null=True, blank=True)

    def __str__(self):
        return f"{self.project_name}"


# Customer mapping
class CustomerMapping(BaseModel):
    customer = models.ForeignKey(CustomerMaster, on_delete=models.CASCADE)
    region = models.ForeignKey(RegionMaster, on_delete=models.CASCADE, null=True, blank=True)
    project = models.ForeignKey(ProjectMaster, on_delete=models.CASCADE, null=True, blank=True)
    opp_no = models.CharField(max_length=25, null=True)
    success_service = models.ForeignKey('SuccessServiceMaster', on_delete=models.SET_NULL, null=True)
    csm = models.ForeignKey('CSMMaster', on_delete=models.SET_NULL, null=True)
    psm = models.ForeignKey('PSMMaster', on_delete=models.SET_NULL, null=True)
    sdm = models.ForeignKey('SDMMaster', on_delete=models.SET_NULL, null=True)
    industry = models.ForeignKey('IndustryMaster', on_delete=models.SET_NULL, null=True)
    success_elements = models.ForeignKey('SuccessElementsMaster', on_delete=models.SET_NULL, null=True)
    description = models.TextField(null=True, blank=True)

    def __str__(self):
        return f"CustomerMapping {self.id} - {self.customer.customer_name}"


# CSM master
class CSMMaster(BaseModel):
    csm_name = models.CharField(max_length=100, unique=True)
    csm_email = models.CharField(max_length=255)

    def __str__(self):
        return self.csm_name


# SDM master
class SDMMaster(BaseModel):
    sdm_name = models.CharField(max_length=100, unique=True)
    sdm_email = models.CharField(max_length=255, blank=True)

    def __str__(self):
        return self.sdm_name


# PSM master
class PSMMaster(BaseModel):
    psm_name = models.CharField(max_length=50, unique=True)
    psm_email = models.CharField(max_length=255, blank=True)

    def __str__(self):
        return self.psm_name


# Industry master
class IndustryMaster(BaseModel):
    industry_type_name = models.CharField(max_length=100, unique=True)
    industry_description = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.industry_type_name


# Success Element Master
class SuccessElementsMaster(BaseModel):
    success_element_name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.success_element_name


# Success Service Master
class SuccessServiceMaster(BaseModel):
    success_service_name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.success_service_name


# menu card master
class MenuCardMaster(BaseModel):
    menu_card = models.CharField(max_length=10, unique=True)
    menu_description = models.TextField()
    template_file_name = models.CharField(max_length=255, null=True, blank=True)
    template_file_path = models.TextField(null=True, blank=True)
    template_file_type = models.CharField(max_length=10, null=True, blank=True)
    template_file_size = models.IntegerField(null=True, blank=True)

    def __str__(self):
        return f"MenuCardMaster {self.id} - {self.menu_card}"


# Sdo master
class SdoMaster(BaseModel):
    sdo_name = models.CharField(max_length=100, unique=True)
    sdo_email = models.CharField(max_length=255, null=True, blank=True)

    def __str__(self):
        return f"SdoMaster - {self.sdo_name}"


# Menu Sdo Mapping
class MenuSdoMapping(BaseModel):
    menu_card = models.ForeignKey(MenuCardMaster, on_delete=models.PROTECT)
    sdo = models.ForeignKey(SdoMaster, on_delete=models.CASCADE)

    def __str__(self):
        return f"MenuSdoMapping {self.id} - MenuCard: {self.menu_card.menu_card}, Sdo: {self.sdo.sdo_name}"


# Creator master
class CreatorMaster(BaseModel):
    creator_account_id = models.CharField(max_length=100)
    creator_name = models.CharField(max_length=100, unique=True)
    creator_email = models.CharField(max_length=255, null=True)

    def __str__(self):
        return f"CreatorMaster {self.id} - {self.creator_name}"


# Logo Master
class LogoMaster(BaseModel):
    logo_file_name = models.CharField(max_length=50, unique=True)
    logo_file_type = models.CharField(max_length=10, null=True)
    logo_file_size = models.IntegerField()
    logo_url = models.CharField(max_length=255)
    logo = models.BinaryField(null=True)

    def __str__(self):
        return f"LogoMaster {self.id} - {self.logo_file_name}"


# Report Status Master
class ReportStatusMaster(BaseModel):
    report_status_name = models.CharField(max_length=25, unique=True)
    status_description = models.CharField(max_length=255, null=True, blank=True)

    def __str__(self):
        return f"ReportStatusMaster {self.id} - {self.report_status_name}"


# Product Master
class ProductMaster(BaseModel):
    product_name = models.CharField(max_length=100, unique=True)
    product_description = models.TextField(null=True, blank=True)

    def __str__(self):
        return f"ProductMaster {self.id} - {self.product_name}"


# Capability Master
class CapabilityMaster(BaseModel):
    capability_name = models.CharField(max_length=100, unique=True)
    capability_description = models.TextField(null=True, blank=True)

    def __str__(self):
        return f"CapabilityMaster {self.id} - {self.capability_name}"


# Sub Capability Master
class SubCapabilityMaster(BaseModel):
    capability = models.ForeignKey(CapabilityMaster, on_delete=models.CASCADE)
    sub_capability_name = models.CharField(max_length=100, unique=True)
    sub_capability_description = models.TextField(null=True, blank=True)

    def __str__(self):
        return f"SubCapabilityMaster {self.id} - {self.sub_capability_name}"


# external customer contact
class ExCustomerContactsMaster(models.Model):
    customer = models.ForeignKey(CustomerMaster, on_delete=models.CASCADE, null=True, blank=True)
    ex_customer_name = models.CharField(max_length=100)
    ex_customer_email = models.TextField(null=True, blank=True)
    ex_customer_id = models.CharField(max_length=100, unique=True)
    description = models.TextField(null=True, blank=True)
    created_by = models.ForeignKey(ExpertMaster, on_delete=models.CASCADE,related_name='excustomer_created',default=1)
    updated_by = models.ForeignKey(ExpertMaster, on_delete=models.CASCADE, related_name='excustomer_updated',default=1)

    def __str__(self):
        return f"ExCustomerContactsMas {self.id} - {self.sub_capability_name}"
