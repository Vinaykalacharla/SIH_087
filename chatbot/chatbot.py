import os
from flask import Blueprint, request, jsonify
import sys
from openai import OpenAI
import translators

from db import get_conn, close_conn

# Blueprint for chatbot routes
chatbot_bp = Blueprint("chatbot", __name__)

api_key = os.getenv("OPENAI_API_KEY")
if not api_key:
    print("Warning: OPENAI_API_KEY environment variable not set. Chatbot will not work.")
    client = None
else:
    client = OpenAI(api_key=api_key)

@chatbot_bp.route("/api/chat", methods=["POST"])
def chat():
    """
    Handle farmer queries:
    - Detect and translate input to English
    - Query OpenAI model
    - Translate back to farmer's original language
    - Save logs in MySQL
    """
    try:
        data = request.get_json()
        farmer_message = data.get("message", "")
        lang_code = data.get("lang", "en")  # default English if not provided
        user_id = data.get("user_id")  # optional

        if not farmer_message.strip():
            return jsonify({"error": "Message is required"}), 400

        # Step 1: Translate farmer query to English (skip if already English)
        if lang_code == "en":
            english_query = farmer_message
        else:
            english_query = translators.translate_text(farmer_message, from_language='auto', to_language='en')

        # Step 2: Ask OpenAI for farming-related advice
        try:
            if client is None:
                return jsonify({"error": "OpenAI API key not configured"}), 500

            response = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {"role": "system", "content": "You are a helpful crop advisory assistant for Indian farmers. Keep answers simple, practical, and clear."},
                    {"role": "user", "content": english_query},
                ],
                temperature=0.7,
                max_tokens=300,
            )

            english_answer = response.choices[0].message.content.strip()
        except Exception as e:
            return jsonify({"error": f"OpenAI API error: {str(e)}"}), 500

        # Step 3: Translate back to farmer's original language
        final_answer = (
            translators.translate_text(english_answer, from_language='en', to_language=lang_code)
            if lang_code != "en"
            else english_answer
        )

        # Step 4: Save conversation to DB
        conn = get_conn()
        try:
            with conn.cursor() as cursor:
                cursor.execute(
                    "INSERT INTO chat_logs (user_id, message, response, language) VALUES (%s, %s, %s, %s)",
                    (user_id, farmer_message, final_answer, lang_code)
                )
            conn.commit()
        finally:
            close_conn(conn)

        return jsonify({
            "query_original": farmer_message,
            "query_english": english_query,
            "answer_english": english_answer,
            "answer_final": final_answer,
            "lang": lang_code
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 500
