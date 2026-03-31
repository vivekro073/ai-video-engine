from ingestion import upload_video
from analyzer import get_viral_clips
from editor import render_clips
from youtube_fetcher import download_video


def process_video(targeted_video_path):

    uploaded_file = upload_video(targeted_video_path)
    if uploaded_file is None:
        return
    ai_jason_data = get_viral_clips(uploaded_file)
    render_clips(targeted_video_path, ai_jason_data)


if __name__ == "__main__":
    print("Initiating YouTube Download...")
    downloaded_file_path = download_video("https://www.youtube.com/watch?v=z99W_73dTT8")
    print(f"Download complete. Processing {downloaded_file_path}...")
    result = process_video(downloaded_file_path)
