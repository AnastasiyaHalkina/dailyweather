from django.urls import path
from . import views


app_name = 'accuweather_bot'

urlpatterns = [
    path('weather/bot<bot_token>/', views.command_view),
]
