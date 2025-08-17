import django_rq
import os

from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver

from videos_app.models import Video
from videos_app.api.tasks import convert_video_to_hls, generate_master_playlist, cleanup_original, cleanup_video_and_thumbnail


@receiver(post_save, sender=Video)
def video_post_save(sender, instance, created, **kwargs):
    """
    When a new video is uploaded, enqueue HLS conversion tasks and cleanup.
    """
    if created:
        queue = django_rq.get_queue('default', autocommit=True)

        video_path = instance.video_file.path
        output_dir = os.path.dirname(video_path)

        # Step 1: enqueue HLS conversion jobs
        job_480 = queue.enqueue(convert_video_to_hls,
                                video_path, 480, output_dir)
        job_720 = queue.enqueue(convert_video_to_hls,
                                video_path, 720, output_dir)
        job_1080 = queue.enqueue(convert_video_to_hls,
                                 video_path, 1080, output_dir)

        # Step 2: enqueue master playlist job, depends on all conversions
        master_job = queue.enqueue(
            generate_master_playlist, output_dir,
            depends_on=[job_480, job_720, job_1080]
        )

        # Step 3: enqueue cleanup, depends on master playlist
        queue.enqueue(cleanup_original, video_path, depends_on=master_job)


@receiver(post_delete, sender=Video)
def video_post_delete(sender, instance, **kwargs):
    """
    Enqueue a task to delete the video folder and thumbnail asynchronously.
    """
    queue = django_rq.get_queue('default', autocommit=True)
    queue.enqueue(
        cleanup_video_and_thumbnail,
        video_path=instance.video_file.path if instance.video_file else None,
        thumbnail_path=instance.thumbnail_url.path if instance.thumbnail_url else None
    )
