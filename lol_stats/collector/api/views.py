from collector import models
from rest_framework import viewsets, status, permissions
from collector.api import serializers
from rest_framework.response import Response


class SummonerViewSet(viewsets.ModelViewSet):
    queryset = models.Summoner.objects.all()
    serializer_class = serializers.SummonerSerializer
    permission_classes = [permissions.AllowAny]

    def create(self, request):
        summoner_name = request.data["name"]
        summoner = models.Summoner.objects.create(summoner_name)
        summoner = serializers.SummonerSerializer(summoner)
        return Response(summoner.data,status=status.HTTP_201_CREATED)