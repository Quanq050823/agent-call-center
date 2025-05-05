#!/usr/bin/env python
"""
Module đơn giản để phân tích lead và trả về kết quả JSON.
"""
import json
from .tools.lead_analyzer_tool import LeadConversationAnalyzer

def qualify_lead(lead_data_json):
    """
    Nhận dữ liệu lead dưới dạng JSON string và trả về kết quả đánh giá đơn giản.
    
    Args:
        lead_data_json (str): Dữ liệu lead ở dạng chuỗi JSON
        
    Returns:
        str: Kết quả đánh giá dưới dạng chuỗi JSON
    """
    analyzer = LeadConversationAnalyzer()
    result = analyzer._run(lead_data_json)
    
    # Chuyển kết quả về dạng dict
    result_dict = json.loads(result)
    
    # Trả về kết quả đơn giản
    simple_result = {
        "score": result_dict.get("score", 0),
        "qualification_status": result_dict.get("qualification_status", "Not Pass")
    }
    
    return json.dumps(simple_result)

if __name__ == "__main__":
    # Ví dụ sử dụng
    sample_lead_data = {
        "_id": {"$oid": "6815bdbb1660633e3262c056"},
        "userId": {"$oid": "67b1c1331e12c93a79317bbb"},
        "flowId": {"$oid": "67f704b14cd3acb38825d64c"},
        "status": {"$numberInt": "2"},
        "leadData": {
            "website_link": "dagttax.vn",
            "email": "quangcuatuonglai@gmail.com",
            "full name": "Đức Quang",
            "phone": "+84355305120",
            "job_title": "it",
            "company_name": "it",
            "transcript": "Hello this is Alice from Wonderland. We will conduct some questions to verify if you meet our criterias.\nWhat's your name?\nJohn.\nHow old are you?\n21\nWhere do you live?\nHCM City\nWe will send you a verified e-mail if you met our criteria. Thanks for your time."
        },
        "nodeId": "aiCall_1745142844714",
        "createdAt": {"$date": {"$numberLong": "1746255291112"}},
        "updatedAt": {"$date": {"$numberLong": "1746255339382"}},
        "__v": {"$numberInt": "0"}
    }
    
    # Chuyển dữ liệu mẫu sang chuỗi JSON
    lead_json_str = json.dumps(sample_lead_data)
    
    # Phân tích và in kết quả
    result = qualify_lead(lead_json_str)
    print(result) 