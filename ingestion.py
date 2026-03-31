import time
import os
from dotenv import load_dotenv
from google import genai




load_dotenv()

client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))


def upload_video(video):
    video_file = client.files.upload(file=video)

    while True:
        file_info = client.files.get(name=video_file.name)
        if file_info.state == "ACTIVE":
            print("Video uploaded")
            return video_file
        elif file_info.state == "FAILED":
            print("Video failed")
            return None
        time.sleep(5)


# if __name__ == "__main__":
#     result = upload_video("videoplayback.mp4")
#     print(result.uri)