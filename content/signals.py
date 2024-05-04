from .models import Video
from django.dispatch import receiver
from django.db.models.signals import post_save, post_delete
import os
import subprocess


@receiver(post_save, sender=Video)
def video_post_save(sender, instance, created, **kwargs):
    """
    Action after the video has been uploaded.
    """
    if created:  # Only execute if the video is newly created
        try:
            input_path = instance.video_file.path
            output_directory_480p = os.path.join(os.path.dirname(input_path), '480p')
            output_directory_720p = os.path.join(os.path.dirname(input_path), '720p')

            # Ensure the directories exist
            os.makedirs(output_directory_480p, exist_ok=True)
            os.makedirs(output_directory_720p, exist_ok=True)

            # Define output paths for 480p and 720p HLS streams
            output_path_480p = os.path.join(output_directory_480p, os.path.basename(input_path).replace('.mp4', '_480p.m3u8'))
            output_path_720p = os.path.join(output_directory_720p, os.path.basename(input_path).replace('.mp4', '_720p.m3u8'))


            # Convert to 480p HLS
            command_480p = ['ffmpeg', '-i', input_path, '-vf', 'scale=-2:480', '-c:v', 'libx264', '-preset', 'medium', '-crf', '23', '-c:a', 'aac', '-b:a', '128k', '-hls_time', '10', '-hls_list_size', '0', '-f', 'hls', output_path_480p]
            subprocess.run(command_480p, check=True)

            # Convert to 720p HLS
            command_720p = ['ffmpeg', '-i', input_path, '-vf', 'scale=-2:720', '-c:v', 'libx264', '-preset', 'medium', '-crf', '23', '-c:a', 'aac', '-b:a', '128k', '-hls_time', '10', '-hls_list_size', '0', '-f', 'hls', output_path_720p]
            subprocess.run(command_720p, check=True)

            # Update the video instance with the paths to the HLS streams
            instance.hls_480p.path = output_path_480p
            instance.hls_720p.path = output_path_720p
            instance.save()

        except Exception as e:
            print(f"Error converting video: {e}")




@receiver(post_delete, sender = Video)
def video_post_delete(sender, instance, **kwargs):
    """
    Delets file from filesystem when corresponding `Video` object is deleted.
    """
    if instance.video_file:
        if os.path.isfile(instance.video_file.path):
            os.remove(instance.video_file.path)

            
