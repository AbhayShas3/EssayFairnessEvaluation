#!/usr/bin/env python3
"""
Step 1: Extract essays from CLC FCE dataset
Reads XML files and exports essay text + metadata to CSV
"""

import xml.etree.ElementTree as ET
import os
import csv
from pathlib import Path

def extract_text_from_element(elem):
    """Extract all text from an XML element, ignoring tags"""
    if elem is None:
        return ""
    return ''.join(elem.itertext()).strip()

def parse_fce_xml(xml_path):
    """Parse a single FCE XML file"""
    try:
        tree = ET.parse(xml_path)
        root = tree.getroot()
        
        # Extract metadata
        language = root.find('.//language')
        language_text = language.text if language is not None else "Unknown"
        
        age = root.find('.//age')
        age_text = age.text if age is not None else "Unknown"
        
        score = root.find('.//score')
        score_value = float(score.text) if score is not None and score.text else 0
        
        # Extract essay text (remove error annotation markup)
        # Get all text from coded_answer elements
        texts = []
        for answer in root.findall('.//coded_answer'):
            text = extract_text_from_element(answer)
            if text:
                texts.append(text)
        
        full_text = " ".join(texts) if texts else ""
        
        return {
            'filename': os.path.basename(xml_path),
            'language': language_text,
            'age': age_text,
            'score': score_value,
            'essay_text': full_text,
            'length': len(full_text.split())
        }
    except Exception as e:
        print(f"Error parsing {xml_path}: {e}")
        return None

def main():
   
    dataset_path = "/Users/abhayshastry/Documents/Data Sec&Priv/fce-released-dataset"
    
    if not os.path.exists(dataset_path):
        print(f"ERROR: Dataset not found at {dataset_path}")
        print("Update the dataset_path in this script to match your local path")
        return
    
    print(f"Looking for essays in: {dataset_path}")
    
    all_essays = []
    
    # Walk through all subdirectories
    for root, dirs, files in os.walk(dataset_path):
        for file in files:
            if file.endswith('.xml') and 'outliers' not in root:
                xml_path = os.path.join(root, file)
                essay_data = parse_fce_xml(xml_path)
                if essay_data:
                    all_essays.append(essay_data)
    
    print(f"Extracted {len(all_essays)} essays")
    
    # Filter for non-native English speakers
    nnes_essays = [e for e in all_essays if e['language'].lower() != 'english']
    print(f"Found {len(nnes_essays)} non-native English speaker essays")
    
    # Save to CSV
    output_csv = "/Users/abhayshastry/Documents/Data Sec&Priv/EssayFairnessEvaluation/Outputs/fce_essays_extracted.csv"
    
    with open(output_csv, 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=['filename', 'language', 'age', 'score', 'length', 'essay_text'])
        writer.writeheader()
        writer.writerows(nnes_essays)
    
    print(f"\nSaved {len(nnes_essays)} NNES essays to: {output_csv}")
    
    # Print summary statistics
    print("\nLanguage distribution:")
    langs = {}
    for essay in nnes_essays:
        lang = essay['language']
        langs[lang] = langs.get(lang, 0) + 1
    
    for lang, count in sorted(langs.items(), key=lambda x: x[1], reverse=True):
        print(f"  {lang}: {count}")
    
    print("\nScore distribution:")
    scores = sorted([e['score'] for e in nnes_essays])
    print(f"  Min: {min(scores):.1f}")
    print(f"  Max: {max(scores):.1f}")
    print(f"  Mean: {sum(scores)/len(scores):.1f}")

if __name__ == "__main__":
    main()