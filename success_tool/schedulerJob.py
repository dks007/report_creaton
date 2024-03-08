from docxtpl import DocxTemplate
from docxtpl import InlineImage
from datetime import datetime
from apps.dashboard.models import SuccessReport,ReportStatusMaster
from django.core.exceptions import ObjectDoesNotExist


def executeSchedulerJob(): 
    print ("Inside the SchedulerJob Class executeSchedulerJob method")
    
    # Get the record from Success Report table where the reportstatus is "Initiated":2
    reportDict = getSuccessReportData ('3')
        
    if (reportDict != None):
        #print (reportDict['report_status'])
        
        reportLocation = "=https://successpilot.corpnet.ifsworld.com/report/"
        templateName="goldenTemplate/IFS_Success_Final_Report_Template.docx"

        #doc = DocxTemplate ("C:\\Users\\lokain\\Documents\\workarea\\Success-Pilot-Web-Project\\IFS_Success_Final_Report_Template.docx")
        
        #f = open("C:\\Users\\lokain\\Documents\\workarea\\Success-Pilot-Web-Project\\IFS_Success_Final_Report_Template.docx", 'rb')
        #doc = DocxTemplate(f)
        #f.close()

        doc = DocxTemplate (reportLocation+templateName)
        context = {
            'Insert_MenuCard_Service_Heading_and_Number_Here' : reportDict['menu_description']+' : '+reportDict['menu_card'],
            'Insert_Customer_branding_here' : InlineImage (doc, 'C:\\Users\\lokain\\Documents\\workarea\\Success-Pilot-Web-Project\\acmeCorporation.png'),
            'customer_name' : reportDict['customer_name'],
            'List_the_names_of_the_participants_from_IFS' : reportDict['expert_name'],
            'List_the_names_of_the_participants_from_customer': reportDict['customer_contact'],
            'ServiceNow_ID' : reportDict['snow_case_no']
            }
        doc.render(context)
                
        #reportName naming convention "EBP_MenuCardId_Product_Capability_SubCapability_SnowCaseId"
        reportName='EBP - '+reportDict['menu_card']+' - '+reportDict['product_name']+' - '+reportDict['capability_name']+' - '+reportDict['sub_capability_name']+' - '+reportDict['snow_case_no']+'.docx'
        #reportName="cs002345.docx"
        #reportLocation="C:\\Users\\lokain\\Documents\\workarea\\Success-Pilot-Web-Project\\"
        doc.save (reportLocation+reportName)

        updateSuccessReport(reportDict['id'], 4, reportLocation+reportName)
        print ("Updated reportStatus to Created state:4")

        print('Report Generation was Success!!')


# get report data to write document
def getSuccessReportData(statusKey):
    try:
        issue_data_dict = {}
       
        # Attempt to retrieve report data
        report_data = SuccessReport.objects.filter(report_status=statusKey).first()

        #print ("Report_Data",report_data)
       
        # If report_data is None, no record with the provided issueKey was found
        if report_data is None:
            return None

        #update the reportstatus to in-Progress state:3
        updateSuccessReport(report_data.id, 3, '')
        print ("Updated reportStatus to in-Progress state:3")

        # Extract data from report_data and populate issue_data_dict
        #issue_data_dict['sdo_name'] = report_data.sdo.sdo_name.strip()
        #issue_data_dict['csm_name'] = report_data.csm.csm_name.strip()
        #issue_data_dict['sdm_name'] = report_data.sdm.sdm_name.strip()
        issue_data_dict['id'] = report_data.id
        issue_data_dict['snow_case_no'] = report_data.snow_case_no.strip()
        issue_data_dict['menu_card'] = report_data.menu_card.menu_card.strip()
        issue_data_dict['menu_description'] = report_data.menu_card.menu_description.strip()
        issue_data_dict['expert_name'] = report_data.expert.expert_name.strip()
        issue_data_dict['product_name'] = report_data.product.product_name.strip()
        issue_data_dict['capability_name'] = report_data.capability.capability_name.strip()
        issue_data_dict['sub_capability_name'] = report_data.sub_capability.sub_capability_name.strip()
        issue_data_dict['customer_name'] = report_data.customer.customer_name.strip()
        issue_data_dict['customer_contact'] = report_data.customer_contact.customer_contact.strip()
        issue_data_dict['report_status'] = report_data.report_status
        

        #print  (issue_data_dict)
 
        return issue_data_dict
   
    except ObjectDoesNotExist:
        # Handle the case where any of the related objects do not exist
        return None
        
    
def updateSuccessReport(id, reportStatus, downloadLink):    
    successReport = SuccessReport.objects.get(id=id)
    successReport.report_status=ReportStatusMaster(id=reportStatus)
    successReport.download_link=downloadLink
    successReport.save()
    print ("SuccessReport table updated sucessfully")