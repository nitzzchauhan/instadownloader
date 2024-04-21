from flask import Flask, request, render_template, send_file,jsonify
import requests
import instaloader
import os
from flask_cors import CORS
from datetime import datetime
app = Flask(__name__)
CORS(app)


def download_instagram_video(url, save_path):
    # Create an instance of instaloader
    L = instaloader.Instaloader()

    # Extract the video ID from the URL
    video_id = url.split('/')[-2]

    try:
        # Get the post details
        post = instaloader.Post.from_shortcode(L.context, video_id)
        
        # Get the video URL
        video_url = post.video_url

        # Download the video
        with open(save_path, 'wb') as f:
            f.write(requests.get(video_url).content)
        
        return f"{save_path}"
    except Exception as e:
        return f"Error occurred: {e}"



@app.route('/', methods=['POST','GET'])
def index():
    if request.method == 'POST':
            global file_path
            current_time = datetime.now().strftime("%H:%M:%S")
            instagram_url = request.form['instagram_url']
            save_path = "new.mp4"
            file_path = download_instagram_video(instagram_url, save_path)
            print(instagram_url,save_path)
            if file_path:
                    return send_file(file_path, as_attachment=True)
    
            else:
                    return "Error downloading video."
   
   
    else:
        return render_template('client.html')
  
@app.route('/d')
def download():
    file_path="new.mp4"
    print(file_path)
    return send_file(file_path, as_attachment=True)
    


if __name__ == '__main__':
    app.run(debug=True)


