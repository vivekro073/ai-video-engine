import yt_dlp

ydl_opts = {
    'format': 'b[ext=mp4]',
    'cookiefile': 'cookies.txt',
    'outtmpl': 'downloaded_podcast.%(ext)s',
    'quiet': True,          # Silences standard output
    'no_warnings': True     # Silences the JS runtime warning
}


def download_video(youtube_url):
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([youtube_url])

        return "downloaded_podcast.mp4"