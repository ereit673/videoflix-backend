from rest_framework import serializers

from videos_app.models import Video


class VideoSerializer(serializers.ModelSerializer):
    """
    Serializer for the Video model.
    """
    class Meta:
        model = Video
        fields = [
            'id',
            'created_at',
            'title',
            'description',
            'thumbnail_url',
            'category'
        ]
