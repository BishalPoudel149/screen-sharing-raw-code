import logging
from hdbcli import dbapi
import uuid
import logging
import google.generativeai as genai
import base64
import os


# Setup logger for DB operations
logger = logging.getLogger("DBOperations")

os.environ['GOOGLE_API_KEY_TRANSCRIBER'] = 'AIzaSyDX2jwJgQGbMLD8TnXysKA4IIk-Jxqdzzs'

def connect_to_hana():
    try:
        # Attempt to connect to the HANA database
        conn = dbapi.connect(
            address="e081bb32-e254-4b11-a024-8fbd3aa056f3.hana.trial-us10.hanacloud.ondemand.com",
            port=443,
            user="DBADMIN",
            password="JackHana@25"
        )
        
        # If the connection is successful
        print("Successfully connected to the HANA database.")
        
        # Return the connection object for further use
        return conn

    except dbapi.Error as e:
        # Handle specific database connection errors
        print(f"Failed to connect to HANA database. Error: {e}")
        return None

    except Exception as e:
        # Handle other unexpected errors
        print(f"An unexpected error occurred: {e}")
        return None 

conn = connect_to_hana()


def create_session(userId, userName ,sessionId):
    """Create a new session in the HANA database."""
    print('create_session funtion call with ')

    try:
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO "DBADMIN"."SESSIONS" 
            (SESSIONID, USERID, USERNAME, CREATEDTIME) 
            VALUES (?, ?, ?,CURRENT_TIMESTAMP)
        """, (sessionId, userId, userName))
        
        conn.commit()
        logger.info(f"Created session: {sessionId} for user {userName}")

        return sessionId

    except Exception as e:
        logger.error(f"Error creating session: {e}")
        raise e

def store_conversation(session_id, audio_source, content):
    """Store a conversation entry in the HANA database."""
    conversation_id = str(uuid.uuid4())  # Generate unique conversation ID

    try:
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO "DBADMIN"."CONVERSATIONS" 
            (ID, SESSIONID, AUDIOSOURCE, CONTENT,TIMESTAMP ) 
            VALUES (?, ?, ?, ?, CURRENT_TIMESTAMP)
        """, (conversation_id, session_id, audio_source, content))
        
        conn.commit()
        logger.info(f"Stored conversation: {conversation_id}, Source: {audio_source}")

    except Exception as e:
        logger.error(f"Error storing conversation: {e}")
        raise e


async def transcribe_audio_gemini(base64_audio_data, model_name="gemini-1.5-pro"):
    print('inside transcribe_audio_gemini')
    """
    Transcribes audio from a base64 encoded audio file using Gemini.

    Args:
        base64_audio_data: Base64 encoded audio data as a string.
        api_key: Your Gemini API key.
        model_name: The Gemini model to use (e.g., "gemini-1.5-pro").

    Returns:
        The transcribed text as a string, or None if an error occurs.
    """

    api_key=os.getenv("GOOGLE_API_KEY_TRANSCRIBER")

    genai.configure(api_key=api_key)
    model = genai.GenerativeModel(model_name)

    try:    
        # Gemini requires a dict with 'mime_type' and 'data'
        audio_content = {
            "mime_type": "audio/wav",  # or "audio/webm", "audio/ogg", etc. Adjust as needed.
            "data": base64_audio_data,
        }

        response =model.generate_content(audio_content)

        if response.text:
            return response.text
        else:
            return "No transcription available."

    except Exception as e:
        print(f"An error occurred: {e}")
        return None