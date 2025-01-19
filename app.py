from youtube_transcript_api import YouTubeTranscriptApi, NoTranscriptFound
import google.generativeai as genai
import requests
import os
import json
# Configure your API key

def get_video_id(youtube_url):
    """Extract the video ID from a YouTube URL."""
    try:
        if "?v=" in youtube_url:
            return youtube_url.split("?v=")[1].split("&")[0]
        elif "youtu.be" in youtube_url:
            return youtube_url.split("youtu.be/")[1]
        else:
            print("Invalid YouTube URL format.")
            return None
    except Exception as e:
        print(f"Error extracting video ID: {e}")
        return None

def fetch_transcript(video_id):
    """Fetch the transcript for a YouTube video."""
    try:
        # Attempt to fetch the transcript in English
        transcript = YouTubeTranscriptApi.get_transcript(video_id, languages=['en'])
        return transcript
    except NoTranscriptFound:
        print("Transcript not found for the given video.")
        return None
    except Exception as e:
        print(f"An error occurred while fetching the transcript: {e}")
        return None


        # Create an instance of the GenerativeModel
     
        
        # Return the text of the generated content
      

if __name__ == "__main__":
    youtube_url = input("Enter the YouTube video URL: ")
    video_id = get_video_id(youtube_url)

    if not video_id:
        print("Invalid YouTube URL.")
    else:
        transcript = fetch_transcript(video_id)
        if transcript:
            print("\nTranscript:")
            # Convert transcript to a single string
            transcript_text = " ".join([entry['text'] for entry in transcript])
            print(transcript_text)

            print("this is the summary")

            # Summarize the transcript

import json

# Set your API key and endpoint
GEMINI_API_KEY = 'AIzaSyD_xFrv1YGDJgEJlxkQ3dtxmLgKZJpskGI'
url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={GEMINI_API_KEY}"

# Prepare the data payload
data = {
    "contents": [
        {
            "parts": [
                {"text": f"give me the summary of the YouTube transcription I provide: {transcript_text}"}
            ]
        }
    ]
}

# Set the headers
headers = {
    'Content-Type': 'application/json',
}

# Make the POST request
response = requests.post(url, headers=headers, data=json.dumps(data))

# Check the response
if response.status_code == 200:
    response_data = response.json()
    # Extract and print the summary text
    summary_text = response_data['candidates'][0]['content']['parts'][0]['text']
    print(summary_text)
else:
    print(f"Error: {response.status_code}, {response.text}")