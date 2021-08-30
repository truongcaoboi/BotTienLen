from django.urls import path, include
from bottienlen import views

urlpatterns=[
    path('getaction', views.get_action_bot)
]