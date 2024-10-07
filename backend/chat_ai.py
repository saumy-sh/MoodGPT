from flask import request, jsonify, Blueprint, session
import os
from backend.auth import login_required
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()

chat_ai = Blueprint("chat", __name__)

GEMINI_API_KEY = os.getenv("GEMINI_API")
# Configure the Gemini API
genai.configure(api_key=GEMINI_API_KEY)

generation_config = {
    "temperature": 1,
    "top_p": 0.95,
    "top_k": 64,
    "max_output_tokens": 8192,
    "response_mime_type": "text/plain",
}

model = genai.GenerativeModel(
    model_name="gemini-1.5-flash",
    generation_config=generation_config,
    system_instruction= """
You are a mental health chatbot designed to support and engage users in managing their emotional well-being and daily tasks. Always address the user by their username and personalize responses based on the following information:

User Data:

Username
Last login time
Current mood
Completed activities (in the form of a list. If [], the user hasn't completed any activities yet)
Badges earned
Last session duration
Emotional Support:

Empathize with the user's current mood, whether it’s positive or negative.
Respond in a supportive and encouraging tone, adjusting based on how the user feels.
Suggest activities that align with the user’s emotional state to help improve their well-being.
Activity Suggestions:
Use the list of activities available on the platform, categorized under "Daily To-Dos":

Gratitude Journaling
Meditation or Deep Breathing
Physical Exercise
Positive Affirmations
Digital Detox
Mindful Eating
Creative Expression
Mood Check-In
Based on the user's completed activities, suggest tasks they haven’t completed yet today. If the completed_activities list is empty ([]), recognize that the user hasn't done any activities yet and encourage them to start. Explain how each activity can benefit their mental and emotional health, and remind them that these activities can be completed on the site.

Encouragement and Progress:

Highlight the badges the user has earned and celebrate their achievements.
Encourage the user to complete remaining tasks to unlock new achievements and earn more points.
Use positive reinforcement and remind them of the benefits of staying consistent with their daily tasks.
Personalized Flow:

Adapt your responses based on the user's mood, progress, and engagement level.
If the user feels stressed, suggest calming activities like Meditation or Deep Breathing.
If the user feels positive, encourage them to continue their streak by completing rewarding tasks.
Always make sure to suggest completing these activities on the site.
Session Duration Check:

If the user's last session was short, ask if there was a specific reason for their brief stay and offer support or solutions.
If the session duration was satisfactory, acknowledge their engagement and encourage them to maintain or increase it by exploring more activities.
Tailor the conversation based on whether the user is staying engaged with the platform for meaningful durations.
"""
)




# Initialize the chat session history in the session (if not already done)
def init_chat_history(activities,username,userMood,loginedAt,badges):
    if 'chat_history' not in session or session["chat_history"] == []:
       
        # Initialize the chat history
        chat_history = [
            {
                "role": "user",
                "parts": [
                    f"I am {username}. I last logged in at {loginedAt}. My current mood is {userMood}. I have completed {activities} activities and earned {badges} badges. Use this info for future reference."
                ],
            } 
        ]
        session['chat_history'] = chat_history
    else:
        update_history(f"{activities} is the list of activities I have completed","user")

# Helper function to update chat history
def update_history(new_message, sender="user"):
    history = session.get('chat_history')
    history.append({
        "role": sender,
        "parts": [new_message]
    })
    
    session['chat_history'] = history  # Save the updated history back to session
    


@chat_ai.route("/chat", methods=['POST', 'GET'])
@login_required
def chat():
    print(request.json.get("message"))
    user_message = request.json.get('message')
    # username = request.json.get('username')  # Get the username from the request
    
    # Add user message to chat history
    update_history(user_message, "user")
    print(session["chat_history"])
    
    # Start a chat session with the current chat history
    chat_session = model.start_chat(history=session['chat_history'])

    # Send the user's message to the chat session
    response = chat_session.send_message(user_message)
    
    # Add model's response to chat history
    update_history(response.text, "model")
    
    # Return the chatbot's response
    return jsonify({"response": response.text})


@chat_ai.route("/update_info", methods=['POST', 'GET'])
@login_required
def update_info():
    
    username = session.get('username')
    loginedAt = session.get('loginedAt')
    activities = session.get('activities')
    userMood = session.get('userMood')
    badges = session.get("badges")
    

    # If new activities are completed, update the history
    init_chat_history(activities,username,userMood,loginedAt,badges)

    # Optionally, start a chat session here if needed
    # chat_session = model.start_chat(history=session['chat_history'])

    # Return success response (this route doesn't need to return a chatbot response unless needed)
    return jsonify({"response": "Info updated successfully!"})
