#!/usr/bin/env python3
"""
Step 4: Record LLM scores and do preliminary analysis
This is where you manually score essays with ChatGPT/Claude
"""

import csv
import pandas as pd
from scipy import stats

def record_llm_scores():
    """
    Workflow for recording LLM scores:
    1. Read the test set
    2. For each essay, copy-paste into ChatGPT/Claude
    3. Record the score
    4. Save results
    """
    
    # Read test set
    test_set_csv = "/home/claude/fce_test_set.csv"
    df = pd.read_csv(test_set_csv)
    
    print("Template for LLM scoring:\n")
    print("Copy this prompt to ChatGPT/Claude:")
    print("""
You are an experienced writing instructor evaluating student essays. Score this essay on a scale of 1-10 based solely on the quality of its argument, use of evidence, and logical reasoning. Ignore minor grammar errors and focus only on the strength and development of ideas. Provide only the score as a number.

[PASTE ESSAY TEXT HERE]
    """)
    print("\n" + "="*60)
    print("For this initial run, we'll score a sample of 5-10 essays")
    print("="*60 + "\n")
    
    # Create output file for manual score entry
    scores_file = "/home/claude/llm_scores_manual.csv"
    
    # For demo: create template with first 5 essays
    sample_essays = df.head(5).copy()
    sample_essays['model'] = 'ChatGPT'  # or 'Claude' or 'Gemini'
    sample_essays['score_run1'] = None
    sample_essays['score_run2'] = None
    sample_essays['score_run3'] = None
    sample_essays['mean_score'] = None
    
    # Save template
    sample_essays.to_csv(scores_file, index=False, encoding='utf-8')
    
    print(f"Score template saved to: {scores_file}")
    print(f"Sample essays ready for scoring (first 5 essays)")
    print("\nInstructions:")
    print("1. For each essay below, copy-paste the text to ChatGPT")
    print("2. Score it 3 times to get the mean")
    print("3. Record the 3 scores in the CSV file")
    print("\n" + "="*60)
    
    # Print first essay as example
    first_essay = df.iloc[0]
    print(f"\nExample Essay 1:")
    print(f"Filename: {first_essay['filename']}")
    print(f"Language: {first_essay['language']}")
    print(f"Human Score: {first_essay['score']}")
    print(f"Perplexity: {first_essay['perplexity']:.2f}")
    print(f"Perplexity Group: {first_essay['perplexity_group']}")
    print("\nText (first 500 chars):")
    print(first_essay['essay_text'][:500] + "...")

def analyze_preliminary_results():
    """
    After you've scored some essays with LLMs, run this to see patterns
    """
    try:
        scores_file = "/home/claude/llm_scores_manual.csv"
        df = pd.read_csv(scores_file)
        
        # Calculate mean score
        df['mean_score'] = df[['score_run1', 'score_run2', 'score_run3']].mean(axis=1)
        
        # Split by perplexity group
        low_perp = df[df['perplexity_group'] == 'low']
        high_perp = df[df['perplexity_group'] == 'high']
        
        print("\nPreliminary Analysis:")
        print("="*60)
        
        if len(low_perp) > 0:
            print(f"\nLow Perplexity Group (n={len(low_perp)}):")
            print(f"  Mean LLM Score: {low_perp['mean_score'].mean():.2f} (SD: {low_perp['mean_score'].std():.2f})")
            print(f"  Mean Human Score: {low_perp['score'].mean():.2f}")
        
        if len(high_perp) > 0:
            print(f"\nHigh Perplexity Group (n={len(high_perp)}):")
            print(f"  Mean LLM Score: {high_perp['mean_score'].mean():.2f} (SD: {high_perp['mean_score'].std():.2f})")
            print(f"  Mean Human Score: {high_perp['score'].mean():.2f}")
        
        if len(low_perp) > 1 and len(high_perp) > 1:
            # T-test
            t_stat, p_val = stats.ttest_ind(low_perp['mean_score'], high_perp['mean_score'])
            print(f"\nT-test (Low vs High Perplexity):")
            print(f"  t-statistic: {t_stat:.3f}")
            print(f"  p-value: {p_val:.3f}")
            
            if p_val < 0.05:
                print(f"  *** SIGNIFICANT DIFFERENCE FOUND ***")
            else:
                print(f"  No significant difference (yet)")
    
    except Exception as e:
        print(f"Could not analyze: {e}")
        print("Score some essays first in the CSV file")

if __name__ == "__main__":
    print("Step 4: LLM Scoring & Analysis")
    print("="*60)
    record_llm_scores()
    print("\n\nTo analyze results later, run: python3 step4_analyze_scores.py --analyze")