from django.shortcuts import get_object_or_404
from workproject.models import Data
from workproject.models import data_raw_sql_query
from workproject.serializers import DataSerializer

from rest_framework import viewsets, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.parsers import JSONParser
from rest_framework.decorators import detail_route, list_route

# Create your views here.
class DataViewSet(viewsets.ModelViewSet):
    queryset = Data.objects.all()
    #queryset = Data.objects.raw("select * from data where publishtime=(select max(publishtime) from data)")
    serializer_class = DataSerializer
    @list_route(methods=['get'])
    def raw_sql_query(self, request):
        longitudee = request.query_params.get('longitude', None)
        data = data_raw_sql_query(longitude=longitudee)
        serializer = DataSerializer(data, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
