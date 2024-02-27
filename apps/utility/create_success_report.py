"""

"""
import json

from django.contrib.auth.models import User
from django.core.serializers import serialize
from django.core.exceptions import ValidationError
from django.db import IntegrityError
from apps.dashboard.models import MenuCardMaster, CustomerMaster, ExpertMaster, ProductMaster, CapabilityMaster, \
    SubCapabilityMaster, CustomerContactMaster, StatusMaster, CreatorMaster, ReportStatusMaster, SuccessReport, \
    ProjectMaster, LogoMaster, SDMMaster, CSMMaster, SdoMaster
from apps.utility.create_upload_file import create_folder_and_upload_to_sharepoint


def success_report(data: dict, logo_id=None):
    menu_card = MenuCardMaster.objects.filter(menu_card=data.get('menu_card')).first()
    product = ProductMaster.objects.filter(product_name=data.get('product')).first()
    capability = CapabilityMaster.objects.filter(capability_name=data.get('capability')).first()
    expert = ExpertMaster.objects.filter(expert_name=data.get('expert_name')).first()
    customer = CustomerMaster.objects.filter(customer_name=data.get('customer_name')).first()
    customer_contact = CustomerContactMaster.objects.filter(customer_contact=data.get('customer_contact')).first()
    sdm = SDMMaster.objects.filter(sdm_name=data.get('sdm_name')).first()
    csm = CSMMaster.objects.filter(csm_name=data.get('csm_name')).first()
    sdo = SdoMaster.objects.filter(sdo_name=data.get('sdo_name')).first()
    # creator = CreatorMaster.objects.filter(creator_name=data.get('creator_name')).first()
    if data.get('action') == 'saved':
        report_status = ReportStatusMaster.objects.get(id=4)
    else:
        report_status = ReportStatusMaster.objects.get(id=1)
    if expert is None:
        expert = ExpertMaster.objects.create(
            expert_name=data.get('expert_name'),
            expert_email=data.get('expert_email'),
        )

    if customer_contact is None:
        customer_contact = CustomerContactMaster.objects.create(
            customer_contact=data.get('customer_contact'),
            customer_email=data.get('customer_email'),
            created_by=expert,
            updated_by=expert
        )
    # create report based on the action
    success_report_data = None
    if data.get('action') == 'saved':
        success_report_data = SuccessReport.objects.update_or_create(
            jira_key=data.get('issue_key'),
            defaults={
                'parent_key': data.get('parent_key'),
                'menu_card': menu_card,
                'product': product,
                'capability': capability,
                'snow_case_no': data.get('snow_case_no'),
                'report_status': report_status,
                "expert": expert,
                "customer": customer,
                "customer_contact": customer_contact,
                "logo_id": logo_id,
                'sdm': sdm,
                'sdo': sdo,
                'csm': csm
            }

        )

    elif data.get('action') == 'created':
        success_report_data = SuccessReport.objects.get(jira_key=data.get('issue_key'))
        if success_report_data is None:
            success_report_data = SuccessReport.objects.update_or_create(
                jira_key=data.get('issue_key'),
                defaults={
                    'parent_key': data.get('parent_key'),
                    'menu_card': menu_card,
                    'product': product,
                    'capability': capability,
                    'snow_case_no': data.get('snow_case_no'),
                    'report_status': report_status,
                    "expert": expert,
                    "customer": customer,
                    "customer_contact": customer_contact,
                    "logo_id": logo_id,
                    'sdm': sdm,
                    'sdo': sdo,
                    'csm': csm
                }

            )
        #calling to shcedular to create report
        #create_folder_and_upload_to_sharepoint(success_report_data)

    return success_report_data


def convert_json(response):
    response = {
        "issue_key": response.jira_key,
        "menu_card": response.menu_card.menu_card,
        "capability": response.capability.capability_name,
        "product": response.product.product_name,
        "snow_case_no": response.snow_case_no,
        "expert": response.expert.expert_name,
        "customer_contact": response.customer_contact.customer_contact,
        "report_status": response.report_status.report_status_name
    }

    return response


# Getting all require master data list
def all_master_list():
    menu_card = MenuCardMaster.objects.values('id', 'menu_card')
    product = ProductMaster.objects.values('id', 'product_name')
    customer_contact = CustomerContactMaster.objects.values('id', 'customer_contact')
    customer = CustomerMaster.objects.values('id', 'customer_name')
    cap_subcap = cap_subcap_array()

    list_menu_card = list(menu_card),
    list_product = list(product),
    list_customer_contact = list(customer_contact),
    list_customer = list(customer),
    list_cap_subcap = list(cap_subcap)

    return list_menu_card, list_product, list_cap_subcap, list_customer_contact, list_customer


# Saving logo data
def upload_logo_image(logo_file):
    try:
        # Create a new LogoMaster instance with the uploaded logo file
        logo = LogoMaster.objects.create(
            logo_file_name=logo_file.name,
            logo_file_type=logo_file.content_type,
            logo_file_size=logo_file.size,
            logo_image=logo_file  # Assuming logo_image is an ImageField
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


def cap_subcap_array():
    cap_subcap = []
    capabilities = CapabilityMaster.objects.all()

    for capability in capabilities:
        cap_obj = {
            'id': capability.id,
            'name': capability.capability_name,
            'sub_capabilities': []
        }

        sub_capabilities = SubCapabilityMaster.objects.filter(capability=capability)
        for sub_capability in sub_capabilities:
            sub_cap_obj = {
                'id': sub_capability.id,
                'name': sub_capability.sub_capability_name
            }
            cap_obj['sub_capabilities'].append(sub_cap_obj)

        cap_subcap.append(cap_obj)

    return cap_subcap
