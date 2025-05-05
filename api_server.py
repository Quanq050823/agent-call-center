#!/usr/bin/env python
"""
API server for lead qualification evaluation service
"""

import os
import sys

# Add root directory to sys.path for easier imports
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

# Import Flask app from api module
from src.argent_qualify_lead6.api import app

if __name__ == "__main__":
    print("Starting Lead Qualification API Server...")
    print("API available at http://localhost:5000")
    print("Endpoints:")
    print("  - POST /api/evaluate-lead")
    print("  - POST /api/evaluate-lead-from-data")
    app.run(debug=True, host='0.0.0.0', port=5000) 