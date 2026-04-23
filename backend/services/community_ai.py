
import os
import json
from openai import OpenAI

# Configure OpenRouter (via OpenAI client) - reusing the key from environment
OPENROUTER_API_KEY = os.getenv("GEMINI_API_KEY")

params = {
    "base_url": "https://openrouter.ai/api/v1",
    "api_key": OPENROUTER_API_KEY,
}

def generate_consensus(barcode, stats, comments):
    """
    Generates a community consensus summary using Gemini.
    
    Args:
        barcode (str): Product barcode.
        stats (dict): {'total_reviews': int, 'average_rating': float}
        comments (list): List of comment dicts with 'rating' and 'comment'.
        
    Returns:
        str: A 1-2 sentence consensus summary.
    """
    if not OPENROUTER_API_KEY:
        return "Community consensus unavailable (API Key missing)."
        
    if not comments:
        return "No community comments yet."

    client = OpenAI(**params)
    
    # Prepare the context for the AI
    # Handle both rating (new) and vote_type (legacy) if needed, but primarily rating
    comments_text = ""
    for c in comments:
        rating = c.get('rating', '?')
        text = c.get('comment', '')
        comments_text += f"- [{rating}/5 Stars]: {text}\n"
    
    prompt = f"""
    Analyze the following community feedback for a food product (Barcode: {barcode}).
    
    Overall Stats: {stats.get('average_rating', 'N/A')}/5 Stars based on {stats.get('total_reviews', 0)} reviews.
    
    Comments:
    {comments_text}
    
    Task:
    Summarize the general sentiment and key takeaways in 1-2 sentences. 
    Start with "Community says:" or similar natural language.
    Mention specific pros/cons if they appear frequently.
    """
    
    try:
        response = client.chat.completions.create(
            model="google/gemini-2.0-flash-001",
            messages=[
                {"role": "system", "content": "You are a helpful community manager AI that summarizes feedback concisely."},
                {"role": "user", "content": prompt}
            ],
        )
        
        return response.choices[0].message.content.strip()
        
    except Exception as e:
        print(f"Consensus generation failed: {e}")
        return "Unable to generate consensus at this time."
