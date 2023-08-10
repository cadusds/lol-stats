import json
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
            summoner = models.Summoner.objects.create_summoner_by_name(summoner_name)
        except IntegrityError:
            return Response(
                {"error": f"The summoner {summoner_name} already exists."},
                status=status.HTTP_400_BAD_REQUEST,
            )
        summoner = serializers.SummonerSerializer(
            summoner, context={"request": request}
        )
        return Response(summoner.data, status=status.HTTP_201_CREATED)


class MatchViesSet(viewsets.ModelViewSet):
    queryset = models.SummonerMatch.objects.all()
    serializer_class = serializers.MatchsSerializer
    permission_classes = [permissions.AllowAny]

    def create(self, request):
        name = request.data["name"]
        try:
            summoner = models.Summoner.objects.get(name=name)
        except:
            return Response(
                {"error": f"The summoner with name {name}, not exists"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        matchs = models.SummonerMatch.objects.create_all_matchs_by_puuid(summoner.puuid)
        data = list()
        for match in matchs:
            match = serializers.MatchsSerializer(
                match, context=dict(request=request)
            ).data
            data.append(match)
        return Response(data={"data": data}, status=status.HTTP_201_CREATED)
