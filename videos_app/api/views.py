from rest_framework import generics
from rest_framework.permissions import IsAuthenticated

from videos_app.models import Video
from videos_app.api.serializers import VideoSerializer


class VideosListView(generics.ListAPIView):
    """
    View to list all videos.
    """
    queryset = Video.objects.all()
    serializer_class = VideoSerializer
    permission_classes = [IsAuthenticated]
