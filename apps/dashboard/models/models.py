# dashboard/models.py
from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone  # Import the timezone module
# dashboard/models.py
from django.db import models
from django.utils import timezone  # Import the timezone module


# class Issue(models.Model):
#     """
#     Model representing an issue.
#     """
#     issue_id = models.IntegerField(help_text="Unique identifier for the issue")
#     issue_key = models.CharField(max_length=255, help_text="Key representing the issue")
#     issue_summary = models.CharField(max_length=255, help_text="Summary of the issue")
#     issue_description = models.TextField(help_text="Detailed description of the issue")
#     activity_short_name = models.CharField(max_length=255, help_text="Short name of the activity")
#     menu_id = models.CharField(max_length=255, help_text="ID of the menu")
#     created = models.DateTimeField(help_text="Date and time when the issue was created")
#     changelog_assignee_created = models.DateTimeField(null=True, blank=True,
#                                                       help_text="Date and time of changelog for assignee creation")
#     creator_name = models.CharField(max_length=255, help_text="Name of the issue creator")
#     creator_email = models.EmailField(help_text="Email of the issue creator")
#     assignee_id = models.IntegerField(help_text="ID of the issue assignee")
#     assignee_email = models.EmailField(help_text="Email of the issue assignee")
#     assignee_name = models.CharField(max_length=255, help_text="Name of the issue assignee")
#     project_id = models.IntegerField(help_text="ID of the project related to the issue")
#     project_key = models.CharField(max_length=255, help_text="Key representing the project")
#     project_name = models.CharField(max_length=255, help_text="Name of the project")
#     parent_id = models.IntegerField(help_text="ID of the parent issue")
#     parent_key = models.CharField(max_length=255, help_text="Key representing the parent issue")
#     parent_summary = models.CharField(max_length=255, help_text="Summary of the parent issue")
#     subtask = models.BooleanField(help_text="Boolean indicating if the issue is a subtask")
#     partner = models.CharField(max_length=1, help_text="Indicator if the issue is a partner")
#     issue_status = models.CharField(max_length=255, help_text="Status of the issue")
#
#     def __str__(self):
#         return f"{self.issue_key} - {self.issue_summary}"


class CustomerProject(models.Model):
    """
    Model representing a customer project.
    """
    customer_name = models.CharField(max_length=255, help_text="Name of the customer")
    region = models.CharField(max_length=255, help_text="Region of the project")
    customer_id = models.IntegerField(help_text="Customer ID")
    project_id = models.CharField(max_length=255, help_text="Project ID")
    opp_no = models.CharField(max_length=255, help_text="Opportunity number")
    success_service = models.CharField(max_length=255, help_text="Type of success service")
    csm = models.CharField(max_length=255, help_text="Customer Success Manager",  null=True, blank=True)
    psm = models.CharField(max_length=255, help_text="Project Success Manager", null=True, blank=True)
    sdm = models.CharField(max_length=255, help_text="Service Delivery Manager",  null=True, blank=True)
    industry = models.CharField(max_length=255, help_text="Industry of the project",   null=True, blank=True)
    success_elements = models.CharField(max_length=255, help_text="Success elements of the project",   null=True, blank=True)
    description = models.TextField(help_text="Description of the project",   null=True, blank=True)
    date_created = models.DateField(default=timezone.now, help_text="Date when the project was created",   null=True, blank=True)

    def __str__(self):
        return f"{self.customer_name} - {self.project_id}"


class MenuSdo(models.Model):
    """
    Model representing a menu card.
    """
    menu_card = models.CharField(max_length=255, help_text="Name of the menu card")
    sdo = models.CharField(max_length=255, help_text="SDO associated with the menu card")
    email = models.EmailField(help_text="Email associated with the menu card")

    def __str__(self):
        return f"{self.menu_card} - {self.sdo}"


# class MenuCards(models.Model):
#     """
#     Model representing a menu template.
#     """
#     menu_card = models.CharField(max_length=255, help_text="Name of the menu card")
#     menu_description = models.TextField(help_text="Description of the menu")
#     menu_template = models.CharField(max_length=255, help_text="Type or name of the menu template")
#     template_path = models.CharField(max_length=255, help_text="Path to the menu template")
#     created_date = models.DateField(default=timezone.now, help_text="Date when the menu template was created")
#
#     def __str__(self):
#         return f"{self.menu_card} - {self.menu_template}"


# class Project(models.Model):
#     """
#     Model representing a project.
#     """
#     project_id = models.IntegerField(help_text="Unique identifier for the project")
#     project_key = models.CharField(max_length=255, help_text="Key representing the project")
#     project_summary = models.CharField(max_length=255, help_text="Summary of the project")
#     project_logo = models.CharField(max_length=255, help_text="Logo url of the project")
#     created = models.DateField(default=timezone.now, help_text="Date when the project was created")
#
#     def __str__(self):
#         return f"{self.project_key} - {self.project_summary}"


class DashboardModel(models.Model):
    jira_key = models.CharField(max_length=255)
    menu_card = models.CharField(max_length=255)
    project_id = models.IntegerField()
    issue_id = models.IntegerField()
    csm = models.CharField(max_length=255)
    sdo = models.CharField(max_length=255)
    sdm = models.CharField(max_length=255)
    approved_by_sdo = models.CharField(max_length=1)
    approved_sdo_date = models.DateField(null=True, blank=True)
    approved_by_csm = models.CharField(max_length=1)
    approved_csm_date = models.DateField(null=True, blank=True)
    approved_by_sdm = models.CharField(max_length=1)
    approved_sdm_date = models.DateField(null=True, blank=True)
    doc_link = models.CharField(max_length=255)
    creator = models.CharField(max_length=255)
    reporter = models.CharField(max_length=255)
    assignee_email = models.EmailField()
    status = models.BooleanField(default=False)
    created_date = models.DateField()
    updated_date = models.DateField()

    def __str__(self):
        return f"{self.jira_key} - {self.menu_card}"


