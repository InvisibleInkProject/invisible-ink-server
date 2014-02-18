from django_cron import CronJobBase, Schedule
from inks.models import Message
from datetime import datetime
from django.utils.timezone import utc

import logging
logger = logging.getLogger(__name__)

class DeleteExpiredInks(CronJobBase):

    RUN_EVERY_MINS = 5
    RETRY_AFTER_FAILURE_MINS = 0

    schedule = Schedule(run_every_mins=RUN_EVERY_MINS,  retry_after_failure_mins=RETRY_AFTER_FAILURE_MINS)
    code = 'inks.DeleteExpiredInks'    # a unique code

    def do(self):
    	logger.debug('DeleteExpiredInks.do: delete inks')
    	now_utc = datetime.utcnow().replace(tzinfo=utc)
    	Message.objects.filter(expires__range=["2011-01-01", now_utc]).delete()