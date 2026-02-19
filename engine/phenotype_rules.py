

# RSID to Phenotype Mapping
VARIANT_PHENOTYPES = {
    'rs4244285': {'gene': 'CYP2C19', 'phenotype': 'Poor Metabolizer', 'severity': 4},
    'rs3892097': {'gene': 'CYP2D6', 'phenotype': 'Poor Metabolizer', 'severity': 4},
    'rs4149056': {'gene': 'SLCO1B1', 'phenotype': 'Increased toxicity risk', 'severity': 3},
    'rs9923231': {'gene': 'CYP2C9', 'phenotype': 'Reduced metabolism', 'severity': 2},
    'rs1142345': {'gene': 'TPMT', 'phenotype': 'Poor metabolizer risk', 'severity': 4},
    'rs3918290': {'gene': 'DPYD', 'phenotype': 'High toxicity risk', 'severity': 5}
}

# Drug to Gene Mapping
DRUG_GENE_MAP = {
    'codeine': 'CYP2D6',
    'clopidogrel': 'CYP2C19',
    'warfarin': 'CYP2C9',
    'simvastatin': 'SLCO1B1',
    'azathioprine': 'TPMT',
    'fluorouracil': 'DPYD'
}

# Severity ranking for tie-breaking
# Higher number = more severe
SEVERITY_RANK = {
    'High toxicity risk': 5,
    'Poor metabolizer risk': 4,
    'Poor Metabolizer': 4,
    'Increased toxicity risk': 3,
    'Reduced metabolism': 2,
    'Normal Metabolizer': 1,
    'Unknown': 0
}
# Abbreviation Mapping
PHENOTYPE_ABBREVIATIONS = {
    'Poor Metabolizer': 'PM',
    'Poor metabolizer risk': 'PM',
    'Reduced metabolism': 'IM',
    'Normal Metabolizer': 'NM',
    'Intermediate Metabolizer': 'IM',
    'Rapid Metabolizer': 'RM',
    'Ultra Rapid Metabolizer': 'URM',
    'Increased toxicity risk': 'PM', # Conservative mapping for SLCO1B1
    'High toxicity risk': 'PM'       # Conservative mapping for DPYD
}

def infer_phenotype(variants, drug_name):
    """
    Infers phenotype from a list of variants, specific to the drug's target gene.
    Returns abbreviation (PM, IM, NM, RM, URM).
    """
    normalized_drug = drug_name.lower().strip()
    target_gene = DRUG_GENE_MAP.get(normalized_drug)
    
    # If drug is unknown, fallback
    if not target_gene:
        return {
            'primary_gene': 'Unknown',
            'phenotype': 'Unknown',
            'diplotype': 'N/A',
            'detected_variants': []
        }

    detected_phenotypes = []
    
    # Filter variants for the specific target gene
    relevant_variants = [v for v in variants if v.get('gene') == target_gene]
    
    # Check each relevant variant against our rules
    for variant in relevant_variants:
        rsid = variant.get('rsid')
        if rsid in VARIANT_PHENOTYPES:
            rule = VARIANT_PHENOTYPES[rsid]
            # Double check gene match just in case
            if rule['gene'] == target_gene:
                detected_phenotypes.append({
                    'gene': rule['gene'],
                    'phenotype': rule['phenotype'],
                    'severity': rule['severity'],
                    'rsid': rsid,
                    'genotype': variant.get('genotype')
                })
            
    if not detected_phenotypes:
        return {
            'primary_gene': target_gene,
            'phenotype': 'NM', # Normal Metabolizer
            'diplotype': '*1/*1',
            'detected_variants': []
        }
        
    # Sort by severity (descending)
    detected_phenotypes.sort(key=lambda x: x['severity'], reverse=True)
    
    # Pick the most severe one as primary
    primary_finding = detected_phenotypes[0]
    
    # Convert to Abbreviation
    full_phenotype = primary_finding['phenotype']
    abbreviation = PHENOTYPE_ABBREVIATIONS.get(full_phenotype, full_phenotype)
    
    return {
        'primary_gene': primary_finding['gene'],
        'phenotype': abbreviation,
        'diplotype': '*1/*2', # Simple placeholder
        'detected_variants': detected_phenotypes
    }
