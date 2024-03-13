# dashboard/models.py
from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone  # Import the timezone module
# dashboard/models.py
from django.db import models
from django.utils import timezone  # Import the timezone module

from apps.dashboard.models import MenuCardMaster, CustomerMaster, ExpertMaster, ProductMaster, CapabilityMaster, \
    SubCapabilityMaster, LogoMaster, StatusMaster, CreatorMaster, ReportStatusMaster, CustomerContactMaster, SdoMaster, CSMMaster, SDMMaster, ExCustomerContactsMaster, BaseModel, PSMMaster


class SuccessReport(models.Model):
    id = models.AutoField(primary_key=True)
    parent_key = models.CharField(max_length=100, null=True, blank=True)
    jira_key = models.CharField(max_length=100, null=False)
    menu_card = models.ForeignKey(MenuCardMaster, on_delete=models.CASCADE)
    customer = models.ForeignKey(CustomerMaster, on_delete=models.CASCADE, null=True, blank=True)
    customer_contact = models.ForeignKey(CustomerContactMaster, on_delete=models.CASCADE, null=True, blank=True,default=1)
    expert = models.ForeignKey(ExpertMaster, on_delete=models.CASCADE, null=True, blank=True,default=1)
    product = models.ForeignKey(ProductMaster, on_delete=models.CASCADE)
    capability = models.ForeignKey(CapabilityMaster, on_delete=models.CASCADE)
    sub_capability = models.ForeignKey(SubCapabilityMaster, on_delete=models.CASCADE, null=True, blank=True)
    logo = models.ForeignKey(LogoMaster, on_delete=models.CASCADE, null=True, blank=True)
    logo_url = models.TextField(null=True, blank=True)
    status = models.ForeignKey(StatusMaster, on_delete=models.CASCADE, default=1)
    error_msg = models.CharField(max_length=255, null=True, blank=True)
    download_link = models.TextField(null=True, blank=True)
    creator = models.ForeignKey(CreatorMaster, on_delete=models.SET_NULL, null=True, blank=True)
    sdm = models.ForeignKey(SDMMaster, on_delete=models.CASCADE, null=True, blank=True)
    csm = models.ForeignKey(CSMMaster, on_delete=models.CASCADE, null=True, blank=True)
    psm = models.ForeignKey(PSMMaster, on_delete=models.CASCADE, null=True, blank=True)
    sdo = models.ForeignKey(SdoMaster, on_delete=models.CASCADE, null=True, blank=True)
    approved_by_sdo = models.CharField(max_length=10, null=True, blank=True)
    approved_sdo_date = models.DateField(null=True, blank=True)
    approved_by_csm = models.CharField(max_length=10, null=True, blank=True)
    approved_csm_date = models.DateField(null=True, blank=True)
    approved_by_sdm = models.CharField(max_length=10, null=True, blank=True)
    approved_sdm_date = models.DateField(null=True, blank=True)
    created_by = models.ForeignKey(ExpertMaster, on_delete=models.CASCADE, related_name='success_report_created_by', null=True, blank=True,default=1)
    created_date = models.DateTimeField(auto_now_add=True, null=True)
    updated_by = models.ForeignKey(ExpertMaster, on_delete=models.CASCADE, related_name='success_report_updated_by', null=True, blank=True,default=1)
    updated_date = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    report_status = models.ForeignKey(ReportStatusMaster, on_delete=models.CASCADE, null=True, blank=True)
    snow_case_no = models.CharField(max_length=20, null=True, blank=True)

    def __str__(self):
        return f"SuccessReport {self.id} - Jira Key: {self.jira_key}, Customer: {self.customer}, Expert: {self.expert}"
    
# success report external customer mapping
class SuccessReportExCustMapping(BaseModel):
    report = models.ForeignKey(SuccessReport, on_delete=models.PROTECT)
    ex_customer = models.ForeignKey(ExCustomerContactsMaster, on_delete=models.CASCADE)

    def __str__(self):
        return f"SuccessReportExCustMapping {self.id} - MenuCard: {self.menu_card.menu_card}, Sdo: {self.sdo.sdo_name}"