from django.contrib import admin
from .models import *
# Register your models here.
admin.site.register(Resource)
admin.site.register(Person)
admin.site.register(Asset)
admin.site.register(Project)
admin.site.register(Widget)
admin.site.register(ProjectOneToOne)
admin.site.register(ProjectManyToOne)
admin.site.register(SlotSetting)
admin.site.register(OpeningHour)
admin.site.register(Slot)
admin.site.register(Booking)
admin.site.register(OneToOneBooking)
admin.site.register(ManyToOneBooking)
admin.site.register(Customer)