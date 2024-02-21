"""

"""
import json

from django.contrib.auth.models import User
from django.core.serializers import serialize
from django.core.exceptions import ValidationError
from django.db import IntegrityError
from apps.dashboard.models import MenuCardMaster, CustomerMaster, ExpertMaster, ProductMaster, CapabilityMaster, \
    SubCapabilityMaster, StatusMaster, CreatorMaster, ReportStatusMaster, SuccessReport, ProjectMaster, LogoMaster


def success_report(data: dict, logo_id=None):
    menu_card = MenuCardMaster.objects.filter(menu_card=data.get('menu_card')).first()
    product = ProductMaster.objects.filter(product_name=data.get('product')).first()
    capability = CapabilityMaster.objects.filter(capability_name=data.get('capability')).first()
    expert = ExpertMaster.objects.filter(expert_name=data.get('expert_name')).first()
    customer = CustomerMaster.objects.filter(customer_name=data.get('customer_name')).first()
    creator = CreatorMaster.objects.filter(creator_name=data.get('creator_name')).first()
    if data.get('action') == 'saved':
        report_status = ReportStatusMaster.objects.get(id=4)
    else:
        report_status = ReportStatusMaster.objects.get(id=1)
    user = User.objects.get(id=1)
    if creator is None:
        creator = CreatorMaster.objects.create(
            creator_name=data.get('creator_name'),
            creator_email=data.get('creator_email'),
            created_by=user,
            updated_by=user
        )
    if expert is None:
        expert = ExpertMaster.objects.create(
            expert_name=data.get('expert_name'),
            expert_email=data.get('expert_email'),
            created_by=user,
            updated_by=user
        )
    if customer is None:
        customer = CustomerMaster.objects.create(
            customer_name=data.get('customer_name'),
            customer_email=data.get('customer_email'),
            created_by=user,
            updated_by=user
        )

    success_report_data = SuccessReport.objects.update_or_create(
        jira_key=data.get('issue_key'),
        defaults={
            'parent_key': data.get('parent_key'),
            'menu_card': menu_card,
            'product': product,
            'capability': capability,
            'creator': creator,
            'snow_case_no': data.get('snow_case_no'),
            'report_status': report_status,
            "expert": expert,
            "customer": customer,
            "logo_id": logo_id
        }

    )

    return success_report_data


def convert_json(response):
    response = {
        "issue_key": response.jira_key,
        "menu_card": response.menu_card.menu_card,
        "capability": response.capability.capability_name,
        "product": response.product.product_name,
        "snow_case_no": response.snow_case_no,
        "creator_email": response.creator.creator_email,
        "assignee_name": "Andreas Andersson",
        "creator_name": response.creator.creator_name,
        "report_status": response.report_status.report_status_name
    }

    return response

# Getting all require master data list
def all_master_list():
    menu_card = MenuCardMaster.objects.all()
    product = ProductMaster.objects.all()
    capability = CapabilityMaster.objects.all()
    creator = CreatorMaster.objects.all()
    customer = CustomerMaster.objects.all()

    json_menu_card = json.loads(serialize('json', menu_card))
    json_product = json.loads(serialize('json', product))
    json_capability = json.loads(serialize('json', capability))
    json_creator = json.loads(serialize('json', creator))
    json_customer = json.loads(serialize('json', customer))

    return json_menu_card, json_product, json_capability, json_creator, json_customer

# Saving logo data
# Saving logo data
def upload_logo_image(logo_file):
    try:
        # Create a new LogoMaster instance with the uploaded logo file
        logo = LogoMaster.objects.create(
            logo_file_name=logo_file.name,
            logo_file_type=logo_file.content_type,
            logo_file_size=logo_file.size,
            logo=logo_file.read()  # Assuming BinaryField is used to store the image data
        )
        return logo.id, None
    except ValidationError as e:
        # Handle validation errors
        error_message = "Validation Error: {}".format(e)
        return None, error_message
    except IntegrityError as e:
        # Handle duplicate entry error
        error_message = "Duplicate entry error: {}".format(e)
        return None, error_message
    except Exception as e:
        # Handle other unexpected errors
        error_message = "An unexpected error occurred: {}".format(e)
        return None, error_message