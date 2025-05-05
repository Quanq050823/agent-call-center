#!/usr/bin/env python
import sys
import warnings

from datetime import datetime

from src.argent_qualify_lead6.crew import ArgentQualifyLead6

warnings.filterwarnings("ignore", category=SyntaxWarning, module="pysbd")

# This main file is intended to be a way for you to run your
# crew locally, so refrain from adding unnecessary logic into this file.
# Replace with inputs you want to test with, it will automatically
# interpolate any tasks and agents information

def run():
    """
    Run the crew.
    """
    # Ví dụ về mẫu hội thoại để phân tích
    sample_conversation = """
    Sales Rep: Chào anh/chị, tôi là [Tên] từ [Công ty]. Cảm ơn anh/chị đã dành thời gian nói chuyện với tôi hôm nay. Tôi thấy anh/chị đã quan tâm đến giải pháp [Sản phẩm/Dịch vụ] của chúng tôi.
    Khách hàng: Vâng, tôi đang tìm kiếm một giải pháp để giải quyết [vấn đề cụ thể].
    Sales Rep: Anh/chị có thể chia sẻ thêm về tình huống hiện tại và thách thức mà doanh nghiệp đang gặp phải không?
    Khách hàng: Hiện tại chúng tôi đang gặp khó khăn trong việc [mô tả vấn đề]. Điều này ảnh hưởng đến [tác động đến doanh nghiệp].
    Sales Rep: Tôi hiểu. Giải pháp của chúng tôi có thể giúp anh/chị [giải quyết vấn đề] bằng cách [cách thức hoạt động]. Anh/chị có đang xem xét các giải pháp khác không?
    Khách hàng: Có, chúng tôi đang xem xét một vài giải pháp khác, nhưng chưa quyết định.
    Sales Rep: Về ngân sách cho dự án này, anh/chị đã có khoảng đầu tư dự kiến chưa?
    Khách hàng: Chúng tôi đang có khoảng 50,000 USD cho dự án này, nhưng con số này có thể linh hoạt nếu thấy giá trị rõ ràng.
    Sales Rep: Tuyệt vời. Về quy trình ra quyết định, ai sẽ là người phê duyệt cuối cùng cho dự án này?
    Khách hàng: Tôi sẽ đề xuất, nhưng quyết định cuối cùng sẽ do giám đốc tài chính của chúng tôi phê duyệt.
    Sales Rep: Anh/chị dự kiến khi nào muốn triển khai giải pháp này?
    Khách hàng: Chúng tôi hy vọng có thể bắt đầu trong quý tới, khoảng 2-3 tháng nữa.
    Sales Rep: Hiểu rồi. Vậy điều gì sẽ là yếu tố quan trọng nhất đối với anh/chị khi lựa chọn giải pháp?
    Khách hàng: Chúng tôi cần một giải pháp dễ triển khai, có hỗ trợ kỹ thuật tốt và có thể mở rộng khi doanh nghiệp phát triển.
    """
    
    inputs = {
        'topic': 'AI LLMs',
        'current_year': str(datetime.now().year),
        'conversation_transcript': sample_conversation
    }
    
    try:
        ArgentQualifyLead6().crew().kickoff(inputs=inputs)
    except Exception as e:
        raise Exception(f"An error occurred while running the crew: {e}")


run()