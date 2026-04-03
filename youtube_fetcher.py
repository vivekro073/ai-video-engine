import yt_dlp

ydl_opts = {
    'format': 'b[ext=mp4]',
    'cookiefile': 'cookies.txt',
    'outtmpl': 'downloaded_podcast.%(ext)s',
    'quiet': True,
    'no_warnings': True,
    'extractor_args': {
        'youtube': ['player_client=android']
}


def download_video(youtube_url):
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([youtube_url])
        return "downloaded_podcast.mp4"
