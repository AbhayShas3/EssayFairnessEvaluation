#!/usr/bin/env python3
"""
Step 3: Prepare test dataset
- Filter for high-quality essays (based on human scores)
- Split into low-perplexity and high-perplexity groups
- Export essays for LLM scoring
"""

import csv
import pandas as pd

def main():
    # Read essays with perplexity
    input_csv = "/Users/abhayshastry/Documents/Data Sec&Priv/EssayFairnessEvaluation/Outputs/fce_essays_with_perplexity.csv"
    
    print(f"Reading from: {input_csv}")
    df = pd.read_csv(input_csv)
    
    print(f"Total essays: {len(df)}")
    
    # Convert score to float
    df['score'] = df['score'].astype(float)
    
    # Filter for high-quality essays (top scoring)
    # Use essays in top 25% by score
    score_threshold = df['score'].quantile(0.75)
    print(f"Score threshold for 'high quality': {score_threshold:.1f}")
    
    high_quality = df[df['score'] >= score_threshold].copy()
    print(f"High-quality essays (top 25%): {len(high_quality)}")
    
    # Sort by perplexity
    high_quality = high_quality.sort_values('perplexity')
    
    # Split into low and high perplexity groups
    # Take bottom 20 (lowest perplexity) and top 20 (highest perplexity)
    if len(high_quality) >= 40:
        low_perplexity = high_quality.head(20).copy()
        high_perplexity = high_quality.tail(20).copy()
    else:
        # If we don't have 40, take what we can
        split_point = len(high_quality) // 2
        low_perplexity = high_quality.head(split_point).copy()
        high_perplexity = high_quality.tail(split_point).copy()
    
    print(f"\nLow perplexity group (n={len(low_perplexity)}):")
    print(f"  Perplexity range: {low_perplexity['perplexity'].min():.2f} - {low_perplexity['perplexity'].max():.2f}")
    print(f"  Mean score: {low_perplexity['score'].mean():.1f}")
    
    print(f"\nHigh perplexity group (n={len(high_perplexity)}):")
    print(f"  Perplexity range: {high_perplexity['perplexity'].min():.2f} - {high_perplexity['perplexity'].max():.2f}")
    print(f"  Mean score: {high_perplexity['score'].mean():.1f}")
    
    # Combine both groups
    test_set = pd.concat([low_perplexity, high_perplexity], ignore_index=True)
    
    # Add group label
    test_set['perplexity_group'] = 'low'
    test_set.loc[test_set['perplexity'] >= high_quality['perplexity'].median(), 'perplexity_group'] = 'high'
    
    # Save test set
    output_csv = "/Users/abhayshastry/Documents/Data Sec&Priv/EssayFairnessEvaluation/Outputs/fce_test_set.csv"
    test_set.to_csv(output_csv, index=False, encoding='utf-8')
    
    print(f"\nTest set saved to: {output_csv}")
    print(f"Total essays for LLM scoring: {len(test_set)}")
    
    # Create a simple file with just essay text for easy viewing/scoring
    output_txt = "/Users/abhayshastry/Documents/Data Sec&Priv/EssayFairnessEvaluation/Outputs/essays_for_scoring.txt"
    with open(output_txt, 'w', encoding='utf-8') as f:
        for idx, row in test_set.iterrows():
            f.write(f"\n{'='*60}\n")
            f.write(f"ESSAY ID: {row['filename']}\n")
            f.write(f"Language: {row['language']}\n")
            f.write(f"Human Score: {row['score']}\n")
            f.write(f"Perplexity: {row['perplexity']:.2f}\n")
            f.write(f"Group: {row['perplexity_group']}\n")
            f.write(f"{'='*60}\n")
            f.write(row['essay_text'][:2000])  # First 2000 chars
            f.write("\n")
    
    print(f"Essays for manual scoring saved to: {output_txt}")

if __name__ == "__main__":
    main()