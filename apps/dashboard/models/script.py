import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "success_tool.settings")

import django
django.setup()

from apps.dashboard.models.masters import SdoMaster, MenuCardMaster, MenuSdoMapping


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

insert_data()