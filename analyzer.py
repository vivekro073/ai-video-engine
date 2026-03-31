import os
from dotenv import load_dotenv
from google import genai


def get_viral_clips(video_file):
    load_dotenv()
    client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

    prompt = """
    You are a master short-form video editor specializing in viral TikToks, Instagram Reels, and YouTube Shorts. 
    Your objective is to watch the provided video and identify the 2 most engaging, high-retention moments. 
    
    Look for moments that have:
    1. A strong hook or sudden shift in energy.
    2. A complete, cohesive thought or funny reaction.
    3. High potential for audience retention.
    
    CRITICAL INSTRUCTIONS FOR OUTPUT:
    You are communicating directly with a Python script, not a human. 
    You MUST return ONLY a raw, valid JSON array. 
    Do NOT wrap the JSON in markdown code blocks (e.g., do not use ```json). 
    Do NOT include any conversational text, greetings, or explanations before or after the array.
    
    Use this exact schema:
    [
      {
        "clip": 1,
        "start_time": 0,
        "end_time": 5,
        "reasoning": "Brief 1-sentence explanation of why this clip is engaging."
      },
      {
        "clip": 2,
        "start_time": 15,
        "end_time": 22,
        "reasoning": "Brief 1-sentence explanation of why this clip is engaging."
      }
    ]
    """

    response = client.models.generate_content(model='gemini-2.5-flash', contents=[video_file, prompt])

    return response.text