from django.conf.urls import url
from startEat import views


urlpatterns = [
    url(r'^start/', views.start, name='start'),
    url(r'^challenge/', views.challenge, name='challenge'),
    url(r'^game/', views.game, name='game'),
    url(r'^end/', views.end, name='end'),
]