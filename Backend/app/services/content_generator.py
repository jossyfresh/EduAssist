import json
import os
from typing import Dict, Any, Optional
from openai import OpenAI
import yt_dlp
from app.core.config import settings

class ContentGenerator:
    def __init__(self):
        # Initialize OpenAI
        self.client = OpenAI(api_key=settings.OPENAI_API_KEY)
        # Load templates
        with open('app/core/content_templates.json', 'r') as f:
            self.templates = json.load(f)

    async def generate_content(
        self,
        content_type: str,
        parameters: Dict[str, Any],
        provider: str = "openai"
    ) -> Dict[str, Any]:
        if content_type not in self.templates:
            raise ValueError(f"Unsupported content type: {content_type}")
        template = self.templates[content_type]
        prompt = template["prompt"].format(**parameters)
        return await self._generate_with_openai(prompt, content_type)

    async def _generate_with_openai(self, prompt: str, content_type: str) -> Dict[str, Any]:
        try:
            response = await self.client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[{"role": "user", "content": prompt}],
                temperature=0.7
            )
            return self._parse_response(response.choices[0].message.content, content_type)
        except Exception as e:
            raise Exception(f"Error generating content: {str(e)}")

    def _parse_response(self, response: str, content_type: str) -> Dict[str, Any]:
        try:
            return json.loads(response)
        except json.JSONDecodeError:
            if content_type == "quiz":
                return self._format_quiz_response(response)
            elif content_type == "youtube_suggestions":
                return self._format_youtube_suggestions(response)
            else:
                return {"content": response}

    def _format_quiz_response(self, response: str) -> Dict[str, Any]:
        questions = response.split("\n\n")
        formatted_questions = []
        for q in questions:
            if q.strip():
                parts = q.split("\n")
                if len(parts) >= 3:
                    question = parts[0]
                    options = [opt.strip() for opt in parts[1:-1] if opt.strip()]
                    answer = parts[-1].replace("Answer: ", "")
                    formatted_questions.append({
                        "question": question,
                        "options": options,
                        "answer": answer
                    })
        return {"questions": formatted_questions}

    def _format_youtube_suggestions(self, response: str) -> Dict[str, Any]:
        suggestions = []
        current_video = {}
        for line in response.split("\n"):
            if line.startswith("Title:"):
                if current_video:
                    suggestions.append(current_video)
                current_video = {"title": line.replace("Title:", "").strip()}
            elif line.startswith("Channel:"):
                current_video["channel"] = line.replace("Channel:", "").strip()
            elif line.startswith("Duration:"):
                current_video["duration"] = line.replace("Duration:", "").strip()
            elif line.startswith("Relevance:"):
                current_video["relevance"] = line.replace("Relevance:", "").strip()
        if current_video:
            suggestions.append(current_video)
        return {"videos": suggestions}

    async def get_youtube_metadata(self, video_url: str) -> Dict[str, Any]:
        ydl_opts = {
            'quiet': True,
            'no_warnings': True,
            'extract_flat': True
        }
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            try:
                info = ydl.extract_info(video_url, download=False)
                return {
                    "title": info.get('title'),
                    "channel": info.get('uploader'),
                    "duration": info.get('duration'),
                    "thumbnail": info.get('thumbnail'),
                    "description": info.get('description')
                }
            except Exception as e:
                raise ValueError(f"Error fetching YouTube metadata: {str(e)}")

    async def generate_quiz(self, topic: str, difficulty: str = "medium") -> Dict[str, Any]:
        prompt = f"Generate a quiz about {topic} with {difficulty} difficulty."
        return await self.generate_content(prompt)

    async def generate_summary(self, text: str) -> Dict[str, Any]:
        prompt = f"Summarize the following text:\n\n{text}"
        return await self.generate_content(prompt) 