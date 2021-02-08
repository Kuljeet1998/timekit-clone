from django.shortcuts import render
from .models import *
from .serializers import *
from rest_framework import viewsets, exceptions
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from rest_framework.decorators import action
# Create your views here.

class CreateListMixin:
    def get_serializer(self, *args, **kwargs):
        if isinstance(kwargs.get('data', {}), list):
            kwargs['many'] = True
        return super().get_serializer(*args, **kwargs)


class ResourceViewSet(viewsets.ModelViewSet):
    queryset = Resource.objects.all()
    serializer_class = ResourceSerializer

class PersonViewSet(viewsets.ModelViewSet):
    queryset = Person.objects.all()
    serializer_class = PersonSerializer

    def create(self, request, *args, **kwargs):
        username = request.data['name']
        email = request.data['email']
        if User.objects.filter(username=username,email=email).exists():
            raise exceptions.ValidationError('Resource already exists')

        user = User.objects.create(username=username,email=email)
        self.request.data['user']=str(user.id)
        self.request.data['resource_type']="person"
        return super().create(request, *args, **kwargs)

class AssetViewSet(viewsets.ModelViewSet):
    queryset = Asset.objects.all()
    serializer_class = AssetSerializer

    def create(self, request, *args, **kwargs):
        self.request.data['resource_type']="asset"
        return super().create(request, *args, **kwargs)

class ProjectViewSet(viewsets.ModelViewSet):
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer

class WidgetViewSet(viewsets.ModelViewSet):
    queryset = Widget.objects.all()
    serializer_class = WidgetSerializer

class ProjectOneToOneViewSet(viewsets.ModelViewSet):
    queryset = ProjectOneToOne.objects.all()
    serializer_class = ProjectOneToOneSerializer

    def create(self, request, *args, **kwargs):
        name = request.data["name"]
        resources = request.data["resources"]
        availability = request.data["availability"]
        availability_constraints = request.data['availability_constraints']
        ui = request.data["ui"]

        project = ProjectOneToOne.objects.create(name=name,type="1_1")
        project.resources.set(Resource.objects.filter(id__in=resources))
        project.save()

        duration = availability['length']
        buffer_time = availability['buffer']
        future_limit = availability['to']

        duration = duration.split()
        if duration[1]=='minutes':
            duration=duration[0]
        elif duration[1]=='hours':
            duration=duration[0]*60
        else:
            raise exceptions.ValidationError("length can only be in minutes/hours")

        buffer_time = buffer_time.split()
        if buffer_time[1]=='minutes':
            buffer_time=buffer_time[0]
        elif buffer_time[1]=='hours':
            buffer_time=buffer_time[0]*60
        else:
            raise exceptions.ValidationError("buffer time can only be in minutes/hours")

        future_limit = future_limit.split()
        if future_limit[1]=='days':
            future_limit=future_limit[0]
        elif future_limit[1]=='weeks':
            future_limit=future_limit[0]*7
        else:
            raise exceptions.ValidationError("future limit ('to' field) can only be in days/weeks")

        slot_setting = SlotSetting.objects.create(duration=duration,
                                                    buffer_time=buffer_time,
                                                    future_limit=future_limit,
                                                    project=project)

        for availability_constraint in availability_constraints:
            OpeningHour.objects.create(day=availability_constraint["day"],
                                        start_time=availability_constraint["start"],
                                        end_time=availability_constraint["end"],
                                        project=project)

        widget = Widget.objects.create(display_name=ui['display_name'],
                                        time_format=ui['time_format'],
                                        button_text=ui['submit_button'],
                                        success_message=ui['success_message'],
                                        project=project)

        data = ProjectOneToOneSerializer(project).data
        return Response(data, status=200)

    @action(detail=True, methods=['post','get'], url_path='resources')
    def add_resources(self, request, pk=None, *args, **kwargs):
        if request.method == 'POST':
            project = get_object_or_404(ProjectOneToOne, id=pk)
            resource_id = request.data['resource_id']
            resource = get_object_or_404(Resource,id=resource_id)
            project.resources.add(resource)
            data = ProjectOneToOneSerializer(project).data
            return Response(data, status=200)

        elif request.method == 'GET':
            project = get_object_or_404(ProjectOneToOne, id=pk)
            resources = project.resources.all().values_list('id',flat=True)
            data = {"data":resources}
            return Response(data, status=200)


class ProjectManyToOneViewSet(viewsets.ModelViewSet):
    queryset = ProjectManyToOne.objects.all()
    serializer_class = ProjectManyToOneSerializer

    def create(self, request, *args, **kwargs):
        name = request.data["name"]
        resources = request.data["resources"]
        ui = request.data["ui"]

        project = ProjectManyToOne.objects.create(name=name,type="m_1")
        project.resources.set(Resource.objects.filter(id__in=resources))
        project.save()

        widget = Widget.objects.create(display_name=ui['display_name'],
                                        time_format=ui['time_format'],
                                        button_text=ui['submit_button'],
                                        success_message=ui['success_message'],
                                        project=project)

        data = ProjectOneToOneSerializer(project).data
        return Response(data, status=200)

    @action(detail=True, methods=['get','post'], url_path='resources')
    def add_resources(self, request, pk=None, *args, **kwargs):
        if request.method == 'POST':
            project = get_object_or_404(ProjectManyToOne, id=pk)
            resource_id = request.data['resource_id']
            resource = get_object_or_404(Resource,id=resource_id)
            project.resources.add(resource)
            data = ProjectOneToOneSerializer(project).data
            return Response(data, status=200)

        elif request.method == 'GET':
            project = get_object_or_404(ProjectManyToOne, id=pk)
            resources = project.resources.all().values_list('id',flat=True)
            data = {"data":resources}
            return Response(data, status=200)

class SlotSettingViewSet(viewsets.ModelViewSet):
    queryset = SlotSetting.objects.all()
    serializer_class = SlotSettingSerializer

class OpeningHourViewSet(viewsets.ModelViewSet):
    queryset = OpeningHour.objects.all()
    serializer_class = OpeningHourSerializer

class SlotViewSet(viewsets.ModelViewSet):
    queryset = Slot.objects.all()
    serializer_class = SlotSerializer

class BookingViewSet(viewsets.ModelViewSet):
    queryset = Booking.objects.all()
    serializer_class = BookingSerializer

    @action(detail=False, methods=['get'], url_path='group')
    def decline_booking_owner(self, request, pk=None, *args, **kwargs):
        if request.method == 'GET':
            booking = get_object_or_404(ManyToOneBooking, id=pk)
            data = ManyToOneBookingSerializer(booking).data
            return Response(data, status=200)

class OneToOneBookingViewSet(CreateListMixin,viewsets.ModelViewSet):
    queryset = OneToOneBooking.objects.all()
    serializer_class = OneToOneBookingSerializer

    def create(self, request, *args, **kwargs):
        graph = request.data['graph']
        start = request.data['start']
        end = request.data['end']
        name = request.data['what']
        location = request.data['where']
        resource_id = request.data['resource_id']
        project_id = request.data['project_id']
        customer = request.data['customer']
        username = customer['name']
        email = customer['email']
        timezone = customer['timezone']

        obj, created = User.objects.get_or_create(username=username,
                                                    email=email)
        if created:
            customer_obj = Customer.objects.create(user=obj,timezone=timezone)
        else:
            if Customer.objects.filter(user=obj,timezone=timezone).exists():
                customer_obj = Customer.objects.get(user=obj,timezone=timezone)
            else:
                customer_obj = Customer.objects.create(user=obj,timezone=timezone)

        slot_settings, created = SlotSetting.objects.get_or_create(project_id=project_id)
        slot_settings.name = name
        slot_settings.location = location
        slot_settings.save()

        resource = get_object_or_404(Resource, id=resource_id)
        project = get_object_or_404(ProjectOneToOne, id=project_id)
        booking = OneToOneBooking.objects.create(booked_by=customer_obj,
                                                    start_date_time=start,end_date_time=end,
                                                    booking_type=graph,
                                                    resource=resource,
                                                    project=project)
        data = OneToOneBookingSerializer(booking).data
        return Response(data, status=200)
        
    def retrieve(self,request, *args, **kwargs):
        try:
            include = request.query_params.get('include')
        except:
            include=None

        booking_id = kwargs['pk']
        booking = get_object_or_404(OneToOneBooking, id=booking_id)
        data = OneToOneBookingSerializer(booking).data
        if include is not None:
            extra_fields = include.split(',')
            for extra_field in extra_fields:
                if extra_field=='available_actions':
                    if data['booking_type']=='instant':
                        available_actions=[]
                    elif data['booking_type']=='confrim_decline':
                        if data['completed']==True:
                            available_actions=[]
                        elif data['state'] is None:
                            available_actions=["decline","confirm"]
                        else:
                            available_actions=[]
                    data['available_actions']=available_actions
                elif extra_field=='attributes':
                    event_info = {
                            "event_info":{
                                    "what":booking.project.slot_setting.name,
                                    "where":booking.project.slot_setting.location
                            }
                    }
                    data['attributes']=event_info
                elif extra_field=='customers':
                    customer_data = CustomerSerializer(booking.booked_by).data
                    data['customers']=customer_data
        return Response(data, status=200)

    @action(detail=True, methods=['get'], url_path='confirm')
    def confirm_booking(self, request, pk=None, *args, **kwargs):
        if request.method == 'GET':
            booking = get_object_or_404(OneToOneBooking, id=pk)
            booking.state='confirmed'
            booking.save()
            data = OneToOneBookingSerializer(booking).data
            return Response(data, status=200)

    @action(detail=True, methods=['get'], url_path='decline')
    def decline_booking(self, request, pk=None, *args, **kwargs):
        if request.method == 'GET':
            booking = get_object_or_404(OneToOneBooking, id=pk)
            booking.state='declined'
            booking.save()
            data = OneToOneBookingSerializer(booking).data
            return Response(data, status=200)

class ManyToOneBookingViewSet(CreateListMixin,viewsets.ModelViewSet):
    queryset = ManyToOneBooking.objects.all()
    serializer_class = ManyToOneBookingSerializer

    def create(self, request, *args, **kwargs):
        graph = request.data['graph']
        start = request.data['start']
        end = request.data['end']
        name = request.data['what']
        location = request.data['where']
        resource_id = request.data['resource_id']
        project_id = request.data['project_id']
        customer = request.data['customer']
        username = customer['name']
        email = customer['email']
        timezone = customer['timezone']

        obj, created = User.objects.get_or_create(username=username,
                                                    email=email)
        if created:
            customer_obj = Customer.objects.create(user=obj,timezone=timezone)
        else:
            if Customer.objects.filter(user=obj,timezone=timezone).exists():
                customer_obj = Customer.objects.get(user=obj,timezone=timezone)
            else:
                customer_obj = Customer.objects.create(user=obj,timezone=timezone)

        resource = get_object_or_404(Resource, id=resource_id)
        project = get_object_or_404(ProjectManyToOne, id=project_id)

        slot, created = Slot.objects.get_or_create(resource=resource,
                                                    project=project,
                                                    name = name,
                                                    location = location,
                                                    start_time = start,
                                                    end_time = end)
        if created:
            slot.duration = int(end[11]+end[12]) - int(start[11]+start[12])
            slot.save()
        booking = ManyToOneBooking.objects.get_or_create(booked_by=customer_obj,
                                                            slot=slot,
                                                            booking_type=graph)
        if created==False:
            raise exceptions.ValidationError("This Customer has already booked")

        data = ManyToOneBookingSerializer(booking).data
        return Response(data, status=200)
        
    def retrieve(self,request, *args, **kwargs):
        try:
            include = request.query_params.get('include')
        except:
            include=None

        booking_id = kwargs['pk']
        booking = get_object_or_404(ManyToOneBooking, id=booking_id)
        slot = booking.slot
        data = ManyToOneBookingSerializer(booking).data
        if include is not None:
            extra_fields = include.split(',')
            for extra_field in extra_fields:
                if extra_field=='available_actions':
                    if data['booking_type']=='instant':
                        available_actions=[]
                    elif data['booking_type']=='confrim_decline':
                        if data['completed']==True:
                            available_actions=[]
                        elif data['state'] is None:
                            available_actions=["decline","confirm"]
                        else:
                            available_actions=[]
                    data['available_actions']=available_actions
                elif extra_field=='attributes':
                    event_info = {
                            "event_info":{
                                    "what":slot.name,
                                    "where":slot.location
                            }
                    }
                    data['attributes']=event_info
                elif extra_field=='customers':
                    customer_ids = slot.many_to_one_bookings.all().values_list('booked_by__id',flat=True)
                    customers = Customer.objects.filter(id__in=customer_ids)
                    customer_data = CustomerSerializer(customers,many=True).data
                    data['customers']=customer_data
        return Response(data, status=200)

    @action(detail=True, methods=['get'], url_path='cancel-customer')
    def decline_booking_customer(self, request, pk=None, *args, **kwargs):
        if request.method == 'GET':
            booking = get_object_or_404(ManyToOneBooking, id=pk)
            booking.state='cancelled_by_customer'
            booking.save()
            data = ManyToOneBookingSerializer(booking).data
            return Response(data, status=200)

    @action(detail=True, methods=['get'], url_path='cancel-owner')
    def decline_booking_owner(self, request, pk=None, *args, **kwargs):
        if request.method == 'GET':
            booking = get_object_or_404(ManyToOneBooking, id=pk)
            booking.state='cancelled_by_owner'
            booking.save()
            data = ManyToOneBookingSerializer(booking).data
            return Response(data, status=200)

    @action(detail=True, methods=['get'], url_path='confirm')
    def decline_booking_owner(self, request, pk=None, *args, **kwargs):
        if request.method == 'GET':
            booking = get_object_or_404(ManyToOneBooking, id=pk)
            booking.state='confirmed'
            booking.save()
            data = ManyToOneBookingSerializer(booking).data
            return Response(data, status=200)