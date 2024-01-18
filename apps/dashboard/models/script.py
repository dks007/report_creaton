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
    # print(menu_card_data,'>>>>>>>>>>')

    for mn in menu_card_data:

        if mn.menu_card.startswith("SAA"):
            sdo = SdoMaster.objects.get(id=1)
            MenuSdoMapping.objects.create(
                menu_card_id=mn,
                sdo_id=sdo,
                status='1'
            )
    return True

# a=insert_data()
# print(a)


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
            customer=cus,
            region=reg,
            project=pr,
            success_service=suc,
            csm=cs,
            psm=ps,
            sdm=sd,
            industry=ind,
            success_elements=succ,
            description='description',
            created_date=datetime.date.today(),
            updated_date=datetime.date.today(),
            status='1'


        )
    return True


# test = insert_details()
# print(test)
