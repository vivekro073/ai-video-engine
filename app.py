from flask import Flask, request, render_template, jsonify
import traceback
from ingestion import upload_video
from analyzer import get_viral_clips
from editor import render_clips

app = Flask(__name__)

@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')

@app.route('/process', methods=['POST'])
def process():
    if 'video_file' not in request.files:
        return jsonify({"error": "No file part found in the request."}), 400

    video = request.files['video_file']

    if video.filename == '':
        return jsonify({"error": "No file selected."}), 400

    # Save the file locally
    file_path = "downloaded_podcast.mp4"
    video.save(file_path)
    print("DEBUG: Video successfully uploaded and saved locally.", flush=True)

    try:
        # Step 1: Ingestion
        print("DEBUG: Uploading to Gemini...", flush=True)
        gemini_video = upload_video(file_path)
        if not gemini_video:
            return jsonify({"error": "Failed to upload video to Gemini."}), 500

        # Step 2: Analysis
        print("DEBUG: Analyzing video for viral moments...", flush=True)
        json_result = get_viral_clips(gemini_video)

        # Step 3: Editing
        print("DEBUG: Rendering final clips...", flush=True)
        render_clips(file_path, json_result)

        return jsonify({"message": "Clips successfully analyzed and rendered!"}), 200

    except Exception as e:
        print(f"DEBUG: Pipeline crashed: {e}", flush=True)
        traceback.print_exc()
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, port=5000)