#!/usr/bin/env python
"""
Command line tool to evaluate lead qualification based on transcript.
Usage: python qualify_lead.py <path_to_lead_data.json> [path_to_criteria_prompt.txt]
"""

import json
import sys
import os
from src.argent_qualify_lead6.call_quality_evaluator import evaluate_lead_qualification

def print_usage():
    print(f"""
Usage: python {sys.argv[0]} <path_to_lead_data.json> [path_to_criteria_prompt.txt]

Arguments:
  path_to_lead_data.json    : Path to JSON file containing lead data with transcript
  path_to_criteria_prompt.txt: Path to text file containing business prompt with evaluation criteria (optional)
    """)

def read_lead_data(file_path):
    """Read lead data from JSON file."""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            lead_data = json.load(f)
        return lead_data
    except Exception as e:
        print(f"Error reading file {file_path}: {str(e)}")
        sys.exit(1)

def read_criteria_prompt(file_path):
    """Read business prompt from text file."""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            prompt = f.read()
        return prompt
    except Exception as e:
        print(f"Error reading file {file_path}: {str(e)}")
        sys.exit(1)

def get_default_prompt():
    """Return default business prompt when no prompt file is provided."""
    return """
    Lead qualification criteria:
    - Customer has a clear budget for product/service
    - Customer has decision-making authority
    - Customer has a clear need for the product/service
    - Customer has a specific implementation timeline
    """

def extract_transcript(lead_data):
    """Extract transcript from lead data."""
    try:
        if "leadData" in lead_data and "transcript" in lead_data["leadData"]:
            return lead_data["leadData"]["transcript"]
        else:
            print("Error: Field 'leadData.transcript' not found in lead data")
            sys.exit(1)
    except Exception as e:
        print(f"Error extracting transcript: {str(e)}")
        sys.exit(1)

def main():
    # Check command line parameters
    if len(sys.argv) < 2:
        print_usage()
        sys.exit(1)
    
    lead_data_path = sys.argv[1]
    
    # Read prompt from file if provided, otherwise use default
    if len(sys.argv) >= 3:
        criteria_prompt_path = sys.argv[2]
        prompt = read_criteria_prompt(criteria_prompt_path)
    else:
        prompt = get_default_prompt()
    
    # Read lead data
    lead_data = read_lead_data(lead_data_path)
    
    # Extract transcript
    transcript = extract_transcript(lead_data)
    
    # Evaluate lead qualification
    result_json = evaluate_lead_qualification(prompt, transcript)
    
    # Print evaluation result
    print(result_json)
    
    # Optional: Save result to file
    result_path = os.path.splitext(lead_data_path)[0] + "_result.json"
    with open(result_path, "w", encoding="utf-8") as f:
        f.write(result_json)
    print(f"\nResult saved to: {result_path}")

if __name__ == "__main__":
    main() 