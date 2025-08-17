from django.urls import path
from videos_app.api import views


urlpatterns = [
    path('video/', views.VideosListView.as_view(), name="videos-list"),
    path('video/<int:movie_id>/<str:resolution>/index.m3u8',
         views.HLSPlaylistView.as_view(), name="hls-playlist"),
]
