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
    customer = models.ForeignKey(CustomerMaster, on_delete=models.CASCADE)
    expert = models.ForeignKey(ExpertMaster, on_delete=models.CASCADE)
    product = models.ForeignKey(ProductMaster, on_delete=models.CASCADE)
    capability = models.ForeignKey(CapabilityMaster, on_delete=models.CASCADE)
    sub_capability = models.ForeignKey(SubCapabilityMaster, on_delete=models.CASCADE)
    logo = models.ForeignKey(LogoMaster, on_delete=models.CASCADE)
    status = models.ForeignKey(StatusMaster, on_delete=models.CASCADE)
    error_msg = models.CharField(max_length=255, null=True)
    download_link = models.TextField(null=True)
    creator = models.ForeignKey(CreatorMaster, on_delete=models.SET_NULL, null=True)
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
    report_status = models.ForeignKey(ReportStatusMaster, on_delete=models.CASCADE)

    def __str__(self):
        return f"SuccessReport {self.id} - Jira Key: {self.jira_key}, Customer: {self.customer.customer_name}, Expert: {self.expert.expert_name}"
