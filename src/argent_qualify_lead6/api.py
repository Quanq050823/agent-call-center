#!/usr/bin/env python
from flask import Flask, request, jsonify
import json
import os
import sys

# Add project root directory to sys.path for easier imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from src.argent_qualify_lead6.call_quality_evaluator import evaluate_lead_qualification

app = Flask(__name__)

@app.route('/api/evaluate-lead', methods=['POST'])
def evaluate_lead():
    """
    API endpoint to evaluate lead qualification based on business prompt and transcript.
    
    Request:
    {
        "prompt": "Business prompt containing lead evaluation criteria",
        "transcript": "Call conversation content to evaluate"
    }
    
    Response: JSON with format:
    {
        "qualification_status": "Qualified/Disqualified/Needs More Info",
        "confidence_score": 0-100,
        "criteria_evaluation": {
            "Criterion 1": "Met/Not Met/Unclear - brief explanation",
            "Criterion 2": "Met/Not Met/Unclear - brief explanation"
        },
        "notes": "Additional observations"
    }
    """
    try:
        # Get data from request
        request_data = request.json
        
        if not request_data or 'prompt' not in request_data or 'transcript' not in request_data:
            return jsonify({
                "error": "Missing required fields 'prompt' and/or 'transcript'",
                "qualification_status": "Needs More Info",
                "confidence_score": 0,
                "criteria_evaluation": {},
                "notes": "Missing required data."
            }), 400
            
        # Get prompt and transcript
        prompt = request_data['prompt']
        transcript = request_data['transcript']
        
        # Evaluate lead qualification
        result_json = evaluate_lead_qualification(prompt, transcript)
        result_dict = json.loads(result_json)
        
        # Return result
        return jsonify(result_dict)
        
    except Exception as e:
        return jsonify({
            "error": str(e),
            "qualification_status": "Needs More Info",
            "confidence_score": 0,
            "criteria_evaluation": {},
            "notes": f"Error: {str(e)}"
        }), 500

@app.route('/api/evaluate-lead-from-data', methods=['POST'])
def evaluate_lead_from_data():
    """
    API endpoint to evaluate lead qualification from JSON data containing prompt and transcript.
    
    Request:
    {
        "prompt": "Business prompt containing lead evaluation criteria",
        "data": {
            "_id": { "$oid": "..." }, // Optional
            "leadData": {
                "transcript": "Call conversation content to evaluate"
            }
        }
    }
    
    Response: JSON with format:
    {
        "qualification_status": "Qualified/Disqualified/Needs More Info",
        "confidence_score": 0-100,
        "criteria_evaluation": {
            "Criterion 1": "Met/Not Met/Unclear - brief explanation",
            "Criterion 2": "Met/Not Met/Unclear - brief explanation"
        },
        "notes": "Additional observations",
        "lead_id": "Lead ID (if available)"
    }
    """
    try:
        # Get data from request
        request_data = request.json
        
        if not request_data or 'prompt' not in request_data or 'data' not in request_data:
            return jsonify({
                "error": "Missing required fields 'prompt' and/or 'data'",
                "qualification_status": "Needs More Info",
                "confidence_score": 0,
                "criteria_evaluation": {},
                "notes": "Missing required data."
            }), 400
            
        # Get prompt and lead data
        prompt = request_data['prompt']
        lead_data = request_data['data']
        
        # Get transcript from lead data
        if "leadData" in lead_data and "transcript" in lead_data["leadData"]:
            transcript = lead_data["leadData"]["transcript"]
        else:
            return jsonify({
                "error": "Missing transcript in leadData",
                "qualification_status": "Needs More Info",
                "confidence_score": 0,
                "criteria_evaluation": {},
                "notes": "Missing transcript in lead data."
            }), 400
        
        # Evaluate lead qualification
        result_json = evaluate_lead_qualification(prompt, transcript)
        result_dict = json.loads(result_json)
        
        # Add lead information to the result
        result_dict["lead_id"] = lead_data.get("_id", {}).get("$oid", "") if "_id" in lead_data else ""
        
        # Return result
        return jsonify(result_dict)
        
    except Exception as e:
        return jsonify({
            "error": str(e),
            "qualification_status": "Needs More Info",
            "confidence_score": 0,
            "criteria_evaluation": {},
            "notes": f"Error: {str(e)}"
        }), 500

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000) 