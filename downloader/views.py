# from django.shortcuts import render

# # Create your views here.
# from django.shortcuts import render

# def index(request):
#     return render(request, 'index.html')
import os
from django.http import HttpResponse
from django.shortcuts import render
from pytube import YouTube
import requests
from moviepy.editor import *
def home(request):
    return HttpResponse("Welcome to the Ytmusic_download app!")
def index(request):
    return render(request, 'index.html')

def convert_mp4_to_mp3(input_path, output_path):
    video = VideoFileClip(input_path)
    audio = video.audio
    audio.write_audiofile(output_path)
    audio.close()
    video.close()

def download_video(request):
    if request.method == 'POST':
        video_url = request.POST.get('video_url')
        format_option = request.POST.get('format')

        try:
            yt = YouTube(video_url)
            stream = yt.streams.get_highest_resolution()

            if format_option == 'mp4':
                video_data = requests.get(stream.url).content
                response = HttpResponse(video_data, content_type=stream.mime_type)
                response['Content-Disposition'] = f'attachment; filename="{yt.title}.mp4"'
            elif format_option == 'mp3':
                # Download the video as MP4
                video_path = f"{yt.title}.mp4"
                video_data = requests.get(stream.url).content
                with open(video_path, 'wb') as f:
                    f.write(video_data)

                # Convert MP4 to MP3
                audio_path = f"{yt.title}.mp3"
                convert_mp4_to_mp3(video_path, audio_path)

                # Read the MP3 audio and create the response
                audio_data = open(audio_path, 'rb').read()
                response = HttpResponse(audio_data, content_type='audio/mpeg')
                response['Content-Disposition'] = f'attachment; filename="{yt.title}.mp3"'

                # Remove the temporary files
                os.remove(video_path)
                os.remove(audio_path)

            return response
        except Exception as e:
            return HttpResponse(f"Error: {e}")
    else:
        return HttpResponse("Invalid Request")
