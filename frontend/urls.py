from django.urls import path
from . import views

urlpatterns = [
    path('searchkeyword', views.result,name="searchkeyword"),
    path('', views.index,name="index"),
]
