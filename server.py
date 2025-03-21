from flask import Flask, request, jsonify, send_file
from pytube import YouTube
import os
from flask_cors import CORS
import re

app = Flask(__name__)
CORS(app)

@app.route('/download', methods=['POST'])
def download_video():
    try:
        data = request.get_json()
        url = data.get('url')
        quality = data.get('quality', '720p')
        
        # Convert quality string to resolution
        resolution_map = {
            '1080p': '1080p',
            '720p': '720p',
            '480p': '480p',
            '360p': '360p'
        }
        
        resolution = resolution_map.get(quality, '720p')
        
        # Create YouTube object
        yt = YouTube(url)
        
        # Get the video stream
        video = yt.streams.filter(progressive=True, file_extension='mp4', resolution=resolution).first()
        
        # If requested quality not found, get the best available
        if not video:
            video = yt.streams.filter(progressive=True, file_extension='mp4').order_by('resolution').desc().first()
        
        # Download the video
        if not os.path.exists('downloads'):
            os.makedirs('downloads')
            
        output_path = video.download('downloads')
        filename = os.path.basename(output_path)
        
        return jsonify({
            'success': True,
            'message': 'Video downloaded successfully',
            'filename': filename,
            'title': yt.title
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'message': str(e)
        }), 400

@app.route('/video/<filename>')
def serve_video(filename):
    try:
        return send_file(f'downloads/{filename}', as_attachment=True)
    except Exception as e:
        return jsonify({
            'success': False,
            'message': str(e)
        }), 404

if __name__ == '__main__':
    app.run(port=5000)