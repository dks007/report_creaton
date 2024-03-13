"""

"""
import json, re, os

from django.contrib.auth.models import User
from django.core.serializers import serialize
from django.core.exceptions import ValidationError
from django.core.files.storage import FileSystemStorage
from django.db import IntegrityError
from apps.dashboard.models import MenuCardMaster, CustomerMaster, ExpertMaster, ProductMaster, CapabilityMaster, \
    SubCapabilityMaster, CustomerContactMaster, StatusMaster, CreatorMaster, ReportStatusMaster, SuccessReport, \
    ProjectMaster, LogoMaster, SDMMaster, CSMMaster, SdoMaster
from apps.utility.create_upload_file import create_folder_and_upload_to_sharepoint

from apps.utility.utils import update_report_status

from django.db import transaction

def success_report(data: dict):

    # Fetch the existing SuccessReport instance, if it exists
    success_report_instance = SuccessReport.objects.filter(jira_key=data.get('issue_key')).first()


    # If the report exists and its status is 2 or 3, return a message indicating that the report is in progress
    if success_report_instance and success_report_instance.report_status.id in [2, 3]:
        return "Report is in progress and cannot be updated."
    
    # If the report exists and its status is 4, return a message indicating that the report has already been created
    if success_report_instance and success_report_instance.report_status.id == 4:
        return "Report has already been created." 
    
    menu_card = MenuCardMaster.objects.filter(menu_card=data.get('menu_card')).first()
    product = ProductMaster.objects.filter(product_name=data.get('product')).first()
    capability = CapabilityMaster.objects.filter(capability_name=data.get('capability')).first()
    sub_capability = SubCapabilityMaster.objects.filter(sub_capability_name=data.get('sub_capability')).first()
    customer = CustomerMaster.objects.filter(customer_name=data.get('customer_name')).first()


    if not capability:
        return "Please select capability !"


    expert, created = ExpertMaster.objects.get_or_create(
        expert_name=data.get('expert_name'),
        defaults={'expert_email': data.get('expert_email')}
    )
    customer_contact, created_customer_contact = CustomerContactMaster.objects.get_or_create(
        customer_contact=data.get('customer_contact'),
        defaults={
            'customer_email': data.get('customer_email'),
            'created_by': expert,
            'updated_by': expert
        }
    )
    sdm = SDMMaster.objects.filter(sdm_name=data.get('sdm_name')).first()
    csm = CSMMaster.objects.filter(csm_name=data.get('csm_name')).first()
    sdo = SdoMaster.objects.filter(sdo_name=data.get('sdo_name')).first()

    # Determining report status based on action
    report_status_id = 5 if data.get('action') == 'saved' else 2
    report_status = ReportStatusMaster.objects.get(id=report_status_id)

    # Handling transaction for atomicity
    with transaction.atomic():
        # Creating or updating SuccessReport object
        success_report_instance, created_success_report = SuccessReport.objects.get_or_create(
        jira_key=data.get('issue_key'),
        defaults={
            'menu_card': menu_card,
            'product': product,
            'capability': capability,
            'sub_capability': sub_capability,
            'snow_case_no': data.get('snow_case_no'),
            'report_status': report_status,
            "expert": expert,
            "customer": customer,
            "customer_contact": customer_contact,
            'sdm': sdm,
            'sdo': sdo,
            'csm': csm,
            'logo_url': data.get('logo_url',''),
        }
    )
        msg ="Report saved successfully."

        # If SuccessReport was not newly created, update the data
        if not created_success_report and success_report_instance.report_status.id not in [2, 3]:
            success_report_instance.menu_card = menu_card
            success_report_instance.product = product
            success_report_instance.capability = capability
            success_report_instance.sub_capability = sub_capability
            success_report_instance.snow_case_no = data.get('snow_case_no')
            success_report_instance.report_status = report_status
            success_report_instance.expert = expert
            success_report_instance.customer = customer
            success_report_instance.customer_contact = customer_contact
            success_report_instance.sdm = sdm
            success_report_instance.sdo = sdo
            success_report_instance.csm = csm
            success_report_instance.logo_url = data.get('logo_url','')
            success_report_instance.save()

        # If action is 'created', update the report status and perform additional actions
        if data.get('action') == 'created':
            update_report_status(success_report_instance.pk, "2")
            msg = "Report initiated successfully."
            # Additional actions for 'created' action
            # create_folder_and_upload_to_sharepoint(success_report_instance)
        # If action is 'created', update the report status and perform additional actions
        if data.get('action') == 'saved':
            msg = "Report saved successfully."
           
    return msg



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

file_storage = FileSystemStorage(location=os.getenv('CLIENT_IMAGES', 'client_images/'))

#Saving logo data
def upload_logo_image(logo_file, customer_name):
    try:
        customer = CustomerMaster.objects.filter(customer_name=customer_name).first()
        # Check if file size exceeds 500KB
        max_size_kb = 500
        max_size_bytes = max_size_kb * 1024  # Convert KB to bytes
        if logo_file.size > max_size_bytes:
            raise ValidationError("File size exceeds the maximum allowed (500KB)")

        # Replace spaces with underscores in customer name
        customer_name = re.sub(r'\s+', '_', customer_name)
        # Get file extension
        file_extension = logo_file.name.split('.')[-1]
        # Construct new filename with customer name and ID
        if customer.customer_id:
            new_filename = f"{customer_name}_{customer.customer_id}.{file_extension}"
        else:
            new_filename = f"{customer_name}.{file_extension}"
       
        # Check if a file with the same name already exists
        if file_storage.exists(new_filename):
            # If the file exists, delete it
            file_storage.delete(new_filename)

        # Save the file using FileSystemStorage, which handles file name conflicts
        saved_file_name = file_storage.save(new_filename, logo_file)

        # Check if a logo with the same filename already exists
        existing_logo = LogoMaster.objects.filter(logo_file_name=new_filename).first()

        if existing_logo:
            # Update existing logo
            existing_logo.logo_file_type = logo_file.content_type
            existing_logo.logo_file_size = logo_file.size
            existing_logo.logo_image = saved_file_name  # Update image field with saved file name
            existing_logo.save()
            return existing_logo.id, None
        else:
            # Create a new LogoMaster instance
            logo = LogoMaster.objects.create(
                logo_file_name=new_filename,
                logo_file_type=logo_file.content_type,
                logo_file_size=logo_file.size,
                logo_image=saved_file_name  # Assign saved file name to the image field
            )
            return logo.id, None
    except ValidationError as e:
        # Handle validation errors
        error_message = "Validation Error: {}".format(e)
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
