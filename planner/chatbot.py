import os
import json
from datetime import datetime, timedelta
from google import genai
from google.genai import types
from django.utils import timezone

GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY")
client = genai.Client(api_key=GEMINI_API_KEY)

SYSTEM_PROMPT = """You are PlanAnything Assistant, a helpful AI that ONLY helps users create new plans and itineraries for trips, workouts, or any other activities.

Your responsibilities:
1. ONLY respond to requests about creating NEW plans, itineraries, or schedules
2. Ask clarifying questions to understand the user's needs (duration, type of activity, preferences, dates, etc.)
3. Propose detailed plans with tasks broken down by date
4. Accept user feedback and modify the proposed plan accordingly
5. Present the final plan in a structured JSON format

Important restrictions:
- DO NOT help with editing existing plans - only creating new ones
- DO NOT respond to questions unrelated to plan creation
- DO NOT provide general advice, answer trivia, or engage in off-topic conversation
- If asked something unrelated, politely redirect: "I can only help you create new plans and itineraries. What would you like to plan?"

When you have gathered enough information and are ready to propose a plan, respond with JSON in this EXACT format:
{
  "type": "plan_proposal",
  "plan": {
    "title": "Plan Title",
    "description": "Brief description of the plan",
    "color": "#3B82F6",
    "start_date": "YYYY-MM-DD",
    "end_date": "YYYY-MM-DD",
    "tasks": [
      {
        "title": "Task title",
        "description": "Task description",
        "task_date": "YYYY-MM-DD",
        "status": "pending"
      }
    ]
  }
}

The color should be a hex color code (default: #3B82F6 for blue, #10B981 for green, #F59E0B for amber, #EF4444 for red, #8B5CF6 for purple).

Before sending the JSON, ask if the user wants any changes. Only send the JSON format when the user confirms they're ready to create the plan."""

def chat_with_assistant(messages):
    """
    Send messages to Gemini and get a response.
    messages should be a list of dicts with 'role' and 'content' keys.
    """
    try:
        contents = []
        for msg in messages:
            role = "user" if msg['role'] == 'user' else "model"
            contents.append(types.Content(role=role, parts=[types.Part(text=msg['content'])]))
        
        generation_config = types.GenerationConfig(
            max_output_tokens=2048
        )
        
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=contents,
            system_instruction=SYSTEM_PROMPT,
            generation_config=generation_config
        )
        
        return response.text or "I'm sorry, I couldn't generate a response."
    except Exception as e:
        return f"I'm sorry, I encountered an error: {str(e)}"

def parse_plan_proposal(response_text):
    """
    Try to extract a plan proposal from the assistant's response.
    Returns None if no valid plan proposal is found.
    """
    try:
        response_text = response_text.strip()
        
        if '```json' in response_text:
            start = response_text.find('```json') + 7
            end = response_text.find('```', start)
            json_text = response_text[start:end].strip()
        elif '```' in response_text:
            start = response_text.find('```') + 3
            end = response_text.find('```', start)
            json_text = response_text[start:end].strip()
        elif response_text.startswith('{'):
            json_text = response_text
        else:
            return None
        
        data = json.loads(json_text)
        
        if data.get('type') == 'plan_proposal' and 'plan' in data:
            return data['plan']
        
        return None
    except:
        return None
