from unicodedata import name
from django.shortcuts import render
from .models import *
from .serializers import *
from rest_framework.response import Response
from rest_framework import routers, serializers, viewsets
from rest_framework.decorators import action
# Create your views here.


class CustomerViewSet(viewsets.ModelViewSet):
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer

    def get_queryset(self):
        # print(self.request)
        result = Customer.objects.filter(id=1)
        return result

    def list(self, request, *args, **kwargs):
        print(request)
        customer = self.get_queryset()  # Customer.objects.all()
        serializer = CustomerSerializer(customer, many=True)
        return Response(serializer.data)

    def retrieve(self, request, *args, **kwargs):
        customer = Customer.objects.get(id=kwargs['pk'])
        customer = self.get_object()
        serializer = CustomerSerializer(customer, many=False)
        return Response(serializer.data)
        return

    def create(self, request, *args, **kwargs):
        data = request.data
        customer = Customer.objects.create(
            name=data['name'], address=data['address'], data_sheet_id=data['data_sheet']
        )
        profession = Profession.objects.get(id=data['profession'])
        customer.professions.add(profession)
        customer.save()
        serializer = CustomerSerializer(customer)
        return Response(serializer.data)

    def update(self, request, *args, **kwargs):
        customer = self.get_object()
        data = request.data
        customer.name = data['name']
        customer.address = data['address']
        customer.data_sheet_id = data['data_sheet']

        profession = Profession.objects.get(id=data['profession'])

        for p in customer.professions.all():
            customer.professions.remove(p)

        customer.professions.add(profession)
        customer.save()
        serializer = CustomerSerializer(customer)

        return Response(serializer.data)

    def partial_update(self, request, *args, **kwargs):
        customer = self.get_object()
        customer.name = request.data.get("name", customer.name)
        customer.address = request.data.get("address", customer.address)
        customer.data_sheet_id = request.data.get(
            "data_sheet", customer.data_sheet_id)
        customer.save()
        serializer = CustomerSerializer(customer)
        return Response(serializer.data)

    def destroy(self, request, *args, **kwargs):
        customer = self.get_object()
        customer.delete()
        return Response({"message": 'customer deleted'})

    # deactivate only specific id /... customer/3/deactivate
    @action(detail=True)
    def deactivate(self, request, **kwargs):
        customer = self.get_object()
        customer.active = False
        customer.save()
        serializer = CustomerSerializer(customer)
        return Response(serializer.data)

    @action(detail=False)  # deactivate all /... customer/deactivate_all
    def deactivate_all(self, request, **kwargs):
        customers = Customer.objects.all()
        customers.update(active=False)
        serializer = CustomerSerializer(customers, many=True)
        return Response(serializer.data)


class ProfessionViewSet(viewsets.ModelViewSet):
    queryset = Profession.objects.all()
    serializer_class = ProfessionSerializer


class DataSheetViewSet(viewsets.ModelViewSet):
    queryset = DataSheet.objects.all()
    serializer_class = DataSheetSerializer


class DocumentViewSet(viewsets.ModelViewSet):
    queryset = Document.objects.all()
    serializer_class = DocumentSerializer
