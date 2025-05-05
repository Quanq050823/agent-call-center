#!/usr/bin/env python
"""
Script để test API đánh giá chất lượng cuộc gọi.
"""
import requests
import json

# URL API
API_URL = "http://localhost:5000/api/evaluate-call-quality"
LEAD_QUALITY_URL = "http://localhost:5000/api/evaluate-lead-quality"

# Dữ liệu mẫu
sample_prompt = """
Hãy đảm bảo cuộc gọi bao gồm các nội dung sau:
- Giới thiệu tên và công ty
- Hỏi tên khách hàng
- Hỏi tuổi khách hàng
- Hỏi nơi khách hàng đang sống
- Kết thúc cuộc gọi với lời cảm ơn
"""

sample_transcript = """
Hello this is Alice from Wonderland. We will conduct some questions to verify if you meet our criterias.
What's your name?
John.
How old are you?
21
Where do you live?
HCM City
We will send you a verified e-mail if you met our criteria. Thanks for your time.
"""

# Dữ liệu lead mẫu
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

def test_evaluate_call_quality():
    """Test API đánh giá chất lượng cuộc gọi."""
    
    # Tạo request data
    request_data = {
        "prompt": sample_prompt,
        "transcript": sample_transcript
    }
    
    # Gửi request
    response = requests.post(
        API_URL,
        json=request_data,
        headers={"Content-Type": "application/json"}
    )
    
    # Xử lý kết quả
    if response.status_code == 200:
        result = response.json()
        print("=== ĐÁNH GIÁ CHẤT LƯỢNG CUỘC GỌI ===")
        print(json.dumps(result, indent=2, ensure_ascii=False))
    else:
        print(f"Lỗi: {response.status_code}")
        print(response.text)

def test_evaluate_lead_quality():
    """Test API đánh giá chất lượng lead."""
    
    # Tạo request data
    request_data = {
        "prompt": sample_prompt,
        "data": sample_lead_data
    }
    
    # Gửi request
    response = requests.post(
        LEAD_QUALITY_URL,
        json=request_data,
        headers={"Content-Type": "application/json"}
    )
    
    # Xử lý kết quả
    if response.status_code == 200:
        result = response.json()
        print("=== ĐÁNH GIÁ CHẤT LƯỢNG LEAD ===")
        print(json.dumps(result, indent=2, ensure_ascii=False))
    else:
        print(f"Lỗi: {response.status_code}")
        print(response.text)

if __name__ == "__main__":
    # Chạy test
    print("Đang test API đánh giá chất lượng cuộc gọi...")
    test_evaluate_call_quality()
    print("\n")
    print("Đang test API đánh giá chất lượng lead...")
    test_evaluate_lead_quality() 