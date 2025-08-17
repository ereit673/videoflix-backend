import django_rq
import os

from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver

from videos_app.models import Video
from videos_app.api.tasks import convert_video, delete_video_folder


@receiver(post_save, sender=Video)
def video_post_save(sender, instance, created, **kwargs):
    """
    Signal to handle post-save actions for video instances.
    """
    if created:
        # Enqueue a task to process the video file for different resolutions
        queue = django_rq.get_queue('default', autocommit=True)
        queue.enqueue(convert_video, instance.video_file.path, 480)
        queue.enqueue(convert_video, instance.video_file.path, 720)


@receiver(post_delete, sender=Video)
def video_post_delete(sender, instance, **kwargs):
    """
    Signal to handle post-delete actions for video instances.
    """
    # Enqueue a task to delete the video folder
    queue = django_rq.get_queue('default', autocommit=True)
    folder_path = os.path.dirname(instance.video_file.path)
    queue.enqueue(delete_video_folder, folder_path)
