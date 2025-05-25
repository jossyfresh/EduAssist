import json
import os
from typing import Dict, Any, Optional, List
from openai import OpenAI
import yt_dlp
from app.core.config import settings
import openai
from google.generativeai import GenerativeModel
import google.generativeai as genai

class ContentGenerator:
    def __init__(self):
        # Initialize OpenAI
        self.client = None
        self.openai_client = None
        self.gemini_model = None
        
        # Load templates
        template_path = os.path.join(os.path.dirname(__file__), '..', 'core', 'content_templates.json')
        with open(os.path.abspath(template_path), 'r') as f:
            self.templates = json.load(f)
            
        # Initialize API clients if keys are available
        if settings.OPENAI_API_KEY:
            self.client = OpenAI(api_key=settings.OPENAI_API_KEY)
            self.openai_client = openai.OpenAI(api_key=settings.OPENAI_API_KEY)
            
        if settings.GEMINI_API_KEY:
            genai.configure(api_key=settings.GEMINI_API_KEY)
            self.gemini_model = GenerativeModel('gemini-pro')

    async def generate_content(self, content_type: str, parameters: Dict[str, Any], provider: str = "openai") -> Dict[str, Any]:
        if provider == "openai":
            if not self.openai_client:
                return {"content": "OpenAI API key not configured"}
            return await self._generate_with_openai(content_type, parameters)
        elif provider == "gemini":
            if not self.gemini_model:
                return {"content": "Gemini API key not configured"}
            return await self._generate_with_gemini(content_type, parameters)
        else:
            raise ValueError(f"Unsupported provider: {provider}")

    async def _generate_with_openai(self, content_type: str, parameters: Dict[str, Any]) -> Dict[str, Any]:
        if content_type == "quiz":
            return await self._generate_quiz_openai(parameters)
        elif content_type == "summary":
            return await self._generate_summary_openai(parameters)
        elif content_type == "flashcard":
            return await self._generate_flashcards_openai(parameters)
        elif content_type == "youtube_suggestions":
            return await self._generate_youtube_suggestions_openai(parameters)
        else:
            raise ValueError(f"Unsupported content type: {content_type}")

    async def _generate_with_gemini(self, content_type: str, parameters: Dict[str, Any]) -> Dict[str, Any]:
        if content_type == "quiz":
            return await self._generate_quiz_gemini(parameters)
        elif content_type == "summary":
            return await self._generate_summary_gemini(parameters)
        elif content_type == "flashcard":
            return await self._generate_flashcards_gemini(parameters)
        elif content_type == "youtube_suggestions":
            return await self._generate_youtube_suggestions_gemini(parameters)
        else:
            raise ValueError(f"Unsupported content type: {content_type}")

    async def _generate_quiz_openai(self, parameters: Dict[str, Any]) -> Dict[str, Any]:
        if not self.openai_client:
            return {"content": "OpenAI API key not configured"}
        prompt = f"Generate a {parameters.get('difficulty', 'beginner')} level quiz about {parameters.get('topic')} with {parameters.get('num_questions', 3)} questions. Format as JSON with questions array containing question, options, and correct_answer."
        try:
            response = await self.openai_client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[{"role": "user", "content": prompt}]
            )
            return {"content": response.choices[0].message.content}
        except Exception as e:
            return {"content": f"Error generating quiz: {str(e)}"}

    async def _generate_quiz_gemini(self, parameters: Dict[str, Any]) -> Dict[str, Any]:
        if not self.gemini_model:
            return {"content": "Gemini API key not configured"}
        prompt = f"Generate a {parameters.get('difficulty', 'beginner')} level quiz about {parameters.get('topic')} with {parameters.get('num_questions', 3)} questions. Format as JSON with questions array containing question, options, and correct_answer."
        try:
            response = await self.gemini_model.generate_content(prompt)
            return {"content": response.text}
        except Exception as e:
            return {"content": f"Error generating quiz: {str(e)}"}

    async def _generate_summary_openai(self, parameters: Dict[str, Any]) -> Dict[str, Any]:
        if not self.openai_client:
            return {"content": "OpenAI API key not configured"}
        prompt = f"Summarize the following text concisely:\n\n{parameters.get('text')}"
        try:
            response = await self.openai_client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[{"role": "user", "content": prompt}]
            )
            return {"content": response.choices[0].message.content}
        except Exception as e:
            return {"content": f"Error generating summary: {str(e)}"}

    async def _generate_summary_gemini(self, parameters: Dict[str, Any]) -> Dict[str, Any]:
        if not self.gemini_model:
            return {"content": "Gemini API key not configured"}
        prompt = f"Summarize the following text concisely:\n\n{parameters.get('text')}"
        try:
            response = await self.gemini_model.generate_content(prompt)
            return {"content": response.text}
        except Exception as e:
            return {"content": f"Error generating summary: {str(e)}"}

    async def _generate_flashcards_openai(self, parameters: Dict[str, Any]) -> Dict[str, Any]:
        if not self.openai_client:
            return {"content": "OpenAI API key not configured"}
        prompt = f"Generate {parameters.get('num_cards', 5)} flashcards about {parameters.get('topic')}. Format as JSON array with front and back fields."
        try:
            response = await self.openai_client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[{"role": "user", "content": prompt}]
            )
            return {"content": response.choices[0].message.content}
        except Exception as e:
            return {"content": f"Error generating flashcards: {str(e)}"}

    async def _generate_flashcards_gemini(self, parameters: Dict[str, Any]) -> Dict[str, Any]:
        if not self.gemini_model:
            return {"content": "Gemini API key not configured"}
        prompt = f"Generate {parameters.get('num_cards', 5)} flashcards about {parameters.get('topic')}. Format as JSON array with front and back fields."
        try:
            response = await self.gemini_model.generate_content(prompt)
            return {"content": response.text}
        except Exception as e:
            return {"content": f"Error generating flashcards: {str(e)}"}

    async def _generate_youtube_suggestions_openai(self, parameters: Dict[str, Any]) -> Dict[str, Any]:
        if not self.openai_client:
            return {"content": "OpenAI API key not configured"}
        prompt = f"Suggest {parameters.get('num_suggestions', 5)} YouTube videos about {parameters.get('topic')}. Format as JSON array with title and url fields."
        try:
            response = await self.openai_client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[{"role": "user", "content": prompt}]
            )
            return {"content": response.choices[0].message.content}
        except Exception as e:
            return {"content": f"Error generating YouTube suggestions: {str(e)}"}

    async def _generate_youtube_suggestions_gemini(self, parameters: Dict[str, Any]) -> Dict[str, Any]:
        if not self.gemini_model:
            return {"content": "Gemini API key not configured"}
        prompt = f"Suggest {parameters.get('num_suggestions', 5)} YouTube videos about {parameters.get('topic')}. Format as JSON array with title and url fields."
        try:
            response = await self.gemini_model.generate_content(prompt)
            return {"content": response.text}
        except Exception as e:
            return {"content": f"Error generating YouTube suggestions: {str(e)}"}

    async def get_youtube_metadata(self, video_url: str) -> Dict[str, str]:
        try:
            ydl_opts = {
                'quiet': True,
                'no_warnings': True,
                'extract_flat': True
            }
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(video_url, download=False)
                return {
                    "title": info.get('title', ''),
                    "description": info.get('description', ''),
                    "duration": str(info.get('duration', 0)),
                    "thumbnail": info.get('thumbnail', '')
                }
        except Exception as e:
            return {
                "title": "Error fetching metadata",
                "description": str(e),
                "duration": "0",
                "thumbnail": ""
            }

    async def extract_youtube_transcript(self, video_url: str) -> Dict[str, str]:
        """
        Download a YouTube video using yt-dlp and extract its transcript using OpenAI Whisper (or another ASR model).
        Returns a dict with transcript and metadata.
        """
        import tempfile
        import subprocess
        import shutil
        transcript = ""
        temp_dir = tempfile.mkdtemp()
        try:
            # Download audio only
            audio_path = os.path.join(temp_dir, "audio.%(ext)s")
            ydl_opts = {
                'format': 'bestaudio/best',
                'outtmpl': audio_path,
                'quiet': True,
                'no_warnings': True,
            }
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(video_url, download=True)
                downloaded_path = ydl.prepare_filename(info).replace(".webm", ".m4a").replace(".mp4", ".m4a")
                # Try to find the downloaded file
                for ext in [".m4a", ".webm", ".mp3", ".wav"]:
                    candidate = ydl.prepare_filename(info).rsplit(".", 1)[0] + ext
                    if os.path.exists(candidate):
                        downloaded_path = candidate
                        break
            # Transcribe using OpenAI Whisper (or another ASR model)
            import openai
            with open(downloaded_path, "rb") as audio_file:
                transcript_response = openai.Audio.transcribe(
                    "whisper-1", audio_file, api_key=settings.OPENAI_API_KEY
                )
                transcript = transcript_response["text"]
            return {
                "transcript": transcript,
                "title": info.get("title", ""),
                "description": info.get("description", ""),
                "duration": str(info.get("duration", 0)),
                "thumbnail": info.get("thumbnail", "")
            }
        except Exception as e:
            return {"error": str(e)}
        finally:
            shutil.rmtree(temp_dir, ignore_errors=True)

    async def generate_quiz(self, topic: str, difficulty: str = "medium") -> Dict[str, Any]:
        prompt = f"Generate a quiz about {topic} with {difficulty} difficulty."
        return await self.generate_content(prompt)

    async def generate_summary(self, text: str) -> Dict[str, Any]:
        prompt = f"Summarize the following text:\n\n{text}"
        return await self.generate_content(prompt)

    def generate_learning_path_outline(self, course_title: str, course_description: str) -> dict:
        """
        Generate a learning path outline with detailed structure for each chapter.
        Returns a dict containing materialTitle, materialDescription, progress, and chapters array.
        Each chapter contains title, description, estimatedDuration, keyConcepts, and resources.
        """
        prompt = (
            f"Given the course title: '{course_title}' and description: '{course_description}', "
            f"generate a JSON object with the following structure: "
            f"{{'materialTitle': <string>, 'materialDescription': <string>, 'progress': 0, 'chapters': ["
            f"{{'title': <string>, 'description': <string>, 'estimatedDuration': <string>, "
            f"'keyConcepts': [<string>], 'resources': [{{'type': <string>, 'title': <string>, 'url': <string>}}]}}, ...]}}. "
            f"Each chapter should be a key step for a beginner, with estimatedDuration in hours, "
            f"keyConcepts as an array of main topics, and resources as an array of learning materials."
        )
        response = self.openai_client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}]
        )
        import json as _json
        try:
            return _json.loads(response.choices[0].message.content)
        except Exception:
            return {
                "materialTitle": course_title,
                "materialDescription": course_description,
                "progress": 0,
                "chapters": []
            }