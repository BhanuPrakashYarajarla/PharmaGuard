
import os
import sys
from dotenv import load_dotenv

# Add project root to path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

def test_explain_env():
    print(f"CWD: {os.getcwd()}")
    if '.env' in os.listdir(os.getcwd()):
        print(".env found in CWD")
    else:
        print(".env NOT found in CWD")
        
    # Explicitly load from CWD
    load_dotenv(os.path.join(os.getcwd(), '.env'))

    gemini_key = os.getenv('GEMINI_API_KEY')
    print(f"Script sees GEMINI_API_KEY: {'Yes' if gemini_key else 'No'}")
    
    if not gemini_key:
        print("Reading .env raw content:")
        with open('.env', 'r') as f:
            print(f.read())
            
    from pharmaguard.llm.explain import generate_explanation

    # Mock data
    profile = {
        'primary_gene': 'CYP2D6',
        'phenotype': 'Poor Metabolizer',
        'diplotype': '*1/*2',
        'detected_variants': []
    }
    drug = "Codeine"
    risk = {
        'risk_label': 'High Risk',
        'severity': 'High',
        'confidence_score': 0.9
    }
    
    print("\nCalling generate_explanation...")
    explanation = generate_explanation(profile, drug, risk)
    
    print("\nResult Summary:", explanation.get('summary'))

if __name__ == "__main__":
    test_explain_env()
