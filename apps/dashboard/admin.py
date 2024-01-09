# dashboard/admin.py
from django.contrib import admin
from apps.dashboard.models.masters import (SdoMaster, PSMMaster, CSMMaster, SDMMaster, IndustryMaster, RegionMaster,
                                           SuccessElementsMaster, SuccessServiceMaster, CustomerMaster,
                                           CapabilityMaster, SubCapabilityMaster, ProjectMaster, MenuSdoMapping,
                                           CustomerMapping)


admin.site.register(SdoMaster)
admin.site.register(PSMMaster)
admin.site.register(CSMMaster)
admin.site.register(SDMMaster)
admin.site.register(RegionMaster)
admin.site.register(CustomerMaster)
admin.site.register(SuccessServiceMaster)
admin.site.register(SuccessElementsMaster)
admin.site.register(IndustryMaster)
admin.site.register(CapabilityMaster)
admin.site.register(SubCapabilityMaster)
admin.site.register(ProjectMaster)
admin.site.register(MenuSdoMapping)
admin.site.register(CustomerMapping)
