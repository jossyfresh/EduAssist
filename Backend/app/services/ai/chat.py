from typing import Dict
import os
import google.generativeai as genai

# Configure Gemini
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
model = genai.GenerativeModel('gemini-1.5-flash')

async def get_ai_response(context: Dict[str, str]) -> str:
    """
    Get AI response based on video context and user message using Gemini.
    
    Args:
        context: Dictionary containing:
            - video_title: Title of the YouTube video
            - video_url: URL of the YouTube video
            - transcript: Full transcript of the video (optional)
            - user_message: User's question or message
    
    Returns:
        str: AI's response
    """
    system_prompt = """You are an AI assistant helping users understand YouTube videos. 
    You have access to the video's title and URL, and optionally its transcript.
    Even without a transcript, you can make educated guesses about the video's content based on its title.
    Be helpful and engaging in your responses. If you're not sure about something, make an educated guess based on the title.
    Always maintain a helpful and friendly tone."""
    
    # Build the prompt based on available information
    prompt_parts = [
        f"Video Title: {context['video_title']}",
        f"Video URL: {context['video_url']}"
    ]
    
    if context.get('transcript'):
        prompt_parts.append(f"\nTranscript:\n{context['transcript']}")
    
    prompt_parts.extend([
        f"\nUser question: {context['user_message']}",
        "\nPlease provide a helpful response. If you don't have the transcript, make an educated guess based on the video title."
    ])
    
    user_prompt = "\n".join(prompt_parts)
    
    try:
        response = model.generate_content(
            contents=[
                {"role": "user", "parts": [system_prompt + "\n\n" + user_prompt]}
            ],
            generation_config={
                "temperature": 0.7,
                "max_output_tokens": 1000,
            }
        )
        return response.text
    except Exception as e:
        raise Exception(f"Error getting AI response: {str(e)}") 