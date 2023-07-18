from celery import shared_task
from accounts.models import OtpCode
import pytz
from datetime import timedelta, datetime


@shared_task
def delete_otp_code():
    expired_time = datetime.now(tz=pytz.timezone('Asia/Tehran')) - timedelta(minutes=5)
    OtpCode.objects.filter(created__lt=expired_time).delete()
