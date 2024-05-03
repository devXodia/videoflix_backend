from django.db import models
from datetime import date
import os
# Create your models here.


def video_upload_path(instance, filename):
    # Use the title field of the instance to create the directory name
    directory_name = instance.title.replace(' ', '_')
    # Join the directory name and filename to create the full upload path
    return os.path.join('videos', directory_name, filename)

class Video(models.Model):
    created_at = models.DateField(default=date.today)
    title = models.CharField(max_length=80)
    description = models.CharField(max_length=500)
    video_file = models.FileField(upload_to=video_upload_path, blank=True, null=True)
    genre = models.CharField(max_length=20, default='')
    img_file = models.FileField(upload_to='preview', blank=True, null=True)

    def __str__(self):
        return self.title