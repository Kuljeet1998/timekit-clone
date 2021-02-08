from rest_framework import serializers
from .models import *


class ResourceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Resource
        fields = '__all__'

class CustomerSerializer(serializers.ModelSerializer):
    name = serializers.SerializerMethodField()
    email = serializers.SerializerMethodField()
    class Meta:
        model = Customer
        fields = ('id','name','email','timezone')

    def get_name(self,instance):
        return instance.user.username

    def get_email(self,instance):
        return instance.user.email

class PersonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Person
        fields = '__all__'

class AssetSerializer(serializers.ModelSerializer):
    class Meta:
        model = Asset
        fields = '__all__'

class ProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = '__all__'

class WidgetSerializer(serializers.ModelSerializer):
    class Meta:
        model = Widget
        fields = '__all__'

class ProjectOneToOneSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProjectOneToOne
        fields = '__all__'

class ProjectManyToOneSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProjectManyToOne
        fields = '__all__'

class SlotSettingSerializer(serializers.ModelSerializer):
    class Meta:
        model = SlotSetting
        fields = '__all__'

class OpeningHourSerializer(serializers.ModelSerializer):
    class Meta:
        model = OpeningHour
        fields = '__all__'

class SlotSerializer(serializers.ModelSerializer):
    class Meta:
        model = Slot
        fields = '__all__'

class BookingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Booking
        fields = '__all__'

# class AvailableActionSerializer(serializers.ModelSerializer):
#     available_actions = serializers.SerializerMethodField()

#     class Meta:
#         model = OneToOneBooking
#         fields = ('available_actions')

#     def get_available_actions(self, instance):
#         if data['graph']=='instant':
#             available_actions=[]
#         elif data['graph']=='confrim_decline':
#             if data['completed']==True:
#                 available_actions=[]
#             elif data['state'] is None:
#                 available_actions=["decline","confirm"]
#             else:
#                 available_actions=[]

class OneToOneBookingSerializer(serializers.ModelSerializer):

    class Meta:
        model = OneToOneBooking
        fields = ('id','state','start_date_time','end_date_time','booking_type')

    # def __init__(self, *args, **kwargs):
    #     super(OneToOneBookingSerializer, self).__init__(*args, **kwargs)

    #     if 'context' in kwargs:
    #         if 'include' in kwargs['context']:
    #             tabs = kwargs['context']['include']
    #             if tabs:
    #                 tabs = tabs.split(',')
    #                 included = set(tabs)
    #                 existing = set(self.fields.keys())
    #                 for tab in tabs:
    #                     if tab == "customers":
    #                         customers=[]
    #                         fields = self.fields
    #                         import pdb;
    #                         pdb.set_trace()
    #                         fields["customers"]=
    #                         fields.append("customers")
    #                         self.fields = fields

class ManyToOneBookingSerializer(serializers.ModelSerializer):
    class Meta:
        model = ManyToOneBooking
        fields = ('id','state','booking_type','booked_by')