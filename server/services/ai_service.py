from openai import OpenAI
import google.generativeai as genai

import base64
import os
import json


OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

def openai_analyze_image_ai(image_bytes: bytes) -> dict:
    # Placeholder for AI image analysis logic
    ai_client = OpenAI(api_key=OPENAI_API_KEY)
    
    base64_image = base64.b64encode(image_bytes).decode("utf-8")
    try:
        response = ai_client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "image_url",
                            "image_url": {
                                "url": f"data:image/png;base64,{base64_image}"
                            }
                        },
                        {
                            "type": "text",
                            "text": "Describe this image. List all visible objects. Identify if a product is present. Provide the response as a single JSON body with the following structure: {\"overall_description\": \"...\", \"objects\": [{\"name\": \"...\", \"description\": \"...\"}, {\"name\": \"...\", \"description\": \"...\"}]}."
                            # "text": "Describe this image. List objects. Identify if a product is present with json body like name and description."
                        }
                    ]
                }
            ]
        )
        return response
    except Exception as e:
        return None
    

def gemini_analyze_image_ai(image_bytes: bytes) -> dict:
    try:
        # Configure Gemini
        genai.configure(api_key=GEMINI_API_KEY)
    
        # Use Gemini 1.5 Flash (fast + cheap + supports vision)
        model = genai.GenerativeModel("gemini-2.5-flash")
    
        # Send image + text prompt
        response = model.generate_content(
            [
                {"mime_type": "image/png", "data": image_bytes},
                "Describe this image. List all visible objects. Identify if a product is present. Provide the response as a single JSON body with the following structure: {\"overall_description\": \"...\", \"objects\": [{\"name\": \"...\", \"description\": \"...\"}, {\"name\": \"...\", \"description\": \"...\"}]}."
            ]
        )
        
        # Clean up response text to extract JSON
        response = response.text.replace("\n", "").replace("```json","```").replace("```","")
        json_response = json.loads(response)
        print("RESPONSE",json_response)
    
        return json_response
    except Exception as e:
        print(f"Error in Gemini AI analysis: {e}")
        raise e