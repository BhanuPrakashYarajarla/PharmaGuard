import os
import json
import google.generativeai as genai
from openai import OpenAI
from dotenv import load_dotenv

# Load environment variables
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

def _construct_prompt(phenotype_profile, drug_name, risk_assessment):
    return f"""
    You are a pharmacogenomics expert. Provide a clinical explanation for the following patient scenario.
    
    Patient Data:
    - Gene: {phenotype_profile.get('primary_gene')}
    - Phenotype: {phenotype_profile.get('phenotype')}
    - Detected Variants: {json.dumps(phenotype_profile.get('detected_variants', []))}
    
    Drug: {drug_name}
    Risk Assessment: {risk_assessment.get('risk_label')} ({risk_assessment.get('severity')})
    
    Return a valid JSON object with exactly these keys:
    - summary: A one-sentence summary for a doctor.
    - biological_mechanism: 2-3 sentences explaining the mechanism (e.g., enzyme activity).
    - clinical_recommendation: Actionable advice (e.g., dosage adjustment, alternative drug).
    - guideline_basis: Reference to CPIC or FDA guidelines supporting this (e.g. "CPIC guidelines recommend...").
    - reasoning: Brief explanation of the clinical impact.
    
    Do not include markdown formatting like ```json ... ```. Just the raw JSON string.
    """

def _call_gemini(prompt):
    api_key = os.getenv('GEMINI_API_KEY')
    if not api_key:
        print("DEBUG: GEMINI_API_KEY not found in environment.")
        return None
        
    try:
        print("DEBUG: Attempting to call Gemini...")
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel('gemini-flash-latest')
        response = model.generate_content(prompt)
        print("DEBUG: Gemini call successful.")
        return response.text
    except Exception as e:
        print(f"DEBUG: Gemini Error: {e}")
        return None

def _call_openai(prompt):
    api_key = os.getenv('OPENAI_API_KEY')
    if not api_key:
        print("DEBUG: OPENAI_API_KEY not found in environment.")
        return None
        
    try:
        print("DEBUG: Attempting to call OpenAI...")
        client = OpenAI(api_key=api_key)
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a pharmacogenomics expert."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.7
        )
        print("DEBUG: OpenAI call successful.")
        return response.choices[0].message.content
    except Exception as e:
        print(f"DEBUG: OpenAI Error: {e}")
        return None

def generate_explanation(phenotype_profile, drug_name, risk_assessment):
    """
    Generates a pharmacogenomic explanation using Gemini, falling back to OpenAI, then to Demo.
    """
    prompt = _construct_prompt(phenotype_profile, drug_name, risk_assessment)
    
    # Provider 1: Gemini
    text = _call_gemini(prompt)
    
    # Provider 2: OpenAI Fallback
    if not text:
        text = _call_openai(prompt)
        
    # Provider 3: Demo Fallback
    if not text:
        return {
            "summary": "Demo Mode: API Keys missing or providers failed.",
            "biological_mechanism": "Simulation: The patient's genotype suggests altered metabolism.",
            "clinical_recommendation": f"Consult guidelines for {drug_name} given {phenotype_profile['phenotype']}.",
            "guideline_basis": "CPIC/FDA Guidelines (Simulation)",
            "reasoning": "This is a fallback response because no LLM provider is available."
        }

    # Parse JSON
    try:
        # Clean up potential markdown formatting
        if text.startswith("```json"):
            text = text[7:]
        if text.endswith("```"):
            text = text[:-3]
        return json.loads(text)
    except Exception as e:
        print(f"JSON Parse Error: {e}")
        return {
            "summary": "Error parsing explanation.",
            "biological_mechanism": "N/A",
            "clinical_recommendation": "Refer to standard guidelines.",
            "reasoning": str(e)
        }
