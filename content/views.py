from django.shortcuts import render
from django.http import HttpResponse, FileResponse
import os
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from .models import Video
# Create your views here.



def stream_video_480p(request, title):
    video = get_object_or_404(Video, title=title)
    video_path = video.video_file.path.replace('.mp4', '_480p.m3u8')
    return FileResponse(open(video_path, 'rb'))



""" @api_view(['GET']) """
def stream_video_720p(request, title):
    video = get_object_or_404(Video, title=title)
    video_path = video.video_file.path.replace('.mp4', '_720p.m3u8')
    return FileResponse(open(video_path, 'rb'))