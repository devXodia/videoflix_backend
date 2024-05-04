from django.db import models
from datetime import date
import os
# Create your models here.

def video_upload_path(instance, filename):
    # Get the filename of the uploaded file
    base_filename = os.path.basename(filename)
    # Use the filename (with extension) to create the directory name
    directory_name = os.path.splitext(base_filename)[0]
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