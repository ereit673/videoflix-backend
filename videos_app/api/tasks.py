import os
import subprocess


def convert_video(source, resolution):
    """
    Convert the video to the given resolution (e.g., 480 or 720).
    """
    base, ext = os.path.splitext(source)
    output_path = f"{base}_{resolution}p.mp4"
    subprocess.run([
        "ffmpeg", "-i", source, "-s", f"hd{resolution}", "-c:v", "libx264", "-crf", "23",
        "-c:a", "aac", "-strict", "-2", output_path
    ])


def delete_video_folder(folder_path):
    """
    Delete the video folder at the given path.
    """
    print(folder_path)
    if os.path.exists(folder_path):
        for root, dirs, files in os.walk(folder_path, topdown=False):
            for name in files:
                os.remove(os.path.join(root, name))
            for name in dirs:
                os.rmdir(os.path.join(root, name))
        os.rmdir(folder_path)
