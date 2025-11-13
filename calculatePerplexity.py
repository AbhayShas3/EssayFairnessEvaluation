#!/usr/bin/env python3
"""
Step 2: Calculate perplexity for all essays
Uses GPT-2 model via Hugging Face transformers
"""

import torch
from transformers import GPT2Tokenizer, GPT2LMHeadModel
import csv
import sys

def calculate_perplexity(text, model, tokenizer):
    """
    Calculate perplexity of text using GPT-2
    Lower perplexity = more predictable text
    """
    try:
        # Tokenize
        input_ids = tokenizer.encode(text, return_tensors="pt", truncation=True, max_length=512)
        
        # Skip very short texts
        if input_ids.shape[1] < 5:
            return None
        
        # Get model output
        with torch.no_grad():
            outputs = model(input_ids, labels=input_ids)
            loss = outputs.loss
        
        # Convert loss to perplexity
        perplexity = torch.exp(loss).item()
        return perplexity
    except Exception as e:
        print(f"Error calculating perplexity: {e}")
        return None

def main():
    print("Loading GPT-2 model (this may take a minute on first run)...")
    tokenizer = GPT2Tokenizer.from_pretrained("gpt2")
    model = GPT2LMHeadModel.from_pretrained("gpt2")
    model.eval()
    
    # Use GPU if available
    if torch.cuda.is_available():
        model.to('cuda')
        print("Using GPU")
    else:
        print("Using CPU")
    
    # Read extracted essays
    input_csv = "/Users/abhayshastry/Documents/Data Sec&Priv/EssayFairnessEvaluation/Outputs/fce_essays_extracted.csv"
    output_csv = "/Users/abhayshastry/Documents/Data Sec&Priv/EssayFairnessEvaluation/Outputs/fce_essays_with_perplexity.csv"
    
    print(f"Reading essays from: {input_csv}")
    
    essays_with_perplexity = []
    
    with open(input_csv, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        total = sum(1 for _ in f)
    
    with open(input_csv, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for i, row in enumerate(reader):
            if i % 50 == 0:
                print(f"Processing essay {i}...")
            
            essay_text = row['essay_text']
            perplexity = calculate_perplexity(essay_text, model, tokenizer)
            
            if perplexity is not None:
                row['perplexity'] = perplexity
                essays_with_perplexity.append(row)
    
    print(f"Calculated perplexity for {len(essays_with_perplexity)} essays")
    
    # Save with perplexity scores
    fieldnames = list(essays_with_perplexity[0].keys()) if essays_with_perplexity else []
    
    with open(output_csv, 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(essays_with_perplexity)
    
    print(f"Saved {len(essays_with_perplexity)} essays with perplexity to: {output_csv}")
    
    # Print statistics
    perplexities = [float(e['perplexity']) for e in essays_with_perplexity]
    print(f"\nPerplexity statistics:")
    print(f"  Min: {min(perplexities):.2f}")
    print(f"  Max: {max(perplexities):.2f}")
    print(f"  Mean: {sum(perplexities)/len(perplexities):.2f}")
    print(f"  Median: {sorted(perplexities)[len(perplexities)//2]:.2f}")

if __name__ == "__main__":
    main()