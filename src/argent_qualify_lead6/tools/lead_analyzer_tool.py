from crewai.tools import BaseTool
from typing import Type, Dict, Any, Union
from pydantic import BaseModel, Field
import json


class LeadConversationAnalyzerInput(BaseModel):
    """Input schema for LeadConversationAnalyzer."""
    lead_data: str = Field(..., description="Dữ liệu lead customer ở định dạng JSON.")

class LeadConversationAnalyzer(BaseTool):
    name: str = "Lead Conversation Analyzer"
    description: str = (
        "Công cụ này phân tích dữ liệu lead customer và đánh giá các yếu tố quan trọng như: "
        "nhu cầu của khách hàng, ngân sách, quyền quyết định, thời gian triển khai và mức độ quan tâm."
    )
    args_schema: Type[BaseModel] = LeadConversationAnalyzerInput

    def _run(self, lead_data: str) -> str:
        """
        Phân tích dữ liệu lead customer và trả về đánh giá về lead dưới dạng JSON.
        """
        try:
            # Parse JSON input
            lead_json = json.loads(lead_data)
            
            # Extract transcript from leadData
            if "leadData" in lead_json and "transcript" in lead_json["leadData"]:
                transcript = lead_json["leadData"]["transcript"]
            else:
                return json.dumps({
                    "error": "Missing transcript in leadData",
                    "score": 0,
                    "qualification_status": "Not Pass"
                })
            
            # Phân tích đoạn hội thoại
            analysis = {
                "needs_identified": self._analyze_needs(transcript),
                "budget_discussed": self._analyze_budget(transcript),
                "decision_maker": self._analyze_authority(transcript),
                "timeline_defined": self._analyze_timeline(transcript),
                "interest_level": self._analyze_interest(transcript)
            }
            
            # Tính điểm và đưa ra kết luận
            qualification_score = self._calculate_qualification_score(analysis)
            qualification_status = "Pass" if qualification_score >= 7 else "Not Pass"
            
            # Tạo kết quả trả về
            result = {
                "lead_id": lead_json.get("_id", {}).get("$oid", ""),
                "user_id": lead_json.get("userId", {}).get("$oid", ""),
                "analysis": analysis,
                "score": qualification_score,
                "qualification_status": qualification_status,
                "recommendation": self._generate_recommendation(analysis, qualification_score)
            }
            
            return json.dumps(result)
        
        except json.JSONDecodeError:
            return json.dumps({
                "error": "Invalid JSON input",
                "score": 0,
                "qualification_status": "Not Pass"
            })
        except Exception as e:
            return json.dumps({
                "error": str(e),
                "score": 0,
                "qualification_status": "Not Pass"
            })
    
    def _analyze_needs(self, transcript):
        """Phân tích nhu cầu của khách hàng từ đoạn hội thoại"""
        # Đây là phiên bản đơn giản, trong thực tế cần dùng NLP phức tạp hơn
        keywords = ["tìm kiếm", "cần", "giải quyết", "vấn đề", "thách thức", "khó khăn"]
        score = 0
        
        # Đếm số từ khóa xuất hiện trong đoạn hội thoại
        for keyword in keywords:
            if keyword.lower() in transcript.lower():
                score += 1.5
        
        # Điều chỉnh điểm số về thang 10
        return min(score, 10)
    
    def _analyze_budget(self, transcript):
        """Phân tích thông tin về ngân sách"""
        budget_keywords = ["ngân sách", "chi phí", "đầu tư", "giá", "tiền", "USD", "VND"]
        score = 0
        
        for keyword in budget_keywords:
            if keyword.lower() in transcript.lower():
                score += 1.5
        
        return min(score, 10)
    
    def _analyze_authority(self, transcript):
        """Phân tích quyền quyết định của lead"""
        authority_keywords = ["quyết định", "phê duyệt", "giám đốc", "quản lý", "CEO", "CFO", "CTO"]
        score = 0
        
        for keyword in authority_keywords:
            if keyword.lower() in transcript.lower():
                score += 1.5
        
        return min(score, 10)
    
    def _analyze_timeline(self, transcript):
        """Phân tích thông tin về thời gian triển khai"""
        timeline_keywords = ["khi nào", "thời gian", "triển khai", "tháng", "quý", "năm", "lịch trình"]
        score = 0
        
        for keyword in timeline_keywords:
            if keyword.lower() in transcript.lower():
                score += 1.5
        
        return min(score, 10)
    
    def _analyze_interest(self, transcript):
        """Phân tích mức độ quan tâm của lead"""
        interest_keywords = ["quan tâm", "thích", "ưu tiên", "muốn", "cần", "sẵn sàng"]
        score = 0
        
        for keyword in interest_keywords:
            if keyword.lower() in transcript.lower():
                score += 1.5
        
        return min(score, 10)
    
    def _calculate_qualification_score(self, analysis):
        """Tính điểm đánh giá dựa trên các yếu tố phân tích"""
        weights = {
            "needs_identified": 0.25,
            "budget_discussed": 0.25,
            "decision_maker": 0.2,
            "timeline_defined": 0.15,
            "interest_level": 0.15
        }
        
        score = sum(analysis[key] * weights[key] for key in weights)
        return round(score, 1)
    
    def _generate_recommendation(self, analysis, score):
        """Tạo đề xuất dựa trên phân tích"""
        if score >= 7:
            return "Nên tiếp tục tương tác với lead này. Có cơ hội cao để chuyển đổi thành khách hàng."
        elif score >= 5:
            return "Lead có tiềm năng nhưng cần thêm thông tin. Đề xuất một cuộc gọi theo dõi để làm rõ các điểm chưa rõ."
        else:
            return "Lead chưa sẵn sàng hoặc không phù hợp. Nên chuyển sang nurturing hoặc xem xét lại sau." 