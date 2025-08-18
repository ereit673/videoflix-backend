import uuid

from django.db import models


def video_file_path(instance, filename):
    """
    Generates the file path for the video file upload.
    """
    # Save videos in media/videos/<id>/<filename>
    return f'videos/{instance.uuid}/{filename}'


class Video(models.Model):
    uuid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    title = models.CharField(max_length=255)
    description = models.TextField()
    thumbnail_url = models.ImageField(upload_to='thumbnails/')
    category = models.CharField(max_length=50)
    video_file = models.FileField(
        upload_to=video_file_path, blank=True, null=True)

    def __str__(self):
        return f"{self.title} in category {self.category}"
