# tasks.py

from celery import shared_task
from .models import SuccessReport, CeleryTask
from .master.models import Expert, Creator  # Adjust the import paths
from .utils import create_folder_and_upload_to_sharepoint

@shared_task
def process_report_task(success_report_id, celery_task_id):
    success_report = SuccessReport.objects.get(id=success_report_id)
    celery_task = CeleryTask.objects.get(id=celery_task_id)

    # Check if the expert exists, otherwise create a new one
    expert_name = success_report.expert_name
    expert, created_expert = Expert.objects.get_or_create(expert_name=expert_name)

    # Check if the creator exists, otherwise create a new one
    creator_name = success_report.creator_name
    creator, created_creator = Creator.objects.get_or_create(creator_name=creator_name)

    # Update SuccessReport with the expert and creator IDs
    success_report.expert = expert
    success_report.creator = creator
    success_report.save()

    # Continue with other tasks
    download_link = create_folder_and_upload_to_sharepoint(success_report)

    # Update SuccessReport with the download link
    success_report.download_link = download_link
    success_report.save()

    celery_task.delete()  # Remove CeleryTask entry after processing
