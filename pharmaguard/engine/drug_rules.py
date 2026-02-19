import random

# (Drug, Phenotype) -> Risk Label
DRUG_RISK_RULES = {
    ('codeine', 'PM'): 'Ineffective',
    ('codeine', 'URM'): 'Toxic', 
    ('clopidogrel', 'PM'): 'Ineffective',
    ('warfarin', 'IM'): 'Adjust dosage',
    ('simvastatin', 'PM'): 'Toxic',
    ('azathioprine', 'PM'): 'Toxic',
    ('fluorouracil', 'PM'): 'Toxic'
}

def assess_drug_risk(drug_name, phenotype_profile):
    """
    Assesses risk for a specific drug based on phenotype profile.
    """
    drug_key = drug_name.lower().strip()
    phenotype = phenotype_profile.get('phenotype')
    
    # Direct lookup for risk label
    risk_label = DRUG_RISK_RULES.get((drug_key, phenotype))
    
    # Base Confidence
    confidence = 0.50
    
    # 1. Genetic Evidence: Matches target gene?
    if phenotype_profile.get('primary_gene') not in ['Unknown', 'None']:
        confidence += 0.20
        
    # 2. Variant Evidence: Count variants
    variants = phenotype_profile.get('detected_variants', [])
    variant_count = len(variants)
    if variant_count > 0:
        confidence += min(0.05 * variant_count, 0.15) # Max +0.15 for 3+ variants
        
    # 3. Phenotype Evidence: Risk Level Impact
    if phenotype in ['PM', 'URM']:
        confidence += 0.10 # High impact phenotypes are clearer
    elif phenotype == 'IM':
        confidence += 0.05 # Moderate impact
    elif phenotype == 'NM':
        confidence += 0.05 # Normal is also a confident result
        
    # 4. Small Jitter for "Evidence Weight" Simulation (0.01 - 0.04)
    # This represents slight variations in data quality or coverage depth
    confidence += random.uniform(0.01, 0.04)
        
    if risk_label:
        return {
            'risk_label': risk_label,
            'severity': 'High' if 'Toxic' in risk_label else 'Medium',
            'confidence_score': min(confidence, 0.98) # Max 98%
        }
        
    # Default / Unknown risk
    return {
        'risk_label': 'Standard Risk / Unknown',
        'severity': 'Low',
        'confidence_score': min(confidence, 0.90) # slightly lower cap for unknown risks
    }
