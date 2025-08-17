import re

from django.db import models


def clean_filename(title):
    return re.sub(r'[^a-zA-Z0-9_]+', '_', title)


def video_file_path(instance, filename):
    title = clean_filename(instance.title)[:50]
    return f'videos/{title}/{filename}'


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
