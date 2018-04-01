from django.conf.urls import url
from eatTogether import views


urlpatterns = [
    url(r'^eating/', views.eating, name='eating'),
    url(r'^invite/', views.invite, name='invite'),
    url(r'^inviteMember/', views.inviteMember, name='inviteMember'),

]