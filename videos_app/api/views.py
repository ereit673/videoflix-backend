import os

from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from django.http import FileResponse, Http404
from django.conf import settings
from videos_app.models import Video
from videos_app.api.serializers import VideoSerializer


class VideosListView(generics.ListAPIView):
    """
    View to list all videos.
    """
    queryset = Video.objects.all()
    serializer_class = VideoSerializer
    permission_classes = [IsAuthenticated]


class HLSPlaylistView(generics.RetrieveAPIView):
    """
    View to retrieve the HLS playlist for a specific video and resolution.
    """
    queryset = Video.objects.all()
    lookup_field = "id"
    lookup_url_kwarg = "movie_id"
    permission_classes = [IsAuthenticated]

    def retrieve(self, request, *args, **kwargs):
        """
        Retrieve the HLS playlist for a specific video and resolution.
        """
        video = self.get_object()
        resolution = kwargs.get("resolution")
        playlist_path = os.path.join(
            settings.MEDIA_ROOT,
            'videos',
            str(video.uuid),
            resolution,
            'index.m3u8'
        )

        if not os.path.exists(playlist_path):
            raise Http404("Playlist not found")

        return FileResponse(open(playlist_path, 'rb'), content_type='application/vnd.apple.mpegurl')


class HLSSegmentView(generics.RetrieveAPIView):
    """
    View to retrieve a specific HLS segment for a video.
    """
    queryset = Video.objects.all()
    lookup_field = "id"
    lookup_url_kwarg = "movie_id"
    permission_classes = [IsAuthenticated]

    def retrieve(self, request, *args, **kwargs):
        """
        Retrieve a specific HLS segment for a video.
        """
        video = self.get_object()
        resolution = kwargs.get("resolution")
        segment = kwargs.get("segment")
        segment_path = os.path.join(
            settings.MEDIA_ROOT,
            'videos',
            str(video.uuid),
            resolution,
            segment
        )

        if not os.path.exists(segment_path):
            raise Http404("Segment not found")

        return FileResponse(open(segment_path, 'rb'), content_type='video/MP2T')
