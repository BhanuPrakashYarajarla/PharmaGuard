import re

TARGET_GENES = {
    'CYP2D6', 'CYP2C19', 'CYP2C9', 'SLCO1B1', 'TPMT', 'DPYD'
}


def parse_vcf(file_path):
    """
    Parses a VCF file and extracts variants for target genes.
    
    Returns:
        List of dictionaries: [ { "gene": "...", "rsid": "...", "genotype": "..." } ]
    """
    variants = []
    print(f"DEBUG: Parsing {file_path}")
    
    try:
        with open(file_path, 'r') as f:
            for line in f:
                if line.startswith('#'):
                    continue
                
                # Flexible whitespace splitting (tabs or spaces)
                parts = re.split(r'\s+', line.strip())
                
                if len(parts) < 10:
                    # Some VCFs might have fewer columns if no samples, but we need samples
                    if len(parts) >= 8: 
                         # Try to parse anyway if it looks like a variant line but maybe missing optional cols?
                         # Actually, standard VCF has 8 fixed cols + FORMAT + SAMPLES.
                         # If we don't have samples (len < 10), we can't extract genotype.
                         continue
                    continue
                
                # Standard VCF columns: 
                # CHROM POS ID REF ALT QUAL FILTER INFO FORMAT SAMPLE
                # 0     1   2  3   4   5    6      7    8      9
                chrom = parts[0]
                pos = parts[1]
                rsid = parts[2]
                ref = parts[3]
                alt = parts[4]
                info = parts[7]
                fmt_str = parts[8]
                sample_str = parts[9] # Taking the first sample
                
                print(f"DEBUG: Checking variant {rsid} at {chrom}:{pos}")

                # Extract Gene
                # Assumption: GENE=GeneName in INFO field
                # Handle cases where GENE might be at start, middle, or end of INFO string
                gene_match = re.search(r'(?:^|;)GENE=([^;]+)', info)
                
                gene = None
                if gene_match:
                    gene = gene_match.group(1)
                
                # Fallback: Check if info IS just the gene name (unlikely but possible in hackathon data)
                if not gene and info in TARGET_GENES:
                     gene = info

                if not gene:
                    # Check if gene is in TARGET_GENES directly (maybe info field is messy)
                    # This is aggressive but helpful for hackathon data
                    for g in TARGET_GENES:
                        if g in info:
                            gene = g
                            break
                
                if not gene:
                    continue
                
                print(f"DEBUG: Found target gene {gene}")

                if gene not in TARGET_GENES:
                    continue
                
                # Extract Genotype
                # Find GT index in FORMAT
                fmt_parts = fmt_str.split(':')
                try:
                    gt_idx = fmt_parts.index('GT')
                except ValueError:
                    print("DEBUG: No GT in FORMAT")
                    continue
                    
                sample_parts = sample_str.split(':')
                if len(sample_parts) <= gt_idx:
                    continue
                    
                gt_val = sample_parts[gt_idx]
                
                # Parse genotype like 0/1, 0|1, 1/1
                # We need to map 0->REF, 1->ALT1, 2->ALT2...
                
                alleles = [ref] + alt.split(',')
                
                # Regex to find numbers in GT string (handles / and |)
                gt_indices = re.findall(r'([0-9.]+)', gt_val)
                
                mapped_alleles = []
                for idx_str in gt_indices:
                    if idx_str == '.':
                        mapped_alleles.append('.') # Missing
                    else:
                        try:
                            idx = int(idx_str)
                            if 0 <= idx < len(alleles):
                                mapped_alleles.append(alleles[idx])
                            else:
                                mapped_alleles.append('?') # Invalid index
                        except ValueError:
                            mapped_alleles.append('?')
                            
                genotype_str = '/'.join(mapped_alleles)
                
                print(f"DEBUG: Extracted {gene} {rsid} {genotype_str}")

                variants.append({
                    "gene": gene,
                    "rsid": rsid,
                    "genotype": genotype_str
                })
                
    except Exception as e:
        print(f"Error parsing VCF: {e}")
        return []

    return variants

