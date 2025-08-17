from django.db import models


def video_file_path(instance, filename):
    # Save every video to media/videos/<id>/<original_filename>
    return f'videos/{instance.id}/{filename}'


class Video(models.Model):
    CATEGORY_CHOICES = [
        ('horror', 'Horror'),
        ('action', 'Action'),
        ('drama', 'Drama'),
        ('animals', 'Animals'),
        ('documentary', 'Documentary')
    ]
    created_at = models.DateTimeField(auto_now_add=True)
    title = models.CharField(max_length=255, blank=False)
    description = models.TextField()
    thumbnail_url = models.ImageField(
        upload_to='thumbnails/', blank=False, null=False)
    category = models.CharField(
        max_length=50, choices=CATEGORY_CHOICES)
    video_file = models.FileField(
        upload_to=video_file_path, blank=True, null=True)

    def __str__(self):
        """
        Returns a string representation of the Video instance.
        """
        return f"{self.title} in category {self.category}"
