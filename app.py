from flask import Flask, request, jsonify
import yt_dlp
import os
import json

app = Flask(__name__)

@app.route('/api/download', methods=['POST'])
def download():
    try:
        data = request.json
        url = data.get('url')
        
        if not url:
            return jsonify({'error': 'لا يوجد URL'}), 400
        
        ydl_opts = {
            'format': 'best',
            'quiet': True,
            'no_warnings': True,
        }
        
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=False)
            
            return jsonify({
                'status': 'success',
                'title': info.get('title'),
                'url': url,
                'duration': info.get('duration'),
                'uploader': info.get('uploader')
            })
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/health', methods=['GET'])
def health():
    return jsonify({'status': 'ok'})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.getenv('PORT', 5000)))
