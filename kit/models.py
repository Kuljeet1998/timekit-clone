from django.db import models
from timezone_field import TimeZoneField
from django.utils.timezone import now
from django.contrib.auth.models import User
from common.models import TimeStampedUUIDModel
from .constants import *
from django.utils import timezone
# Create your models here.
class Resource(TimeStampedUUIDModel):
    timezone = models.CharField(max_length=32, choices=TIMEZONES, default='UTC')
    resource_type = models.CharField(max_length=6, choices=RESOURCE_TYPE)

    def __str__(self):
        return self.resource_type

class Customer(TimeStampedUUIDModel):
    user = models.OneToOneField(User,
                                related_name='customer',
                                on_delete='models.CASCADE')
    timezone = models.CharField(max_length=32, choices=TIMEZONES, default='UTC')

    def __str__(self):
        return self.user.username

class Person(Resource):
    user = models.OneToOneField(User,
                                related_name='person',
                                on_delete='models.CASCADE')

    def __str__(self):
        return self.user.username

class Asset(Resource):
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name


class Project(TimeStampedUUIDModel):
    name = models.CharField(max_length=100)
    type = models.CharField(max_length=15,choices=PROJECT_TYPE)

    resources = models.ManyToManyField(Resource,
                                        related_name='projects')

class Widget(TimeStampedUUIDModel):
    display_name = models.CharField(max_length=100)
    calendar_type = models.CharField(max_length=15, choices=CALENDAR_TYPE, default='week')
    time_format = models.PositiveIntegerField(choices=TIME_FORMAT, default=24)
    button_text = models.CharField(max_length=100,default="Book it")
    success_message = models.CharField(max_length=300, default="We have received your booking and sent a confirmation")

    project = models.OneToOneField(Project,
                                    related_name='widget',
                                    on_delete=models.CASCADE)

    def __str__(self):
        return self.display_name

class ProjectOneToOne(Project):
    pass

    def __str__(self):
        return self.name

class ProjectManyToOne(Project):
    pass

    def __str__(self):
        return self.name

class SlotSetting(TimeStampedUUIDModel):
    name = models.CharField(max_length=50,default="what")
    location = models.CharField(max_length=300, default='TBD')
    duration = models.PositiveIntegerField(default=60) #in minutes
    min_booking_notice = models.PositiveIntegerField(default=1) #in hours
    min_cancellation_notice = models.PositiveIntegerField(default=60) #in minutes
    future_limit = models.PositiveIntegerField(default=28) #in days
    buffer_time = models.PositiveIntegerField(default=0) #in minutes

    project = models.OneToOneField(ProjectOneToOne,
                                    related_name='slot_setting',
                                    on_delete=models.CASCADE)

    def __str__(self):
        return self.name

class OpeningHour(TimeStampedUUIDModel):
    day = models.CharField(max_length=20,choices=DAYS)
    start_time = models.TimeField()
    end_time = models.TimeField()

    project = models.ForeignKey(ProjectOneToOne,
                                related_name='opening_hours',
                                on_delete=models.CASCADE)
    def __str__(self):
        return "{project} - {day} from {from_time} to {to}".format(project=self.project.name,day=self.day,from_time=self.start_time,to=self.end_time)

class Slot(TimeStampedUUIDModel):
    name = models.CharField(max_length=50,default='name')
    location = models.CharField(max_length=300, default='TBD')
    start_time = models.DateTimeField(default=timezone.now())
    end_time = models.DateTimeField(default=timezone.now()+timezone.timedelta(hours=1))
    max_seats = models.PositiveIntegerField(default=3)
    slot_duration = models.PositiveIntegerField(default=1) #in hours

    resource = models.ForeignKey(Resource,
                                    related_name='slots',
                                    on_delete=models.CASCADE)
    project = models.ForeignKey(ProjectManyToOne,
                                related_name='slots',
                                on_delete=models.CASCADE)

    def __str__(self):
        return self.name

class Booking(TimeStampedUUIDModel):
    state = models.CharField(max_length=23,choices=STATE,default='tentative')

    booked_by = models.ForeignKey(Customer,
                                    related_name='bookings',
                                    on_delete=models.CASCADE)
   

class OneToOneBooking(Booking):
    start_date_time = models.DateTimeField()
    end_date_time = models.DateTimeField()
    booking_type = models.CharField(max_length=15,choices=BOOKING_TYPE_1_1, default='instant')

    resource = models.OneToOneField(Resource,
                                    related_name='one_to_one_booking',
                                    on_delete=models.CASCADE)
    project = models.ForeignKey(ProjectOneToOne,
                                related_name='bookings',
                                on_delete=models.CASCADE)

class ManyToOneBooking(Booking):
    booking_type = models.CharField(max_length=14,choices=BOOKING_TYPE_M_1, default='group_customer')
    slot = models.ForeignKey(Slot,
                                related_name='many_to_one_bookings',
                                on_delete=models.CASCADE)