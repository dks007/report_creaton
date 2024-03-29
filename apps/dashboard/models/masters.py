from django.contrib.auth.models import User
from django.db import models

class BaseModel(models.Model):
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    created_date = models.DateTimeField(auto_now_add=True)
    updated_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='+')
    updated_date = models.DateTimeField(auto_now=True)
    status = models.ForeignKey('StatusMaster', on_delete=models.PROTECT, null=True, blank=True)

    class Meta:
        abstract = True

class StatusMaster(models.Model):
    status_name = models.CharField(max_length=25, unique=True)
    status_description = models.CharField(max_length=255, null=True, blank=True)

    def __str__(self):
        return self.status_name

class CustomerMaster(BaseModel):
    customer_id = models.CharField(max_length=100, unique=True)
    customer_name = models.CharField(max_length=100)

    def __str__(self):
        return self.customer_name

class RegionMaster(BaseModel):
    region_name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.region_name

class ProjectMaster(BaseModel):
    project_name = models.CharField(max_length=100, unique=True)
    projectid = models.CharField(max_length=25, null=True)
    project_logo_id = models.IntegerField(null=True, blank=True)

    def __str__(self):
        return f"{self.projectid} - {self.project_name}"

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

class CSMMaster(BaseModel):
    csm_name = models.CharField(max_length=100, unique=True)
    csm_email = models.CharField(max_length=255)

    def __str__(self):
        return self.csm_name

class SDMMaster(BaseModel):
    sdm_name = models.CharField(max_length=100, unique=True)
    sdm_email = models.CharField(max_length=255, blank=True)

    def __str__(self):
        return self.sdm_name

class PSMMaster(BaseModel):
    psm_name = models.CharField(max_length=50, unique=True)
    psm_email = models.CharField(max_length=255,blank=True)

    def __str__(self):
        return self.psm_name

class IndustryMaster(BaseModel):
    industry_type_name = models.CharField(max_length=100, unique=True)
    industry_description = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.industry_type_name

class SuccessElementsMaster(BaseModel):
    success_element_name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.success_element_name

class SuccessServiceMaster(BaseModel):
    success_service_name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.success_service_name

class MenuCardMaster(BaseModel):
    menu_card = models.CharField(max_length=10, unique=True)
    menu_description = models.TextField()
    template_file_name = models.CharField(max_length=255, null=True, blank=True)
    template_file_path = models.TextField(null=True, blank=True)
    template_file_type = models.CharField(max_length=10, null=True, blank=True)
    template_file_size = models.IntegerField(null=True, blank=True)

    def __str__(self):
        return f"MenuCardMaster {self.id} - {self.menu_card}"

class SdoMaster(BaseModel):
    sdo_name = models.CharField(max_length=100, unique=True)
    sdo_email = models.CharField(max_length=255, null=True, blank=True)

    def __str__(self):
        return f"SdoMaster - {self.sdo_name}"

class MenuSdoMapping(BaseModel):
    menu_card = models.ForeignKey(MenuCardMaster, on_delete=models.PROTECT)
    sdo = models.ForeignKey(SdoMaster, on_delete=models.CASCADE)

    def __str__(self):
        return f"MenuSdoMapping {self.id} - MenuCard: {self.menu_card.menu_card}, Sdo: {self.sdo.sdo_name}"

class ExpertMaster(BaseModel):
    expert_account_id = models.CharField(max_length=100)
    expert_name = models.CharField(max_length=100, unique=True)
    expert_email = models.CharField(max_length=255)

    def __str__(self):
        return f"ExpertMaster {self.id} - {self.expert_name}"

class CreatorMaster(BaseModel):
    creator_account_id = models.CharField(max_length=100)
    creator_name = models.CharField(max_length=100, unique=True)
    creator_email = models.CharField(max_length=255)

    def __str__(self):
        return f"CreatorMaster {self.id} - {self.creator_name}"

class LogoMaster(BaseModel):
    logo_file_name = models.CharField(max_length=50, unique=True)
    logo_file_type = models.CharField(max_length=10, null=True)
    logo_file_size = models.IntegerField()
    logo_url = models.CharField(max_length=255)
    logo = models.BinaryField(null=True)

    def __str__(self):
        return f"LogoMaster {self.id} - {self.logo_file_name}"

class ReportStatusMaster(BaseModel):
    report_status_name = models.CharField(max_length=25, unique=True)
    status_description = models.CharField(max_length=255, null=True, blank=True)

    def __str__(self):
        return f"ReportStatusMaster {self.id} - {self.report_status_name}"

class ProductMaster(BaseModel):
    product_name = models.CharField(max_length=100, unique=True)
    product_description = models.TextField(null=True, blank=True)

    def __str__(self):
        return f"ProductMaster {self.id} - {self.product_name}"

class CapabilityMaster(BaseModel):
    capability_name = models.CharField(max_length=100, unique=True)
    capability_description = models.TextField(null=True, blank=True)

    def __str__(self):
        return f"CapabilityMaster {self.id} - {self.capability_name}"

class SubCapabilityMaster(BaseModel):
    capability = models.ForeignKey(CapabilityMaster, on_delete=models.CASCADE)
    sub_capability_name = models.CharField(max_length=100, unique=True)
    sub_capability_description = models.TextField(null=True, blank=True)

    def __str__(self):
        return f"SubCapabilityMaster {self.id} - {self.sub_capability_name}"
