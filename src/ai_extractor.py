import os
import json
import google.generativeai as genai
from google.colab import userdata

try:
    gemini_api_key = userdata.get('GEMINI_API_KEY')
except Exception:
    gemini_api_key = None

if not gemini_api_key:
    from getpass import getpass
    gemini_api_key = getpass("Please paste your Gemini API key here: ")

genai.configure(api_key=gemini_api_key)

def extract_decisions_with_ai(document_text: str) -> list:
    """
    Sends meeting text to Google Gemini (gemini-3.8-flash) and extracts structured 
    decision fields in a JSON format.
    """
    prompt = f"""
    You are an AI Decision Risk Intelligence engine called Zentriq. 
    Analyze the following business meeting text and extract all business decisions discussed.
    
    For each decision, extract the following fields:
    - "decision": Name or description of the decision
    - "status": Resolved, Unresolved, Planned, In Progress, or At Risk
    - "owner": Person responsible (or null if none)
    - "deadline": Date or timeline mentioned (or null if none)
    - "business_area": Department or area involved (e.g., Marketing, Engineering, Management)
    - "unresolved_issue": Description of why it's pending (or null)
    - "dependencies": Any other task or department it depends on (or null)
    - "conflicts": Any conflicting information or blockers (or null)
    - "risk_factors": Brief note on risks associated with this decision
    
    Return your output strictly as a valid JSON list of objects. Do not include markdown code blocks like ```json in your response, just return the raw JSON array string.
    
    Meeting Text:
    {document_text}
    """
    
    model = genai.GenerativeModel('gemini-3.8-flash')
    response = model.generate_content(prompt)
    
    cleaned_response = response.text.strip()
    if cleaned_response.startswith("```json"):
        cleaned_response = cleaned_response[7:]
    if cleaned_response.endswith("```"):
        cleaned_response = cleaned_response[:-3]
        
    try:
        decisions_data = json.loads(cleaned_response.strip())
        return decisions_data
    except json.JSONDecodeError:
        print("Error parsing JSON from AI response. Raw response was:")
        print(cleaned_response)
        return []