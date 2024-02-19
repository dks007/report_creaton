"""

"""
from django.contrib.auth.models import User

from apps.dashboard.models import MenuCardMaster, CustomerMaster, ExpertMaster, ProductMaster, CapabilityMaster, \
    SubCapabilityMaster, StatusMaster, CreatorMaster, ReportStatusMaster, SuccessReport, ProjectMaster


def success_report(data: dict):
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
