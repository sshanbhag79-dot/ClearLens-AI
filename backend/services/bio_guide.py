import os
import json
from openai import OpenAI
from backend.models import ChatRequest, ChatResponse, UserProfile, ProductData

# Configure OpenRouter (via OpenAI client)
OPENROUTER_API_KEY = os.getenv("GEMINI_API_KEY")

params = {
    "base_url": "https://openrouter.ai/api/v1",
    "api_key": OPENROUTER_API_KEY,
}

def get_bio_guide_reply(request: ChatRequest, current_product: ProductData = None) -> ChatResponse:
    """
    Core logic for the Bio-Guide AI. 
    Combines Ingredient Translation and Conversational Bio-Logging.
    """
    if not OPENROUTER_API_KEY:
        return ChatResponse(reply="Sorry, my brain (API Key) is missing! Tag the developer.")

    client = OpenAI(**params)
    
    product_context = ""
    if current_product:
        product_context = f"""
        Current Context Product:
        - Name: {current_product.product_name}
        - Calories: {current_product.calories} kcal/100g
        - Ingredients: {current_product.ingredients_text}
        - Marketing Claims: {current_product.marketing_claims or "N/A"}
        """

    system_prompt = f"""
    You are the ClearLens Advocate. 
    Your goal is to help the Leeds community decode food labels, build healthy recipes from their pantry, and log meals effortlessly.
    Persona: Supportive, transparent, and expert health advocate.

    User Profile:
    - Allergies: {', '.join(request.user_profile.allergies or [])}
    - Dietary Goals: {', '.join(request.user_profile.diets or [])}
    - Strictness: {request.user_profile.strictness}

    Core Capabilities:

    1. The Ingredient Translator (Community English):
    - Access the ingredient_list and 'marketing claims' of the currently scanned product.
    - Translate complex chemicals into 'Community English' (e.g., 'E471 is just a thickener for shelf-life').
    - Identify 'Health-Washing': Flag if marketing claims (e.g., 'Natural') contradict ingredients.

    2. The Bio-Chef Meal Builder:
    - When asked for meal options (e.g., "What can I make with this?"), use the currently scanned item as the base.
    - Incorporate any pantry items the user mentions.
    - Suggest a simple, healthy recipe combining the scan + pantry items.
    - Suggest 'Bio-Boosts': One cheap, whole-food addition (e.g., spinach, lentils).

    3. Autonomous Bio-Logging:
    - Listen for logging intent (e.g., 'Add this', 'I just ate a bowl of oats', 'Log 2 bananas').
    - TRIGGER: Output "intent": "LOG_MEAL".
    - If 'this', use current scan data.
    - If generic (e.g., "bowl of soup"), ESTIMATE the calories based on standard portion sizes.
    - Response: "Logged! Your Bio-Quality Index is now updated." (plus a brief encouraging remark).

    Persona Guardrails:
    - If a user logs a 🔴 Red item, don't judge—instead, suggest a 🟢 Green 'System Reboot' (healthy alternative) for their next meal.
    - Always sign off as "ClearLens".

    {product_context}

    Output strictly in JSON format:
    {{
        "reply": "Your conversational response",
        "intent": "LOG_MEAL" | null,
        "log_params": {{
            "product_name": "...",
            "calories": float (100g base or estimate),
            "quantity": float (multiplier),
            "status": "Red" | "Yellow" | "Green"
        }} | null
    }}
    """

    try:
        response = client.chat.completions.create(
            model="google/gemini-2.0-flash-001",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": request.message}
            ],
            response_format={"type": "json_object"}
        )
        
        content = response.choices[0].message.content
        result = json.loads(content)
        
        return ChatResponse(
            reply=result.get("reply"),
            intent=result.get("intent"),
            log_params=result.get("log_params")
        )
    except Exception as e:
        print(f"Bio-Guide Chat failed: {e}")
        return ChatResponse(reply=f"Ugh, my brain stalled: {str(e)}")
