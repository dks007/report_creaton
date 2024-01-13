# dashboard/models.py
from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone  # Import the timezone module
# dashboard/models.py
from django.db import models
from django.utils import timezone  # Import the timezone module


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


