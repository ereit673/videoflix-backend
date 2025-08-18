import os
import shutil
import subprocess


def convert_video_to_hls(source, resolution, output_dir):
    """
    Convert the video to the given resolution and output HLS files.
    """
    res_dir = os.path.join(output_dir, f"{resolution}p")  # add 'p' to folder
    os.makedirs(res_dir, exist_ok=True)

    playlist_path = os.path.join(res_dir, "index.m3u8")
    segment_pattern = os.path.join(res_dir, "%03d.ts")

    subprocess.run([
        "ffmpeg", "-i", source,
        "-vf", f"scale=-2:{resolution}",
        "-c:v", "libx264", "-crf", "23", "-preset", "veryfast",
        "-c:a", "aac", "-strict", "-2",
        "-hls_time", "6",
        "-hls_playlist_type", "vod",
        "-hls_segment_filename", segment_pattern,
        playlist_path
    ], check=True)

    return playlist_path


def generate_master_playlist(output_dir):
    """
    Generate a master.m3u8 file pointing to fixed resolution variants.
    """
    master_path = os.path.join(output_dir, "master.m3u8")
    with open(master_path, "w") as f:
        f.write("#EXTM3U\n#EXT-X-VERSION:3\n")
        f.write(
            "#EXT-X-STREAM-INF:BANDWIDTH=800000,RESOLUTION=854x480\n480p/index.m3u8\n")
        f.write(
            "#EXT-X-STREAM-INF:BANDWIDTH=2800000,RESOLUTION=1280x720\n720p/index.m3u8\n")
        f.write(
            "#EXT-X-STREAM-INF:BANDWIDTH=5000000,RESOLUTION=1920x1080\n1080p/index.m3u8\n")
    return master_path


def cleanup_original(video_path):
    """
    Delete the original uploaded MP4 after HLS conversion is complete.
    """
    if os.path.exists(video_path):
        os.remove(video_path)
        return f"Deleted {video_path}"
    return f"{video_path} not found"


def cleanup_video_and_thumbnail(video_path=None, thumbnail_path=None):
    """
    Deletes the video folder and the thumbnail file.
    """
    # Delete video folder
    if video_path:
        folder_path = os.path.dirname(video_path)
        if os.path.exists(folder_path):
            shutil.rmtree(folder_path)

    # Delete thumbnail
    if thumbnail_path and os.path.exists(thumbnail_path):
        os.remove(thumbnail_path)
