from django.urls import path

from . import views

urlpatterns = [
    path('<str:userID>', views.index, name='index'),
]