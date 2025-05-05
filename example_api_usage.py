#!/usr/bin/env python
"""
Example of using the Lead Qualification API
"""

import requests
import json

# API server URL - change if needed
API_BASE_URL = "http://localhost:5000"

def evaluate_lead_with_transcript(prompt, transcript):
    """
    Call the API to evaluate lead qualification based on business prompt and transcript.
    
    Args:
        prompt (str): Business prompt containing evaluation criteria
        transcript (str): Call conversation content to evaluate
        
    Returns:
        dict: Lead evaluation result
    """
    endpoint = f"{API_BASE_URL}/api/evaluate-lead"
    
    payload = {
        "prompt": prompt,
        "transcript": transcript
    }
    
    headers = {
        "Content-Type": "application/json"
    }
    
    response = requests.post(endpoint, json=payload, headers=headers)
    
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Error: {response.status_code}")
        print(response.text)
        return None

def evaluate_lead_from_data(prompt, lead_data):
    """
    Call the API to evaluate lead qualification based on business prompt and lead data.
    
    Args:
        prompt (str): Business prompt containing evaluation criteria
        lead_data (dict): Lead data containing transcript
        
    Returns:
        dict: Lead evaluation result
    """
    endpoint = f"{API_BASE_URL}/api/evaluate-lead-from-data"
    
    payload = {
        "prompt": prompt,
        "data": lead_data
    }
    
    headers = {
        "Content-Type": "application/json"
    }
    
    response = requests.post(endpoint, json=payload, headers=headers)
    
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Error: {response.status_code}")
        print(response.text)
        return None

def load_sample_data(file_path):
    """
    Read sample lead data from a JSON file.
    
    Args:
        file_path (str): Path to the JSON file
        
    Returns:
        dict: Lead data
    """
    with open(file_path, 'r', encoding='utf-8') as f:
        return json.load(f)

def main():
    # Example 1: Evaluate lead with direct prompt and transcript
    sample_prompt = """
    Lead qualification criteria:
    - Customer has a minimum budget of $10,000
    - Customer has decision-making authority
    - Customer has a clear need for the product
    - Customer needs implementation within 3 months
    """
    
    sample_transcript = """
    Sales: Hello, our company specializes in management software solutions. What product are you interested in?
    Customer: I need a human resources management system for my company.
    Sales: Great, when do you plan to implement it?
    Customer: I want to implement it next month.
    Sales: What's the budget for this project?
    Customer: About $15,000.
    Sales: Are you the final decision maker?
    Customer: Yes, I'm the HR director and I have the authority to make this decision.
    """
    
    print("Example 1: Evaluate lead with direct prompt and transcript")
    result1 = evaluate_lead_with_transcript(sample_prompt, sample_transcript)
    if result1:
        print(json.dumps(result1, indent=2, ensure_ascii=False))
    print("\n" + "-"*50 + "\n")
    
    # Example 2: Evaluate lead from JSON data
    try:
        sample_lead_data = load_sample_data("sample_lead.json")
        
        print("Example 2: Evaluate lead from JSON data")
        result2 = evaluate_lead_from_data(sample_prompt, sample_lead_data)
        if result2:
            print(json.dumps(result2, indent=2, ensure_ascii=False))
    except FileNotFoundError:
        print("File sample_lead.json not found")
    
if __name__ == "__main__":
    main() 