import requests
import traceback


def download_video(youtube_url):
    print(f"DEBUG: Contacting Cobalt API for {youtube_url}", flush=True)

    # 1. The API Endpoint and Headers
    api_url = "https://api.cobalt.tools/api/json"
    headers = {
        "Accept": "application/json",
        "Content-Type": "application/json",
    }

    # 2. Our request payload (Asking for 720p to keep processing fast)
    payload = {
        "url": youtube_url,
        "vQuality": "720"
    }

    try:
        # Step A: Ask the API to bypass YouTube and give us a direct link
        response = requests.post(api_url, json=payload, headers=headers)
        response.raise_for_status()  # Check for HTTP errors
        data = response.json()

        # If the API didn't return a URL, something went wrong
        if "url" not in data:
            print(f"DEBUG: API Failed to return video. Response: {data}", flush=True)
            return None

        direct_download_link = data["url"]
        print("DEBUG: API successfully bypassed YouTube! Downloading file...", flush=True)

        # Step B: Download the actual video file to our server
        video_response = requests.get(direct_download_link, stream=True)
        video_response.raise_for_status()

        file_path = "downloaded_podcast.mp4"
        with open(file_path, "wb") as f:
            for chunk in video_response.iter_content(chunk_size=8192):
                f.write(chunk)

        print("DEBUG: Video completely downloaded and ready for AI processing.", flush=True)
        return file_path

    except Exception as e:
        print(f"DEBUG: API Pipeline crashed: {e}", flush=True)
        print("DEBUG: FULL TRACEBACK BELOW:", flush=True)
        traceback.print_exc()
        return None