import os
import base64
import yt_dlp
import traceback  # <--- Added to stop silent crashes


def _setup_secure_cookies():
    if "YOUTUBE_COOKIES" not in os.environ:
        print("DEBUG: CRITICAL ERROR - YOUTUBE_COOKIES secret not found!", flush=True)
        return

    try:
        encoded_string = os.environ["YOUTUBE_COOKIES"]
        decoded_bytes = base64.b64decode(encoded_string)
        decoded_text = decoded_bytes.decode('utf-8')

        with open("cookies.txt", "w") as f:
            f.write(decoded_text)

        print("DEBUG: Cookie file successfully decoded and written.", flush=True)
    except Exception as e:
        print(f"DEBUG: CRITICAL ERROR decoding cookies: {e}", flush=True)


def download_video(youtube_url):
    _setup_secure_cookies()

    # 100% clean options. No impersonation hacks.
    ydl_opts = {
        'format': 'b[ext=mp4]',
        'cookiefile': 'cookies.txt',
        'outtmpl': 'downloaded_podcast.%(ext)s',
        'quiet': True,
        'no_warnings': True,
        'extractor_args': {
            'youtube': ['player_client=android']
        }
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([youtube_url])
        return "downloaded_podcast.mp4"
    except Exception as e:
        print(f"DEBUG: Download failed: {e}", flush=True)
        print("DEBUG: FULL TRACEBACK BELOW:", flush=True)
        traceback.print_exc()  # <--- This will print the exact reason it crashed
        return None