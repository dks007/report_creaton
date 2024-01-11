import datetime
import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "success_tool.settings")

import django
django.setup()

from apps.dashboard.models.masters import (SdoMaster, MenuCardMaster, MenuSdoMapping, CustomerMaster, RegionMaster,
                                           ProjectMaster, SuccessServiceMaster, PSMMaster, CSMMaster, SDMMaster,
                                           IndustryMaster, SuccessElementsMaster, CustomerMapping)


def insert_data():
    menu_card_data = MenuCardMaster.objects.all()

    for mn in menu_card_data:

        if mn.menu_card.startswith("EMA") or mn.menu_card.startswith("TAA"):
            sdo = SdoMaster.objects.get(id=3)
            MenuSdoMapping.objects.create(
                menu_card_id=mn,
                sdo_id=sdo,
                status='1'
            )
    return True

# insert_data()


def insert_details():
    customer = CustomerMaster.objects.all()
    region = RegionMaster.objects.all()
    project = ProjectMaster.objects.all()
    success = SuccessServiceMaster.objects.all()
    csm = CSMMaster.objects.all()
    psm = PSMMaster.objects.all()
    sdm = SDMMaster.objects.all()
    inds = IndustryMaster.objects.all()
    succE = SuccessElementsMaster.objects.all()

    for cus, reg, pr, suc, cs, ps, sd, ind, succ in zip(customer,region, project, success, csm, psm, sdm, inds,succE):
        CustomerMapping.objects.create(
            customer_id=cus,
            region_id=reg,
            project_id=pr,
            success_service_id=suc,
            csm_id=cs,
            psm_id=ps,
            sdm_id=sd,
            industry_id=ind,
            success_elements_id=succ,
            description='description',
            created_date=datetime.date.today(),
            updated_date=datetime.date.today(),
            status='1'


        )
    return True


# test = insert_details()
# print(test)
def abc():
    print(os.getenv('JIRA_URL'))
abc()