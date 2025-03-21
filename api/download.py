from http.server import BaseHTTPRequestHandler
from pytube import YouTube
import json
import os
from urllib.parse import parse_qs

class handler(BaseHTTPRequestHandler):
    def do_OPTIONS(self):
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()

    def do_POST(self):
        try:
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            data = json.loads(post_data.decode('utf-8'))
            
            url = data.get('url')
            quality = data.get('quality', '720p')
            
            # Create YouTube object
            yt = YouTube(url)
            
            # Get video info
            video_info = {
                'title': yt.title,
                'thumbnail': yt.thumbnail_url,
                'duration': yt.length,
                'author': yt.author,
                'views': yt.views,
                'streams': []
            }
            
            # Get available streams
            streams = yt.streams.filter(progressive=True, file_extension='mp4')
            for stream in streams:
                video_info['streams'].append({
                    'itag': stream.itag,
                    'resolution': stream.resolution,
                    'filesize': stream.filesize,
                    'url': stream.url
                })
            
            # Send response
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            
            response = {
                'success': True,
                'data': video_info
            }
            
            self.wfile.write(json.dumps(response).encode())
            
        except Exception as e:
            self.send_response(500)
            self.send_header('Content-type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            
            error_response = {
                'success': False,
                'error': str(e)
            }
            
            self.wfile.write(json.dumps(error_response).encode())

    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()
        
        response = {
            'status': 'API is running'
        }
        
        self.wfile.write(json.dumps(response).encode())