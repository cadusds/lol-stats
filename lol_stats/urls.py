"""lol_stats URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from rest_framework import routers
from collector.api import views


router = routers.DefaultRouter()
router.register(r"summoners", views.SummonerViewSet, basename="summoner")
router.register(
    r"summoner_matchs", views.SummonerMatchViewSet, basename="summoner_match"
)
router.register(r"matchs", views.MatchViewSet, basename="match")
router.register(
    r"match_participant_stats",
    views.MatchParticipantStatsViewSet,
    basename="match_participants_stats",
)
router.register(
    r"match_participant_basic_stats",
    views.MatchParticipantBasicStatsViewSet,
    basename="match_participants_basic_stats",
)
router.register(
    r"match_participant_champion_stats",
    views.MatchParticipantChampionStatsViewSet,
    basename="match_participants_champion_stats",
)

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include(router.urls)),
    path("api-auth/", include("rest_framework.urls", namespace="rest_framework")),
]
