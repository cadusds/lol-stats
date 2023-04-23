from collector import models
from rest_framework import viewsets
from rest_framework import permissions
from collector.api import serializers


class SummonerViewSet(viewsets.ModelViewSet):
    queryset = models.Summoners.objects.all()
    serializer_class = serializers.SummonersSerializer
    permission_classes = [permissions.AllowAny]

    def create(self, request, *args, **kwargs):
        return super().create(request,*args,**kwargs)