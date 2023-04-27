from collector import models
from rest_framework import viewsets, status, permissions
from collector.api import serializers
from rest_framework.response import Response
from django.db.utils import IntegrityError


class SummonerViewSet(viewsets.ModelViewSet):
    queryset = models.Summoner.objects.all()
    serializer_class = serializers.SummonerSerializer
    permission_classes = [permissions.AllowAny]

    def create(self, request):
        summoner_name = request.data["name"]
        try:
            summoner = models.Summoner.objects.create(summoner_name)
        except IntegrityError:
            return Response({"error":f"The summoner {summoner_name} already exists."}, status=status.HTTP_400_BAD_REQUEST)
        summoner = serializers.SummonerSerializer(summoner)
        return Response(summoner.data,status=status.HTTP_201_CREATED)