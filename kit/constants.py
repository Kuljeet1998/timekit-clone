import pytz

TIMEZONES = tuple(zip(pytz.all_timezones, pytz.all_timezones))
RESOURCE_TYPE = (('person','person'),('asset','asset'))
STATE = (('tentative','tentative'),('confirmed','confirmed'),('error','error'),
        ('declined','declined'),('completed','completed'),('cancelled_by_owner','cancelled_by_owner'),
        ('cancelled_by_customer','cancelled_by_customer'),('rescheduled_by_customer','rescheduled_by_customer'))
TYPE = (('text','text'),('email','email'),('phone','phone'))
CALENDAR_TYPE = (('week','week'),('list','list'))
TIME_FORMAT = ((24,'24'),(12,'12'))
PROJECT_TYPE = (('1_1','1-1'),('m_1','m-1'))
DAYS = (('monday','monday'),('tuesday','tuesday'),('wednesday','wednesday'),
        ('thursday','thursday'),('friday','friday'),('saturday','saturday'),('sunday','sunday'))
BOOKING_TYPE_1_1=(('instant','instant'),('confirm_decline','confirm_decline'))
BOOKING_TYPE_M_1=(('group_owner','group_owner'),('group_customer','group_customer'))