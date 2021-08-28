from django.urls import path
from .views import NdtvView, QtvView, HomeView, AmazonView, Internshala, Iimjobs, Talentrack

app_name = 'core'

urlpatterns = [
    path('', HomeView.as_view(), name="home"),
    path('ndtv/', NdtvView.as_view(), name="ndtv"),
    path('internshala/', Internshala.as_view(), name="internshala"),
    path('iimjobs/', Iimjobs.as_view(), name="iimjobs"),
    path('talentrack/', Talentrack.as_view(), name="talentrack"),
    path('amazon/', AmazonView.as_view(), name="amazon"),
    path('qtv/', QtvView.as_view(), name="qtv"),
    ]