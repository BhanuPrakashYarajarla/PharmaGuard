
import os
import sys

# Add project root to path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

from pharmaguard.engine.drug_rules import assess_drug_risk

def test_confidence_scoring():
    print("Testing Confidence Scoring...")
    
    # Case 1: Minimal Evidence (Normal Metabolizer, No Variants)
    profile1 = {
        'primary_gene': 'CYP2D6', # Matched gene (+0.2)
        'phenotype': 'Normal Metabolizer',
        'detected_variants': []
    }
    # Base 0.5 + 0.2 (Gene) = 0.7
    risk1 = assess_drug_risk('Codeine', profile1)
    print(f"\nCase 1 (Normal): Score = {risk1['confidence_score']}")
    assert risk1['confidence_score'] == 0.7
    
    # Case 2: Strong Evidence (Poor Metabolizer, Variants Found)
    profile2 = {
        'primary_gene': 'CYP2D6', # +0.2
        'phenotype': 'Poor Metabolizer', # +0.1
        'detected_variants': [{'rsid': 'rs123'}] # +0.15
    }
    # Base 0.5 + 0.2 + 0.1 + 0.15 = 0.95
    risk2 = assess_drug_risk('Codeine', profile2)
    print(f"\nCase 2 (Risk Found): Score = {risk2['confidence_score']}")
    assert risk2['confidence_score'] >= 0.95

    # Case 3: Unknown Gene (e.g. drug not in map)
    profile3 = {
        'primary_gene': 'Unknown',
        'phenotype': 'Unknown',
        'detected_variants': []
    }
    # Base 0.5
    risk3 = assess_drug_risk('MysteryDrug', profile3)
    print(f"\nCase 3 (Unknown): Score = {risk3['confidence_score']}")
    assert risk3['confidence_score'] == 0.5

    print("\nSUCCESS: Scoring logic verified!")

if __name__ == "__main__":
    test_confidence_scoring()
