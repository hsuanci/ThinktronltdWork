from rest_framework import serializers
from workproject.models import Data


class DataSerializer(serializers.ModelSerializer):
    class Meta:
        model = Data
       # fields = '__all__'
        fields = ('sitename', 'county', 'aqi', 'publishtime', 'longitude','latitude')
