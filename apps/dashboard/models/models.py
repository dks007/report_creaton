# dashboard/models.py
from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone  # Import the timezone module
# dashboard/models.py
from django.db import models
from django.utils import timezone  # Import the timezone module

from apps.dashboard.models import MenuCardMaster, CustomerMaster, ExpertMaster, ProductMaster, CapabilityMaster, \
    SubCapabilityMaster, LogoMaster, StatusMaster, CreatorMaster, ReportStatusMaster


class SuccessReport(models.Model):
    id = models.AutoField(primary_key=True)
    parent_key = models.CharField(max_length=100, null=True, blank=True)
    jira_key = models.CharField(max_length=100, null=False)
    menu_card = models.ForeignKey(MenuCardMaster, on_delete=models.CASCADE)
    customer = models.ForeignKey(CustomerMaster, on_delete=models.CASCADE, null=True, blank=True)
    expert = models.ForeignKey(ExpertMaster, on_delete=models.CASCADE, null=True, blank=True)
    product = models.ForeignKey(ProductMaster, on_delete=models.CASCADE)
    capability = models.ForeignKey(CapabilityMaster, on_delete=models.CASCADE)
    sub_capability = models.ForeignKey(SubCapabilityMaster, on_delete=models.CASCADE, null=True, blank=True)
    logo = models.ForeignKey(LogoMaster, on_delete=models.CASCADE, null=True, blank=True)
    status = models.ForeignKey(StatusMaster, on_delete=models.CASCADE, null=True, blank=True)
    error_msg = models.CharField(max_length=255, null=True, blank=True)
    download_link = models.TextField(null=True, blank=True)
    creator = models.ForeignKey(CreatorMaster, on_delete=models.SET_NULL, null=True, blank=True)
    approved_by_sdo = models.CharField(max_length=10, null=True, blank=True)
    approved_sdo_date = models.DateField(null=True, blank=True)
    approved_by_csm = models.CharField(max_length=10, null=True, blank=True)
    approved_csm_date = models.DateField(null=True, blank=True)
    approved_by_sdm = models.CharField(max_length=10, null=True, blank=True)
    approved_sdm_date = models.DateField(null=True, blank=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='success_report_created_by', null=True, blank=True)
    created_date = models.DateTimeField(auto_now_add=True, null=True)
    updated_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='success_report_updated_by', null=True, blank=True)
    updated_date = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    report_status = models.ForeignKey(ReportStatusMaster, on_delete=models.CASCADE, null=True, blank=True)
    snow_case_no = models.CharField(max_length=10, null=True, blank=True)

    def __str__(self):
        return f"SuccessReport {self.id} - Jira Key: {self.jira_key}, Customer: {self.customer}, Expert: {self.expert}"
