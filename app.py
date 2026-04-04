from flask import Flask, request, render_template, jsonify, send_from_directory
import traceback
import json
import os

from ingestion import upload_video
from analyzer import get_viral_clips
from editor import render_clips

app = Flask(__name__)


@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')


# --- THE NEW DELIVERY TRUCK ROUTE ---
@app.route('/download/<filename>', methods=['GET'])
def download_file(filename):
    # This grabs the file from the server and sends it to the user's browser
    return send_from_directory(os.getcwd(), filename, as_attachment=True)


@app.route('/process', methods=['POST'])
def process():
    if 'video_file' not in request.files:
        return jsonify({"error": "No file part found in the request."}), 400

    video = request.files['video_file']

    if video.filename == '':
        return jsonify({"error": "No file selected."}), 400

    file_path = "downloaded_podcast.mp4"
    video.save(file_path)
    print("DEBUG: Video successfully uploaded and saved locally.", flush=True)

    try:
        print("DEBUG: Uploading to Gemini...", flush=True)
        gemini_video = upload_video(file_path)
        if not gemini_video:
            return jsonify({"error": "Failed to upload video to Gemini."}), 500

        print("DEBUG: Analyzing video for viral moments...", flush=True)
        json_result = get_viral_clips(gemini_video)

        print("DEBUG: Rendering final clips...", flush=True)
        render_clips(file_path, json_result)

        # --- THE FIX: Tell the frontend the names of the generated files ---
        clip_data = json.loads(json_result)

        # Create a list of download URLs based on the clip numbers
        download_urls = []
        for clip in clip_data:
            clip_num = clip["clip"]
            download_urls.append({
                "name": f"Viral Clip {clip_num}",
                "url": f"/download/viral_clip_{clip_num}.mp4"
            })

        return jsonify({
            "message": "Clips successfully analyzed and rendered!",
            "downloads": download_urls
        }), 200

    except Exception as e:
        print(f"DEBUG: Pipeline crashed: {e}", flush=True)
        traceback.print_exc()
        return jsonify({"error": str(e)}), 500


if __name__ == '__main__':
    app.run(debug=True, port=5000)