#!/usr/bin/env python
"""
Module for lead qualification evaluation based on system prompt and transcript.
"""
import json
import re
from typing import Dict, List, Any, Tuple

class LeadQualificationEvaluator:
    """
    Evaluates lead qualification based on business prompt and call transcript.
    """
    
    SYSTEM_PROMPT = """
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
    """
    
    def __init__(self):
        """
        Initialize the lead qualification evaluation object.
        """
        pass
    
    def extract_criteria_from_prompt(self, prompt: str) -> List[str]:
        """
        Extract criteria from the prompt.
        
        Args:
            prompt (str): Prompt containing the evaluation criteria
            
        Returns:
            List[str]: List of criteria
        """
        # Analyze prompt to extract criteria
        criteria = []
        
        # Find bullet points or numbered lists more precisely with better handling of multiline text
        bullet_points = re.findall(r'[-•*]\s*(.*?)(?=\s*\n\s*[-•*]|\s*\n\s*\n|\s*\Z)', prompt, re.DOTALL)
        numbered_points = re.findall(r'\d+\.\s*(.*?)(?=\s*\n\s*\d+\.|\s*\n\s*\n|\s*\Z)', prompt, re.DOTALL)
        
        # Combine the found points and clean them (remove extra whitespace and newlines)
        for point in bullet_points:
            clean_point = re.sub(r'\s+', ' ', point).strip()
            if clean_point:
                criteria.append(clean_point)
                
        for point in numbered_points:
            clean_point = re.sub(r'\s+', ' ', point).strip()
            if clean_point:
                criteria.append(clean_point)
        
        # If no lists are found using the above methods, try a simpler approach
        if not criteria:
            # Try to split by common bullet point markers
            lines = prompt.split('\n')
            for line in lines:
                line = line.strip()
                # Check if line starts with a bullet point or number
                if re.match(r'^[-•*]\s+\w+', line) or re.match(r'^\d+\.\s+\w+', line):
                    # Remove the bullet point or number
                    clean_line = re.sub(r'^[-•*]\d+\.\s+', '', line).strip()
                    if clean_line:
                        criteria.append(clean_line)
        
        # If still no criteria found, split by sentences
        if not criteria:
            sentences = re.split(r'[.!?]\s+', prompt)
            for sentence in sentences:
                clean_sentence = sentence.strip()
                if clean_sentence and len(clean_sentence) > 10:  # Avoid short fragments
                    criteria.append(clean_sentence)
        
        # For debugging, print how many criteria were found
        print(f"Criteria extraction found {len(criteria)} items")
        
        return criteria
    
    def evaluate_criterion(self, criterion: str, transcript: str) -> Tuple[str, str]:
        """
        Evaluate a specific criterion based on the transcript.
        
        Args:
            criterion (str): Criterion to evaluate
            transcript (str): Conversation transcript to evaluate
            
        Returns:
            Tuple[str, str]: (Evaluation status, Explanation)
        """
        # Create keywords and patterns
        keywords = self._extract_keywords(criterion)
        patterns = self._create_patterns(criterion)
        
        # Check if keywords are in the transcript
        matches = 0
        total_keywords = len(keywords)
        
        if total_keywords == 0:
            return "Unclear", "Cannot determine criterion"
            
        for keyword in keywords:
            # Use word boundary to find exact matches
            pattern = r'\b' + re.escape(keyword) + r'\b'
            if re.search(pattern, transcript.lower()):
                matches += 1
        
        # Check specific pattern matches
        pattern_matches = 0
        pattern_explanations = []
        
        for pattern, expected_text in patterns:
            if pattern.search(transcript.lower()):
                pattern_matches += 1
                pattern_explanations.append(expected_text)
                # When a pattern matches, increase matches more significantly
                matches += 3  # Increased from 2 to 3 to give patterns more weight
        
        # Evaluate match level - lowered thresholds for better matching
        match_ratio = matches / max(total_keywords, 1)
        
        # If we have pattern matches, it should heavily influence the result
        if pattern_matches > 0:
            status = "Met"
            explanation = f"Found: {', '.join(pattern_explanations)}"
        elif match_ratio > 0.4:  # Lowered from 0.6 to 0.4
            status = "Met"
            explanation = f"Found {matches}/{total_keywords} keywords"
        elif match_ratio > 0.2:  # Lowered from 0.3 to 0.2
            status = "Unclear"
            explanation = "Some information found but not sufficient"
        else:
            status = "Not Met"
            explanation = "Not enough relevant information found"
            
        return status, explanation
    
    def _extract_keywords(self, criterion: str) -> List[str]:
        """
        Extract keywords from the criterion.
        
        Args:
            criterion (str): Criterion to extract keywords from
            
        Returns:
            List[str]: List of keywords
        """
        # Remove stop words - expanded list
        stop_words = ['a', 'an', 'the', 'and', 'or', 'is', 'has', 'of', 'in', 'about', 
                      'with', 'to', 'from', 'including', 'content', 'after', 'ensure',
                      'for', 'that', 'this', 'these', 'those', 'be', 'as', 'by', 'at', 'on']
        
        # Split into words
        words = re.findall(r'\b\w+\b', criterion.lower())
        
        # Remove stop words and words that are too short
        keywords = [word for word in words if word not in stop_words and len(word) > 2]  # Changed from 1 to 2
        
        # Add specific keywords based on the context of the criterion
        if "budget" in criterion.lower() or "cost" in criterion.lower() or "price" in criterion.lower() or "$" in criterion:
            keywords.extend(["budget", "cost", "price", "payment", "afford", "spend", "spending", "money", 
                           "dollars", "usd", "$", "financial", "invest", "investment", "fund", "funding"])
            
        if "decision" in criterion.lower() or "authority" in criterion.lower():
            keywords.extend(["decide", "decision", "authority", "approve", "approval", "authorized", "power",
                           "sign off", "green light", "go ahead", "permission", "authorize", "final", "say"])
            
        if "need" in criterion.lower() or "requirement" in criterion.lower() or "problem" in criterion.lower():
            keywords.extend(["need", "require", "want", "must", "should", "requirement", "problem", "solution",
                           "issue", "challenge", "difficulty", "pain point", "necessity", "essential", "important"])
            
        if "time" in criterion.lower() or "timeline" in criterion.lower() or "month" in criterion.lower():
            keywords.extend(["when", "timeline", "deadline", "schedule", "month", "year", "date", "time",
                           "quarter", "q1", "q2", "q3", "q4", "soon", "asap", "immediate", "urgency", "week"])
        
        # Look for numeric values in criterion (e.g., "10,000")
        numbers = re.findall(r'\d[\d,.]*', criterion)
        if numbers:
            for number in numbers:
                # Clean number and add to keywords
                clean_number = number.replace(',', '')
                keywords.append(clean_number)
        
        return keywords
    
    def _create_patterns(self, criterion: str) -> List[Tuple[re.Pattern, str]]:
        """
        Create regex patterns for more specific searches.
        
        Args:
            criterion (str): Criterion to create patterns for
            
        Returns:
            List[Tuple[re.Pattern, str]]: List of (pattern, description)
        """
        patterns = []
        
        # Extract numbers from criterion for more specific matching
        amount_matches = re.findall(r'(\$?\s*\d[\d,.]*\s*k?\s*(?:thousand|million|dollars|usd)?)', criterion.lower())
        amount_value = None
        if amount_matches:
            for amount in amount_matches:
                # Clean and store the amount for comparison
                cleaned = re.sub(r'[^\d.]', '', amount)
                if cleaned:
                    try:
                        amount_value = float(cleaned)
                        # If "k" or "thousand" in the amount, multiply by 1000
                        if 'k' in amount or 'thousand' in amount:
                            amount_value *= 1000
                    except ValueError:
                        pass
        
        # Budget
        if "budget" in criterion.lower() or "cost" in criterion.lower() or "price" in criterion.lower() or "$" in criterion:
            # Generic budget patterns
            patterns.append((re.compile(r"(budget|cost|price|payment|afford|spend|spending).{0,30}([\d,.]+\s*(usd|dollars|k)|\$\s*[\d,.]+)"), "specific budget discussion"))
            patterns.append((re.compile(r"(how much).{0,20}(cost|price|pay)"), "asking about cost"))
            patterns.append((re.compile(r"([\d,.]+\s*(dollars|usd)|\$\s*[\d,.]+)"), "mentioned specific amount"))
            
            # If we found a specific amount in the criterion, create a pattern to match amounts that exceed it
            if amount_value:
                # Pattern to match numbers in the transcript
                patterns.append((re.compile(r"([\d,.]+\s*(k|thousand|dollars|usd)|\$\s*[\d,.]+)"), "mentioned budget amount"))
                
        # Authority
        if "decision" in criterion.lower() or "authority" in criterion.lower():
            patterns.append((re.compile(r"(i|we).{0,15}(decide|approval|decision|authority|authorized|sign off)"), "has decision-making authority"))
            patterns.append((re.compile(r"(i am|i'm|i have).{0,15}(authority|authorized|decision maker|final say)"), "has decision-making authority"))
            patterns.append((re.compile(r"(my|the).{0,10}(decision|approval|authorization)"), "has decision-making authority"))
            patterns.append((re.compile(r"(yes).{0,30}(decision|authority|authorized|approve|sign)"), "confirmed decision authority"))
            # Negative patterns
            patterns.append((re.compile(r"(talk|speak|discuss|consult|need).{0,20}(manager|boss|director|team|board|approval)"), "needs to consult others"))
            
        # Need
        if "need" in criterion.lower() or "requirement" in criterion.lower():
            patterns.append((re.compile(r"(need|require|want|must|have to|looking for).{0,30}(solution|product|service|software|system|platform|tool)"), "specific need identified"))
            patterns.append((re.compile(r"(need|want|looking for).{0,5}(a|an).{0,20}(system|solution|product)"), "expressed need for product"))
            patterns.append((re.compile(r"(facing|having|experiencing).{0,20}(issue|problem|challenge|difficulty)"), "has problem that needs solving"))
            
        # Timeline
        if "time" in criterion.lower() or "timeline" in criterion.lower() or "month" in criterion.lower():
            # Specific date mentions
            patterns.append((re.compile(r"(by|before|within|until).{0,15}(january|february|march|april|may|june|july|august|september|october|november|december|jan|feb|mar|apr|may|jun|jul|aug|sep|oct|nov|dec)"), "specific timeframe mentioned"))
            # General timeline
            patterns.append((re.compile(r"(need|want|require|implement|start|begin|launch).{0,15}(asap|immediately|urgently|soon|quickly)"), "needs urgent implementation"))
            patterns.append((re.compile(r"(next|coming|this).{0,10}(week|month|quarter|year)"), "planned for upcoming period"))
            patterns.append((re.compile(r"(within|in).{0,5}(\d+).{0,5}(days|weeks|months)"), "specific timeline mentioned"))
            
            # If the criterion specifies a number of months, create a specific pattern
            month_match = re.search(r'(\d+)\s*months?', criterion.lower())
            if month_match:
                month_value = int(month_match.group(1))
                # Create patterns to look for dates within that timeframe
                patterns.append((re.compile(r"(next|this|coming|within).{0,5}(\d+).{0,5}(month|months)"), "timeline specified in months"))
                patterns.append((re.compile(r"(next|this|coming).{0,5}(month|week|few weeks)"), "near-term implementation planned"))
        
        return patterns
        
    def evaluate(self, prompt: str, transcript: str) -> Dict[str, Any]:
        """
        Evaluate lead qualification.
        
        Args:
            prompt (str): Business prompt containing evaluation criteria
            transcript (str): Conversation transcript to evaluate
            
        Returns:
            Dict[str, Any]: Evaluation result in JSON format
        """
        # Extract criteria from prompt
        criteria = self.extract_criteria_from_prompt(prompt)
        
        # Debug print
        print(f"Extracted {len(criteria)} criteria: {criteria}")
        
        # Evaluate each criterion
        criteria_evaluation = {}
        met_count = 0
        unclear_count = 0
        not_met_count = 0
        
        for criterion in criteria:
            status, explanation = self.evaluate_criterion(criterion, transcript)
            criteria_evaluation[criterion] = f"{status} - {explanation}"
            
            print(f"Criterion: '{criterion}' -> {status} - {explanation}")
            
            if status == "Met":
                met_count += 1
            elif status == "Unclear":
                unclear_count += 1
            else:  # Not Met
                not_met_count += 1
        
        # Calculate confidence and status
        total_criteria = len(criteria)
        
        if total_criteria > 0:
            # Modified scoring formula that gives more weight to "Met" criteria
            # and partial credit for "Unclear" criteria
            confidence_score = int(((met_count + (unclear_count * 0.5)) / total_criteria) * 100)
            
            # Determine qualification status
            if met_count == total_criteria:
                qualification_status = "Qualified"
            elif not_met_count > 0:
                qualification_status = "Disqualified"
            else:
                qualification_status = "Needs More Info"
        else:
            confidence_score = 0
            qualification_status = "Needs More Info"
        
        # Create notes
        notes = []
        if unclear_count > 0:
            notes.append(f"There are {unclear_count} unclear criteria that need more information.")
        if not_met_count > 0:
            notes.append(f"There are {not_met_count} criteria that are not met.")
        
        # Create result with new structure
        result = {
            "qualification_status": qualification_status,
            "confidence_score": confidence_score,
            "criteria_evaluation": criteria_evaluation,
            "notes": ". ".join(notes) if notes else "No additional notes."
        }
        
        return result

def evaluate_lead_qualification(prompt: str, transcript: str) -> str:
    """
    Utility function to evaluate lead qualification.
    
    Args:
        prompt (str): Business prompt containing evaluation criteria
        transcript (str): Conversation transcript to evaluate
        
    Returns:
        str: Evaluation result as JSON string
    """
    evaluator = LeadQualificationEvaluator()
    result = evaluator.evaluate(prompt, transcript)
    return json.dumps(result, ensure_ascii=False, indent=2)

# Example usage
if __name__ == "__main__":
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
    
    result = evaluate_lead_qualification(sample_prompt, sample_transcript)
    print(result) 