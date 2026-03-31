import json
from moviepy import VideoFileClip

def render_clips(video_path, json_string):

    clip_data = json.loads(json_string)

    master_video = VideoFileClip(video_path)

    for clip in clip_data:
        start = clip["start_time"]
        end = clip["end_time"]
        clip_num = clip["clip"]

        subclip = master_video.subclipped(start, end)

        print(f"Rendering Clip {clip_num}...")
        subclip.write_videofile(f"viral_clip_{clip_num}.mp4", codec="libx264", audio_codec="aac")

    print("All rendering complete.")