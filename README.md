# Argent Lead Qualification

An application for evaluating lead qualification based on analysis of conversation transcripts (between sales representatives and potential customers), according to criteria from a business prompt.

## Features

1. **Lead Analysis Based on Criteria**

   - Extract evaluation criteria from business prompt
   - Analyze transcript against each criterion (Met/Not Met/Unclear)
   - Calculate confidence score (0-100)
   - Provide conclusion: Qualified/Disqualified/Needs More Info

2. **Intelligent Analysis Using Pattern Matching**

   - Identify patterns related to BANT (Budget, Authority, Need, Timeline)
   - Extract important information from conversation transcripts
   - Generate detailed explanations for each criterion

3. **API Endpoints**

   - `/api/evaluate-lead`: Evaluate lead from business prompt and transcript
   - `/api/evaluate-lead-from-data`: Evaluate lead from business prompt and JSON data

4. **Command Line Tools**
   - Analyze leads from JSON files with customizable prompts
   - Save analysis results in JSON format

## Installation

1. Install required libraries:

```bash
pip install -r requirements.txt
```

2. Make sure you have Flask installed:

```bash
pip install flask
```

## Usage

### Run API Server

```bash
python api_server.py
```

The server will start at `http://localhost:5000`

### API Endpoints

1. **Evaluate Lead from Prompt and Transcript**

   - URL: `/api/evaluate-lead`
   - Method: POST
   - Body:
     ```json
     {
     	"prompt": "Business prompt containing lead evaluation criteria",
     	"transcript": "Call conversation content to evaluate"
     }
     ```
   - Response:
     ```json
     {
     	"qualification_status": "Qualified/Disqualified/Needs More Info",
     	"confidence_score": 85,
     	"criteria_evaluation": {
     		"Criterion 1": "Met - Found: relevant information",
     		"Criterion 2": "Not Met - Not enough relevant information found"
     	},
     	"notes": "Important additional observations"
     }
     ```

2. **Evaluate Lead from JSON Data**
   - URL: `/api/evaluate-lead-from-data`
   - Method: POST
   - Body:
     ```json
     {
     	"prompt": "Business prompt containing lead evaluation criteria",
     	"data": {
     		"_id": { "$oid": "..." },
     		"leadData": {
     			"transcript": "Call conversation content to evaluate"
     		}
     	}
     }
     ```
   - Response: Same as `/api/evaluate-lead` but with added `lead_id` field

### Command Line Tools

1. **Evaluate Lead from JSON File**:

   ```bash
   python qualify_lead.py sample_lead.json [path_to_criteria_prompt.txt]
   ```

   - Parameter `sample_lead.json`: JSON file containing lead data
   - Parameter `path_to_criteria_prompt.txt` (optional): Text file containing business prompt with evaluation criteria

2. **Example API Usage**:
   ```bash
   python example_api_usage.py
   ```

## Using in Code

```python
# Evaluate lead qualification
from src.argent_qualify_lead6.call_quality_evaluator import evaluate_lead_qualification

# Define prompt and transcript
prompt = """
Lead qualification criteria:
- Customer has a minimum budget of $10,000
- Customer has decision-making authority
- Customer has a clear need for the product
- Customer needs implementation within 3 months
"""

transcript = """
Sales: Hello, our company specializes in management software solutions. What product are you interested in?
Customer: I need a human resources management system for my company.
Sales: Great, when do you plan to implement it?
Customer: I want to implement it next month.
Sales: What's the budget for this project?
Customer: About $15,000.
Sales: Are you the final decision maker?
Customer: Yes, I'm the HR director and I have the authority to make this decision.
"""

# Evaluate lead qualification
result_json = evaluate_lead_qualification(prompt, transcript)
print(result_json)
```

## System Requirements

- Python 3.8+
- Flask
- Other libraries listed in requirements.txt

## System Prompt of AI Lead Qualification Agent

```
You are an AI Lead Qualification Agent specialized in analyzing sales call transcripts to evaluate leads.

## Your Tasks

1. Receive input including:
   - Business Prompt (company description and lead qualification criteria)
   - Sales call transcript

2. Analysis:
   - Extract evaluation criteria from the Business Prompt
   - Evaluate the transcript against each criterion
   - Score the compliance level (0-100)

3. Return output in JSON format:
{
  "qualification_status": "Qualified/Disqualified/Needs More Info",
  "confidence_score": 0-100,
  "criteria_evaluation": {
    "Criterion 1": "Met/Not Met/Unclear - brief explanation",
    "Criterion 2": "Met/Not Met/Unclear - brief explanation"
  },
  "notes": "Important additional observations"
}

## Evaluation Rules

1. Only mark as "Qualified" when ALL essential criteria are met
2. Mark "Unclear" for information that is not clear
3. Do not assume information not present in the transcript
4. Analysis should be objective, detailed but concise
```
