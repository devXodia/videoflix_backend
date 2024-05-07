from django.conf import settings
from django.shortcuts import render
from django.http import HttpResponse, FileResponse
import os
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from django.core.cache.backends.base import DEFAULT_TIMEOUT
from .models import Video
from .serializers import VideoSerializer
from django.views.decorators.cache import cache_page
from django.contrib.auth.decorators import login_required
from django.core.cache import cache

# Create your views here.

CACHE_TTL = getattr(settings, 'CACHE_TTL', DEFAULT_TIMEOUT)


@api_view(['GET'])
def stream_video_480p(request, title):
    if request.method == 'GET': 
        video = get_object_or_404(Video, title=title)
        video_file_name = os.path.basename(video.video_file.path)
        video_path = os.path.join(os.path.dirname(video.video_file.path), '480p', video_file_name.replace('.mp4', '_480p.m3u8'))
        return FileResponse(open(video_path, 'rb'))


@api_view(['GET'])
def stream_video_720p(request, title):
    if request.method == 'GET': 
        video = get_object_or_404(Video, title=title)
        video_path = video.video_file.path.replace('.mp4', '_720p.m3u8')
        return FileResponse(open(video_path, 'rb'))



@cache_page(CACHE_TTL)
@api_view(['GET'])
def movie_list(request):
    cache_key = request.path
    cached_data = cache.get(cache_key)
    if request.method == 'GET':
        if not cached_data:
            videos = Video.objects.all()
            serializer = VideoSerializer(videos, many=True)
            cached_data = serializer.data
            cache.set(cache_key, cached_data, CACHE_TTL)
        else:
            return Response(cached_data, status=status.HTTP_200_OK)
    
        return Response(serializer.data, status=status.HTTP_200_OK)