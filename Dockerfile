# Use an official Python runtime as a parent image
FROM python:3.10-slim

# Set the working directory in the container
WORKDIR /app

# Copy the requirements file and install dependencies
# We install ffmpeg here because video processing usually requires it!
RUN apt-get update && apt-get install -y ffmpeg
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of your application code
COPY . .

# Hugging Face STRICTLY requires your app to run on port 7860
EXPOSE 7860

# Run the Flask app on port 7860
CMD ["flask", "run", "--host=0.0.0.0", "--port=7860"]