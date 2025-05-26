import json
import os
from typing import Dict, Any, Optional, List
from openai import OpenAI
import yt_dlp
from app.core.config import settings
import openai
from google.generativeai import GenerativeModel
import google.generativeai as genai
from fastapi import HTTPException
import logging

logger = logging.getLogger(__name__)

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
            try:
                self.openai_client = OpenAI(
                    api_key=settings.OPENAI_API_KEY,
                    timeout=30.0,  # 30 second timeout
                    max_retries=3  # Retry failed requests up to 3 times
                )
            except Exception as e:
                logger.error(f"Failed to initialize OpenAI client: {str(e)}")
                self.openai_client = None
            
        if settings.GEMINI_API_KEY:
            try:
                genai.configure(api_key=settings.GEMINI_API_KEY)
                self.gemini_model = GenerativeModel('gemini-1.5-flash')
            except Exception as e:
                logger.error(f"Failed to initialize Gemini client: {str(e)}")
                self.gemini_model = None

    async def generate_content(self, content_type: str, parameters: Dict[str, Any], provider: str = "openai") -> Dict[str, Any]:
        """Generate content using AI."""
        try:
            # Try Gemini first if configured
            if provider == "gemini" and self.gemini_model:
                try:
                    response = await self._generate_with_gemini(self._get_prompt(content_type, parameters))
                    return self._parse_response(response, content_type)
                except Exception as e:
                    logger.warning(f"Gemini generation failed, falling back to OpenAI: {str(e)}")
            
            # Fall back to OpenAI if Gemini fails or isn't configured
            if self.openai_client:
                response = await self._generate_with_openai(self._get_prompt(content_type, parameters))
                return self._parse_response(response, content_type)
            
            raise HTTPException(
                status_code=500,
                detail="No AI provider configured"
            )
        except Exception as e:
            logger.error(f"Content generation error: {str(e)}")
            raise HTTPException(
                status_code=500,
                detail=f"Error generating content: {str(e)}"
            )

    async def _generate_with_openai(self, prompt: str) -> str:
        """Generate content using OpenAI."""
        if not self.openai_client:
            raise HTTPException(
                status_code=500,
                detail="OpenAI client not initialized. Please check your API key."
            )
            
        try:
            response = self.openai_client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[{"role": "user", "content": prompt}],
                temperature=0.7,
                max_tokens=1000
            )
            return response.choices[0].message.content
        except Exception as e:
            logger.error(f"OpenAI generation error: {str(e)}")
            raise HTTPException(
                status_code=500,
                detail=f"Error generating content with OpenAI: {str(e)}"
            )

    async def _generate_with_gemini(self, prompt: str) -> str:
        """Generate content using Gemini."""
        try:
            response = self.gemini_model.generate_content(prompt)
            return response.text
        except Exception as e:
            logger.error(f"Gemini generation error: {str(e)}")
            raise HTTPException(
                status_code=500,
                detail=f"Error generating content with Gemini: {str(e)}"
            )

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

    async def extract_youtube_transcript(self, video_url: str) -> Dict[str, str]:
        """Extract transcript and metadata from a YouTube video."""
        try:
            ydl_opts = {
                'quiet': True,
                'no_warnings': True,
                'extract_flat': True
            }
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(video_url, download=False)
                return {
                    "transcript": "",  # You'll need to implement actual transcript extraction
                    "title": info.get('title', ''),
                    "description": info.get('description', ''),
                    "duration": str(info.get('duration', 0)),
                    "thumbnail": info.get('thumbnail', '')
                }
        except Exception as e:
            return {
                "error": str(e),
                "title": "Error fetching metadata",
                "description": str(e),
                "duration": "0",
                "thumbnail": ""
            }

    async def generate_course_content(self, prompt: str) -> Dict[str, Any]:
        """Generate course content using AI."""
        ai_prompt = f"""Given the following course idea or topic, generate a comprehensive course structure. 
        Respond with a valid JSON object in this exact format (no extra text or formatting):
        {{
            "title": "A catchy, engaging course title",
            "sub_title": "A concise subtitle that highlights the key focus",
            "description": "A detailed description that includes what students will learn, key topics covered, prerequisites (if any), expected outcomes, and who this course is for"
        }}

        Prompt: {prompt}"""
        
        try:
            # Try Gemini first
            if self.gemini_model:
                response = await self.gemini_model.generate_content(ai_prompt)
                content = response.text
                if content.startswith("```json"):
                    content = content[7:]
                if content.endswith("```"):
                    content = content[:-3]
                content = content.strip()
                start = content.find("{")
                end = content.rfind("}") + 1
                if start >= 0 and end > start:
                    content = content[start:end]
                return {"content": content}
            
            # Fall back to OpenAI
            elif self.openai_client:
                response = await self.openai_client.chat.completions.create(
                    model="gpt-3.5-turbo",
                    messages=[{"role": "user", "content": ai_prompt}]
                )
                return {"content": response.choices[0].message.content}
            
            # Default response if no AI provider is configured
            return {"content": json.dumps({
                "title": "Untitled Course",
                "sub_title": "A course about " + prompt,
                "description": f"This course will help you learn about {prompt}. Join us to explore this topic in depth."
            })}
        except Exception as e:
            return {"content": json.dumps({
                "title": "Untitled Course",
                "sub_title": "A course about " + prompt,
                "description": f"This course will help you learn about {prompt}. Join us to explore this topic in depth."
            })}

    def _get_prompt(self, content_type: str, params: Dict[str, Any]) -> str:
        """Construct the prompt for generating content."""
        if content_type == "quiz":
            return f"""Generate a {params.get('difficulty', 'beginner')} level quiz about {params.get('topic')} with {params.get('num_questions', 3)} questions.
            Include a mix of {', '.join(params.get('question_types', ['multiple_choice']))} questions.
            Format the response as a valid JSON object with this exact structure:
            {{
                "title": "Quiz Title",
                "description": "Brief description of the quiz",
                "questions": [
                    {{
                        "question": "Question text",
                        "options": ["Option 1", "Option 2", "Option 3", "Option 4"],
                        "correct_answer": 0,
                        "explanation": "Explanation of the correct answer"
                    }}
                ]
            }}
            Ensure the response is valid JSON and follows this exact structure."""
        elif content_type == "summary":
            return f"Summarize the following text concisely:\n\n{params.get('text')}"
        elif content_type == "flashcard":
            return f"Generate {params.get('num_cards', 5)} flashcards about {params.get('topic')}. Format as JSON array with front and back fields."
        elif content_type == "youtube_suggestions":
            return f"Suggest {params.get('num_suggestions', 5)} YouTube videos about {params.get('topic')}. Format as JSON array with title and url fields."
        else:
            raise ValueError(f"Unsupported content type: {content_type}")

    def _parse_response(self, response: str, content_type: str) -> Dict[str, Any]:
        """Parse the response from the AI and return the content."""
        try:
            if content_type == "quiz":
                # Parse the JSON response
                quiz_data = json.loads(response)
                return {
                    "title": quiz_data.get("title", "Generated Quiz"),
                    "content": json.dumps(quiz_data),  # Store the full quiz data as JSON string
                    "content_type": "QUIZ",
                    "description": quiz_data.get("description", "AI-generated quiz"),
                    "meta": {
                        "questions": quiz_data.get("questions", []),
                        "num_questions": len(quiz_data.get("questions", [])),
                        "difficulty": quiz_data.get("difficulty", "beginner")
                    }
                }
            elif content_type == "summary":
                return {"content": response}
            elif content_type == "flashcard":
                return {"content": response}
            elif content_type == "youtube_suggestions":
                return {"content": response}
            else:
                raise ValueError(f"Unsupported content type: {content_type}")
        except json.JSONDecodeError as e:
            logger.error(f"Failed to parse AI response as JSON: {str(e)}")
            raise HTTPException(
                status_code=500,
                detail=f"Invalid response format from AI: {str(e)}"
            )

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