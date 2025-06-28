from flask import Flask, render_template,redirect,url_for,request,jsonify
from yt_dlp import YoutubeDL
from pathlib import Path

app = Flask(__name__)


progress_status = {'status': '','percentage': ''}
@app.route('/', methods=['GET', 'POST'])
def download_video():
    status=""
    video_url = request.form.get('video_url')
    download_options = {
        'format': 'bestvideo[height=1080]+bestaudio',
        'merge_output_format': 'mp4',
        'outtmpl': 'downloads/%(title)s.%(ext)s',  # Output folder and filename
        'quiet': True,
        'retries': 1,
    }

    if video_url and request.method == 'POST':
        status = "downloading.."
        downloads_path = str(Path.home() / "Downloads")
        try:
            with YoutubeDL(download_options) as video:
                video.download([video_url])
            status = "Download completed successfully!"
        except Exception as e:
            print(f"Error downloading video: {e}")
            return render_template('vid.html', error=str(e))
        return redirect(url_for('download_video'))

    return render_template('vid.html',status=status)

@app.route('/progress')
def get_progress():
    return jsonify(progress_status)
 
if __name__ == '__main__':
    app.run(debug=True)