import os
import json
from google import genai
from google.genai import types

GEMINI_API_KEY = "AIzaSyB0tkP9EVV8hU-xgRLTyRHqZUnbO0TAqaI"
client = genai.Client(api_key=GEMINI_API_KEY)

SYSTEM_PROMPT = """You are PlanAnything Assistant, a helpful AI that ONLY helps users create new plans and itineraries for trips, workouts, or any other activities.

Your responsibilities:
1. ONLY respond to requests about creating NEW plans, itineraries, or schedules
2. Ask clarifying questions to understand the user's needs (duration, type of activity, preferences, dates, etc.)
3. Propose detailed plans with tasks broken down by date
4. Accept user feedback and modify the proposed plan accordingly
5. Present the final plan in a structured JSON format
6. If user wants to submit their already written plan, convert it into a proper format and then go ahead with propose detailed plan

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
"""

def chat_with_assistant(messages):
    """
    Send messages to Gemini and get a response.
    messages should be a list of dicts with 'role' and 'content' keys.
    """
    try:
        contents = []

        # Add system prompt as the first user message
        contents.append(
            types.Content(
                role="user",
                parts=[types.Part(text=SYSTEM_PROMPT)]
            )
        )

        # Add user and model messages
        for msg in messages:
            role = "user" if msg['role'] == 'user' else "model"
            contents.append(types.Content(role=role, parts=[types.Part(text=msg['content'])]))

        # Call the model
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=contents
        )

        return response.text or "I'm sorry, I couldn't generate a response."

    except Exception as e:
        return f"I'm sorry, I encountered an error: {str(e)}"

# Example test
messages = [{"role": "user", "content": "Create a 3-day fitness workout plan"}]
print(chat_with_assistant(messages))