from django.urls import path
from .views import NdtvView, QtvView, HomeView, AmazonView

app_name = 'core'

urlpatterns = [
    path('', HomeView.as_view(), name="home"),
    path('ndtv/', NdtvView.as_view(), name="ndtv"),
    path('amazon/', AmazonView.as_view(), name="amazon"),
    path('qtv/', QtvView.as_view(), name="qtv"),
    ]