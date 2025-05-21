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
        self.client = OpenAI(api_key=settings.OPENAI_API_KEY)
        # Load templates
        with open('app/core/content_templates.json', 'r') as f:
            self.templates = json.load(f)
        self.openai_client = openai.OpenAI(api_key=settings.OPENAI_API_KEY)
        genai.configure(api_key=settings.GEMINI_API_KEY)
        self.gemini_model = GenerativeModel('gemini-pro')

    async def generate_content(self, content_type: str, parameters: Dict[str, Any], provider: str = "openai") -> Dict[str, Any]:
        if provider == "openai":
            return await self._generate_with_openai(content_type, parameters)
        elif provider == "gemini":
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
        prompt = f"Generate a {parameters.get('difficulty', 'beginner')} level quiz about {parameters.get('topic')} with {parameters.get('num_questions', 3)} questions. Format as JSON with questions array containing question, options, and correct_answer."
        response = await self.openai_client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}]
        )
        return {"content": response.choices[0].message.content}

    async def _generate_quiz_gemini(self, parameters: Dict[str, Any]) -> Dict[str, Any]:
        prompt = f"Generate a {parameters.get('difficulty', 'beginner')} level quiz about {parameters.get('topic')} with {parameters.get('num_questions', 3)} questions. Format as JSON with questions array containing question, options, and correct_answer."
        response = await self.gemini_model.generate_content(prompt)
        return {"content": response.text}

    async def _generate_summary_openai(self, parameters: Dict[str, Any]) -> Dict[str, Any]:
        prompt = f"Summarize the following text concisely:\n\n{parameters.get('text')}"
        response = await self.openai_client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}]
        )
        return {"content": response.choices[0].message.content}

    async def _generate_summary_gemini(self, parameters: Dict[str, Any]) -> Dict[str, Any]:
        prompt = f"Summarize the following text concisely:\n\n{parameters.get('text')}"
        response = await self.gemini_model.generate_content(prompt)
        return {"content": response.text}

    async def _generate_flashcards_openai(self, parameters: Dict[str, Any]) -> Dict[str, Any]:
        prompt = f"Generate {parameters.get('num_cards', 5)} flashcards about {parameters.get('topic')}. Format as JSON array with front and back fields."
        response = await self.openai_client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}]
        )
        return {"content": response.choices[0].message.content}

    async def _generate_flashcards_gemini(self, parameters: Dict[str, Any]) -> Dict[str, Any]:
        prompt = f"Generate {parameters.get('num_cards', 5)} flashcards about {parameters.get('topic')}. Format as JSON array with front and back fields."
        response = await self.gemini_model.generate_content(prompt)
        return {"content": response.text}

    async def _generate_youtube_suggestions_openai(self, parameters: Dict[str, Any]) -> Dict[str, Any]:
        prompt = f"Suggest {parameters.get('num_suggestions', 5)} YouTube videos about {parameters.get('topic')}. Format as JSON array with title and url fields."
        response = await self.openai_client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}]
        )
        return {"content": response.choices[0].message.content}

    async def _generate_youtube_suggestions_gemini(self, parameters: Dict[str, Any]) -> Dict[str, Any]:
        prompt = f"Suggest {parameters.get('num_suggestions', 5)} YouTube videos about {parameters.get('topic')}. Format as JSON array with title and url fields."
        response = await self.gemini_model.generate_content(prompt)
        return {"content": response.text}

    async def get_youtube_metadata(self, video_url: str) -> Dict[str, str]:
        # This is a stub - in a real implementation, you would use the YouTube API
        return {
            "title": "Sample YouTube Title",
            "description": "Sample YouTube Description",
            "duration": "10:00",
            "thumbnail": "https://example.com/thumbnail.jpg"
        }

    async def generate_quiz(self, topic: str, difficulty: str = "medium") -> Dict[str, Any]:
        prompt = f"Generate a quiz about {topic} with {difficulty} difficulty."
        return await self.generate_content(prompt)

    async def generate_summary(self, text: str) -> Dict[str, Any]:
        prompt = f"Summarize the following text:\n\n{text}"
        return await self.generate_content(prompt) 