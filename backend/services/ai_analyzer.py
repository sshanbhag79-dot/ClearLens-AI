import os
import json
from openai import OpenAI
from backend.models import ProductData, UserProfile, ScanResponse, IngredientAnalysis

# Configure OpenRouter (via OpenAI client)
OPENROUTER_API_KEY = os.getenv("GEMINI_API_KEY")

params = {
    "base_url": "https://openrouter.ai/api/v1",
    "api_key": OPENROUTER_API_KEY,
}

def analyze_safety(product: ProductData, profile: UserProfile) -> ScanResponse:
    if not OPENROUTER_API_KEY:
        return ScanResponse(
            status="Yellow", 
            reason="API Key missing. Unable to analyze.",
            product=product
        )

    client = OpenAI(**params)
    
    # SAFE F-STRING CONSTRUCTION:
    # 1. Define the dynamic user context
    user_context = f"""
    User Profile:
    - Allergies: {', '.join(profile.allergies)}
    - Dietary Goals: {', '.join(profile.diets)}
    - Strictness: {profile.strictness}
    
    Product:
    - Name: {product.product_name}
    - Ingredients: {product.ingredients_text}
    - Marketing Claims (if any): {product.marketing_claims or "Look at the name/packaging claims"}
    """

    # 2. Define the static JSON template (NO f-string here!)
    json_template = """
    Output strictly in JSON format:
    {
        "status": "Green" | "Yellow" | "Red",
        "reason": "1 sentence specific reason for the status.",
        "marketing_vs_reality": "Expose the 'Health-Washing' gap.",
        "community_takeaway": "Simple student-to-student advice.",
        "bio_red_flags": ["List problematic ingredients"],
        "trust_score": 1,
        "pros": ["nutritional highlights"],
        "cons": ["nutritional drawbacks"],
        "ingredients_analysis": [
            {
                "name": "Common English Name",
                "status": "Safe" | "Caution" | "Avoid",
                "reason": "Simple explanation",
                "significance": "High" | "Medium" | "Low" | "Trace"
            }
        ],
        "alternative": "A Green 'System Reboot' whole-food alternative."
    }
    """

    # 3. Combine them simply
    prompt = f"""
    You are the "Bio-Guide" AI, the supportive health advocate for BioFilter.
    
    {user_context}
    
    Task:
    1. Identify 'Health-Washing' in the marketing claims.
    2. Provide a 'Trust Verdict' (1-10).
    3. Identify "Bio Red Flags".
    4. If it's a Red item, suggest a Green 'System Reboot'.

    {json_template}
    """
    
    try:
        response = client.chat.completions.create(
            model="google/gemini-2.0-flash-001",
            messages=[
                {"role": "system", "content": "You are a no-nonsense food investigator AI. Output JSON only. For ingredients_analysis, ALWAYS provide EXACTLY one of these significance levels: 'High', 'Medium', 'Low', or 'Trace'. Do NOT include percentages or 'Unknown'."},
                {"role": "user", "content": prompt}
            ],
            response_format={"type": "json_object"}
        )
        
        content = response.choices[0].message.content
        print(f"DEBUG: Raw AI Response: {content}")
        try:
            result = json.loads(content)
        except Exception as json_err:
            print(f"JSON Parsing failed: {json_err}")
            return ScanResponse(
                status="Yellow",
                reason=f"AI returned invalid JSON: {json_err}",
                product=product
            )
        
        # Build analysis list with safety
        ingredients_list = []
        for ing in result.get("ingredients_analysis", []):
            ingredients_list.append(IngredientAnalysis(
                name=ing.get("name", "Unknown"),
                status=ing.get("status", "Safe"),
                reason=ing.get("reason", ""),
                significance=ing.get("significance", "Medium")
            ))

        # Handle trust score safely
        trust_val = result.get("trust_score", 5)
        try:
            health_score_calc = int(trust_val) * 10
        except (ValueError, TypeError):
            health_score_calc = 50

        return ScanResponse(
            status=result.get("status", "Yellow"),
            reason=result.get("reason", "Analysis completed."),
            alternative=result.get("alternative"),
            product=product,
            pros=result.get("pros", []),
            cons=result.get("cons", []),
            health_score=health_score_calc,
            ingredients_analysis=ingredients_list,
            marketing_vs_reality=result.get("marketing_vs_reality"),
            community_takeaway=result.get("community_takeaway"),
            bio_red_flags=result.get("bio_red_flags", []),
            trust_score=trust_val if isinstance(trust_val, int) else 5
        )
    except Exception as e:
        import traceback
        print(f"AI Analysis failed: {e}")
        traceback.print_exc()
        return ScanResponse(
            status="Yellow", 
            reason=f"AI analysis failed: {str(e)}",
            product=product
        )
