from flask import Flask, request, jsonify, render_template
from youtube_fetcher import download_video
from ingestion import upload_video
from analyzer import get_viral_clips
from editor import render_clips
import os



if "YOUTUBE_COOKIES" in os.environ:
    with open("cookies.txt", "w") as f:
        f.write(os.environ["YOUTUBE_COOKIES"])


app = Flask(__name__)

@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')


@app.route('/process', methods=['POST'])
def process():
    data = request.json
    youtube_url = data.get('url')

    if not youtube_url:
        return jsonify({"error": "No URL provided"}), 400

    try:
        print(f"Executing Pipeline for: {youtube_url}")

        downloaded_file = download_video(youtube_url)
        print("1. Download Complete.")

        uploaded_file = upload_video(downloaded_file)
        if uploaded_file is None:
            return jsonify({"error": "Failed to upload video to Gemini"}), 500
        print("2. Gemini Ingestion Complete.")

        ai_json_data = get_viral_clips(uploaded_file)
        print("3. Multimodal Analysis Complete.")

        render_clips(downloaded_file, ai_json_data)
        print("4. Local Rendering Complete.")

        return jsonify({"status": "success", "message": "Clips physically rendered to your project folder!"}), 200

    except Exception as e:
        print(f"PIPELINE FAILURE: {str(e)}")
        return jsonify({"error": str(e)}), 500


if __name__ == '__main__':
    app.run(debug=True, port=5000)