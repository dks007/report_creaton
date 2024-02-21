"""

"""
import json

from django.contrib.auth.models import User
from django.core.serializers import serialize

from apps.dashboard.models import MenuCardMaster, CustomerMaster, ExpertMaster, ProductMaster, CapabilityMaster, \
    SubCapabilityMaster, StatusMaster, CreatorMaster, ReportStatusMaster, SuccessReport, ProjectMaster, LogoMaster


def success_report(data: dict, logo_id=None):
    menu_card = MenuCardMaster.objects.filter(menu_card=data.get('menu_card')).first()
    product = ProductMaster.objects.filter(product_name=data.get('product')).first()
    capability = CapabilityMaster.objects.filter(capability_name=data.get('capability')).first()
    expert = ExpertMaster.objects.filter(expert_name=data.get('expert_name')).first()
    customer = CustomerMaster.objects.filter(customer_name=data.get('customer_name')).first()
    creator = CreatorMaster.objects.filter(creator_name=data.get('creator_name')).first()
    user = User.objects.get(id=1)
    if expert is None:
        ExpertMaster.objects.create(
            expert_account_id='1',
            expert_email='expert@gmail.com',
            expert_name=data.get('expert_name'),
            created_by=user,
            updated_by=user
        )
    if data.get('action') == 'saved':
        report_status = ReportStatusMaster.objects.get(id=4)
    else:
        report_status = ReportStatusMaster.objects.get(id=1)
    if creator is None:
        creator = CreatorMaster.objects.create(
            creator_name=data.get('creator_name'),
            creator_email=data.get('creator_email'),
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
            "customer": customer
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


def all_master_list():
    menu_card = MenuCardMaster.objects.all().values('id', 'menu_card')
    product = ProductMaster.objects.all().values('id', 'product_name')
    capability = CapabilityMaster.objects.all().values('id', 'capability_name')
    creator = CreatorMaster.objects.all().values('id', 'creator_name')
    customer = CustomerMaster.objects.all().values('id', 'customer_id', 'customer_name')

    json_menu_card = json.dumps(list(menu_card))
    json_product = json.dumps(list(product))
    json_capability = json.dumps(list(capability))
    json_creator = json.dumps(list(creator))
    json_customer = json.dumps(list(customer))

    return json_menu_card, json_product, json_capability, json_creator, json_customer

# Saving logo data
def upload_logo_image(logo_file):
    # Create a new LogoMaster instance with the uploaded logo file
    logo = LogoMaster.objects.create(
        logo_file_name=logo_file.name,
        logo_file_type=logo_file.content_type,
        logo_file_size=logo_file.size,
        logo=logo_file.read()  # Assuming BinaryField is used to store the image data
    )
    return logo.id