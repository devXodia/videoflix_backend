from django.shortcuts import render
from django.http import HttpResponse, FileResponse
import os
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
# Create your views here.

@api_view(['GET'])
def stream_video(request, video_filename):
    if request.method == 'GET':
        video_path = os.path.join('videos', video_filename)
    
    # Check if the file exists
    if not os.path.exists(video_path):
        return HttpResponse("Video not found", status=404)
    
    # Open the file and stream it using FileResponse
    try:
        with open(video_path, 'rb') as video_file:
            response = FileResponse(video_file)
            return response
    except Exception as e:
        return HttpResponse(str(e), status=500)
