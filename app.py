from flask import Flask, render_template, request
from youtube_transcript_api import YouTubeTranscriptApi, NoTranscriptFound
import requests
import json

# Initialize Flask app
app = Flask(__name__)

# Function to extract video ID from URL
def get_video_id(youtube_url):
    """Extract the video ID from a YouTube URL."""
    try:
        if "?v=" in youtube_url:
            return youtube_url.split("?v=")[1].split("&")[0]
        elif "youtu.be" in youtube_url:
            return youtube_url.split("youtu.be/")[1]
        else:
            return None
    except Exception as e:
        print(f"Error extracting video ID: {e}")
        return None

# Function to fetch transcript from YouTube video
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

# Function to summarize the transcript using Gemini API
def summarize_transcript(transcript_text):
    """Generate a summary of the given transcript using Google Generative AI."""
    GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={GEMINI_API_KEY}"

    data = {
        "contents": [
            {
                "parts": [
                    {"text": f"Give me the summary of the YouTube transcription I provide: {transcript_text}"}
                ]
            }
        ]
    }

    headers = {
        'Content-Type': 'application/json',
    }

    response = requests.post(url, headers=headers, data=json.dumps(data))

    if response.status_code == 200:
        response_data = response.json()
        summary_text = response_data['candidates'][0]['content']['parts'][0]['text']
        return summary_text
    else:
        return f"Error: {response.status_code}, {response.text}"

# Home route
@app.route('/')
def index():
    return render_template('index.html')

# Route to process the form and display result
@app.route('/summarize', methods=['POST'])
def summarize():
    youtube_url = request.form['youtube_url']
    video_id = get_video_id(youtube_url)

    if not video_id:
        return "Invalid YouTube URL."

    transcript = fetch_transcript(video_id)

    if transcript:
        transcript_text = " ".join([entry['text'] for entry in transcript])
        summary = summarize_transcript(transcript_text)
        return render_template('result.html', summary=summary)
    else:
        return "Transcript not found for the given video."

# Run the app
if __name__ == "__main__":
    app.run()
