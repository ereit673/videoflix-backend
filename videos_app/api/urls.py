from django.urls import path
from videos_app.api import views


urlpatterns = [
    path('video/', views.VideosListView.as_view(), name="videos-list")
]
